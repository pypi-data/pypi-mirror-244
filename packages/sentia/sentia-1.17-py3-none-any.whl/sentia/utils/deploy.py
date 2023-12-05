import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('Locutusque/gpt2-xl-conversational')
model = AutoModelForCausalLM.from_pretrained("Locutusque/gpt2-xl-conversational", torch_dtype=torch.float16)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
def generate_text(model, prompt, tokenizer, temperature=0.1, top_p=0.14, top_k=35, max_length=256, stop_tokens=["</s>"]):
    stop_tokens = stop_tokens
    prompt = f'<|USER|> {prompt} <|ASSISTANT|> '
    index = len(prompt)
    input_ids = tokenizer(prompt, add_special_tokens=True, max_length=512, truncation=True, return_tensors="pt", return_attention_mask=True).to(device=model.device)
    output = model.generate(input_ids["input_ids"], do_sample=True, temperature=temperature, top_p=top_p, top_k=top_k, repetition_penalty=1.176, max_length=max_length, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id)
    output_ids = tokenizer.decode(output[0], skip_special_tokens=False)
    #output_ids = output_ids[index:]
    for token in stop_tokens:
        if token in output_ids:
            output_ids = output_ids.split(token)[0]
            break
    return output_ids
# Loop to interact with the model
while True:
    prompt = input("Enter a prompt (or 'q' to quit): ")
    if prompt == "q":
        break
    output_text = generate_text(model, prompt, tokenizer, max_length=256)
    print(output_text)

