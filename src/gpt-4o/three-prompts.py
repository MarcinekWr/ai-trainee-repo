import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version=os.getenv("API_VERSION"),
    azure_endpoint=os.getenv("API_BASE"),
)

deployment = "gpt-4o"
log_path = os.path.abspath("logs/usage.md")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

prompts = [
    "Dlaczego używa się Azure AI?",
    "Jakie są trzy najważniejsze trendy technologiczne w 2025 roku?",
    "Powiedź mi coś o Politechnice Wrocławskiej."
]

def log(index, prompt, reply, usage, cost):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"### Prompt {index+1}\n")
        f.write(f"**Prompt:** {prompt}\n")
        f.write(f"**Response:** {reply}\n")
        f.write(f"**Tokens in:** {usage.prompt_tokens}\n")
        f.write(f"**Tokens out:** {usage.completion_tokens}\n")
        f.write(f"**Total tokens:** {usage.total_tokens}\n")
        f.write(f"**Cost:** ${cost:.4f}\n")
        f.write(f"**Date:** {datetime.now().isoformat()}\n\n")


results = []

for i, prompt in enumerate(prompts):
    completion = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}]
    )

    reply = completion.choices[0].message.content
    usage = completion.usage
    cost = (usage.prompt_tokens / 1000 * 0.005) + (usage.completion_tokens / 1000 * 0.015)

    log(i, prompt, reply, usage, cost)
    results.append((usage, cost))
    print(f"Prompt {i+1} zapisany — koszt: ${cost:.4f}")

efficiencies = [(i, usage.prompt_tokens + usage.completion_tokens, cost) for i, (usage, cost) in enumerate(results)]
best = min(efficiencies, key=lambda x: x[2])
print(f"\nNajbardziej efektywny prompt względem kosztu: Prompt {best[0] + 1} — koszt: ${best[2]:.4f}")
