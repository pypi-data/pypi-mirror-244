import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import sacrebleu
from tqdm import tqdm
import math
from sentia import SENTIAForCausalLM, SENTIAConfig, SENTIADataset
import wandb
from transformers import AutoTokenizer
from datasets import load_dataset

STRING_TO_DTYPE_MAPPING = {
     "float32": torch.float32,
     "float16": torch.float16,
     "float64": torch.float64,
     "float8_e4m3fn": torch.float8_e4m3fn,
     "float8": torch.float8_e4m3fn,
     "float8_e5m2": torch.float8_e5m2,
}

def train(model, dataloader, optimizer, tokenizer, device="cuda"):
    model.train()
    total_loss = 0
    total_perplexity = 0

    for i, batch in tqdm(enumerate(dataloader)):
                input_ids = batch["input_ids"].to(device)
                target_ids = batch["labels"].to(device)
                target_text = batch["target_text"]
                # Generate the output and calculate the loss
                outputs = model(input_ids=input_ids, labels=target_ids)
                loss, logits = outputs[:2]
                # loss = torch.exp(loss)
                # Calculate the BLEU score
                # probs = F.softmax(logits, dim=-1)
                predictions = torch.argmax(logits, dim=-1)
                predictions_str = [tokenizer.decode(pred, skip_special_tokens=True) for pred in predictions.tolist()]
                target_ids_str = [tokenizer.decode(tgt, skip_special_tokens=True) for tgt in target_ids.tolist()]
                print(predictions_str[0])
                bleu_scores = []
                accuracy_scores = []
                for pred_str, target_str in zip(predictions_str, target_ids_str):
                    bleu = sacrebleu.sentence_bleu(pred_str, [target_str])
                    bleu_scores.append(bleu.score)
                for pred_id, target_id in zip(predictions, target_ids):
                    accuracy = SENTIAForCausalLM.calculate_accuracy(pred_id, target_id)
                    accuracy_scores.append(accuracy)

                accuracy = sum(accuracy_scores) / len(accuracy_scores)
                bleu = sum(bleu_scores) / len(bleu_scores)
                # Calculate the reward
                reward, penalty = SENTIAForCausalLM.get_reward(predictions.tolist()[0], target_ids.tolist()[0], bleu)
                ol = loss
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
                # Update the metrics
                total_loss += loss.item()
                # total_reward += reward
                
                total_perplexity += torch.exp(ol).item()
                #wandb.log({"loss": ol.item(), "bleu": bleu, "perplexity": torch.exp(ol).item(), "accuracy": accuracy})
                print(
                    f"Batch {i + 1}/{len(dataloader)}: Loss - {ol.item():.4f}, NetReward - {reward - penalty:.4f}, BLEU - {bleu:.4f}, Perplexity - {torch.exp(ol).item()}, Accuracy - {accuracy}")

    return total_loss / len(dataloader)

def evaluate(model, val_loader):
    model.eval()
    total_loss = 0

    with torch.no_grad():
        for batch in tqdm(val_loader, desc="Evaluating"):
            input_data, target_data = batch
            output, loss = model(input_data)
            output_dim = output.shape[-1]
            output = output.view(-1, output_dim)
            target_data = target_data.view(-1)
            total_loss += loss.item()

    return total_loss / len(val_loader)

def main(args):
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    tokenizer.add_special_tokens({"eos_token": "<|endoftext|>"})
    train_data = load_dataset(args.dataset, args.datasetconfig, split=args.split, cache_dir=r"D:\Datasets")
    val = load_dataset(args.val_dataset, split="train[:500]", cache_dir=r"D:\Datasets")
    dtype = STRING_TO_DTYPE_MAPPING.get(args.dtype)
    #wandb.init(dir="D:\\Projects\\chatTulu\\", project="Explorer")
    train_data = SENTIADataset(tokenizer, train_data)
    val_data = SENTIADataset(tokenizer, data=val)
    train_loader = DataLoader(train_data, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=args.batch_size)

    config = SENTIAConfig(len(tokenizer), args.d_model, args.d_model, args.n_layer, args.n_head)

    # Initialize the model
    model = SENTIAForCausalLM._from_config(config)
    model.to(args.device, dtype=dtype)
    
    # Define the loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adamax(model.parameters(), lr=args.learning_rate)
    
    # Training and evaluation loops
    try:
        for epoch in range(args.num_epochs):
            print(f'Epoch: {epoch+1:02}')
            train_loss = train(model, train_loader, optimizer, tokenizer, args.device)
            val_loss = evaluate(model, val_loader, criterion)

            print(f'Epoch: {epoch+1:02}')
            print(f'\tTrain Loss: {train_loss:.3f} | Train PPL: {math.exp(train_loss):7.3f}')
            print(f'\tVal Loss: {val_loss:.3f} | Val PPL: {math.exp(val_loss):7.3f}')

            # Calculate and display BLEU, accuracy, and any other desired metrics
            # You'll need to implement this part based on your specific task
    except KeyboardInterrupt:
         print("Saving and cleaning up the model...")
         print("Do NOT kill the terminal it WILL corrupt the model files")
         model.save(args.save_dir)
         quit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Causal Language Model Training')
    # Add your command-line arguments here
    parser.add_argument('--dtype', type=str, default="float32")
    parser.add_argument('--device', type=str, default="cuda")
    parser.add_argument('--momentum', type=str, help="The momentum to use in the RMSProp optim", default=0.5)
    parser.add_argument('--tokenizer', type=str, help="Tokenizer to load from hugging face", default="Locutusque/gpt2-xl-conversational")
    parser.add_argument('--dataset', type=str, help="Dataset to load from hugging face", default="Skylion007/openwebtext")
    parser.add_argument('--datasetconfig', type=str, default=None)
    parser.add_argument('--val_dataset', type=str, default="Skylion007/openwebtext")
    parser.add_argument('--split', type=str, default="train[:250000]")
    parser.add_argument('--learning_rate', type=float, help='Learning rate', default=3e-4)
    parser.add_argument('--save_dir', type=str, default=r'D:\Projects\test')
    parser.add_argument('--batch_size', type=int, default=2)
    parser.add_argument('--d_model', type=int, default=768)
    parser.add_argument('--n_head', type=int, default=16)
    parser.add_argument('--n_layer', type=int, default=12)
    parser.add_argument('--num_epochs', type=int, help='Number of training epochs', default=5)
    args = parser.parse_args()
    
    main(args)
