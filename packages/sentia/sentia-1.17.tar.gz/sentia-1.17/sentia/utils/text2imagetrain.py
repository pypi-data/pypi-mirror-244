import argparse
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, CLIPTextModel
from torchvision import transforms
from PIL import Image
from sentia.modeling_sentia import SENTIAConfig, SENTIAForImageGeneration
import requests
from io import BytesIO
from datasets import load_dataset
import matplotlib.pyplot as plt

torch.cuda.set_per_process_memory_fraction(1.0)
torch.manual_seed(1024)
torch.cuda.manual_seed(1024)
# Define your custom dataset
class CustomImageTextDataset(Dataset):
    def __init__(self, tokenizer, data, transform=None):
        self.tokenizer = tokenizer
        self.data = data
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item['prompt']
        image_path = item['image']

        # Load and preprocess the image
        if isinstance(image_path, str):
            if image_path.startswith("http"):
                response = requests.get(image_path)
                image = Image.open(BytesIO(response.content))
            else:
                image = Image.open(image_path)
        else:
            image = image_path

        if self.transform:
            image = self.transform(image).to("cuda", dtype=torch.float16)

        # Tokenize the text
        inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', max_length=256, truncation=True)

        return {
            'input_ids': inputs['input_ids'].to("cuda"),
            'labels': image
        }


def train(args):
    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.pretrained_model)
    config = SENTIAConfig(len(tokenizer), args.hidden_dim, n_embed=args.embedding_dim, n_layer=args.num_layers, n_head=args.num_heads, pad_token_id=tokenizer.pad_token_id, cross_attention=True)
    model = SENTIAForImageGeneration(config, discriminator=None, add_latent=False, discriminator_weight=0.5)
    model.summary()
    model.to("cuda", dtype=torch.float16)
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-3, fused=True, eps=1e-4)
    # Define the dataset with image URLs and text data
    data = load_dataset("poloclub/diffusiondb", "2m_first_1k", split="train[:1]")
    # Define the dataset and dataloader
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
    ])

    dataset = CustomImageTextDataset(tokenizer, data, transform=transform)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

    # Training loop (remaining part remains the same)
    for epoch in range(args.num_epochs):
        model.train()
        total_loss = 0

        for i, batch in enumerate(dataloader):

            optimizer.zero_grad()
            input_ids = batch["input_ids"].cuda()
            labels = batch["labels"].cuda()
            outputs = model.forward(input_ids=input_ids, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            print(f"Batch {i}/{len(dataloader)} - Loss: {loss.item()}")

            total_loss += loss.item()

    average_loss = total_loss / len(dataloader)
    print(f'Epoch [{epoch + 1}/{args.num_epochs}] Loss: {average_loss:.4f}')
    generated_image = generate_image(model, input_ids)
    print(generated_image)
    image = Image.fromarray((generated_image * 255).astype("uint8"), mode="RGB")
    image.save("/media/sebastian/T7/Projects/test/image.png")
def generate_image(model, input_ids, num_steps=100):
    # Initial image generation
    with torch.no_grad():
        input_ids = model.encoder.embed_tokens(input_ids.squeeze(0))
        for module in model.encoder.encoder_layers:
            outputs = module(input_ids=input_ids, use_cache=False)
            input_ids = outputs[0]

    # Get the initial image
    generated_image = torch.rand(input_ids.size(0), 3, 512, 512, device=input_ids.device) * (255 -1) + 1
    attention_mask = torch.ones(input_ids.size(0), 1, 256, 256, device=input_ids.device, dtype=torch.bool)

    # Set the model to evaluation mode
    model.eval()

    # Perform multiple iteration steps
    for _ in range(num_steps):
        # Generate image for the current step
        with torch.no_grad():
            outputs = model(inputs_embeds=input_ids, labels=generated_image, encoder_outputs=input_ids, attention_mask=attention_mask).image_outputs[0, 0, 0, :].view(1, 3, 512, 512)

        # Update the generated image
        generated_image = outputs
    return generated_image.squeeze(0).permute(1, 2, 0).detach().cpu().numpy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pretrained_model', type=str, default='Locutusque/gpt2-xl-conversational')
    parser.add_argument('--hidden_dim', type=int, default=768)
    parser.add_argument('--embedding_dim', type=int, default=768)
    parser.add_argument('--num_layers', type=int, default=18)
    parser.add_argument('--num_heads', type=int, default=32)
    parser.add_argument('--batch_size', type=int, default=1)
    parser.add_argument('--num_epochs', type=int, default=120)

    args = parser.parse_args()
    train(args)
