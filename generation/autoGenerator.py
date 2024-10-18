import os
import re

from openai import OpenAI
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

client = OpenAI(
  api_key = os.getenv('OPENAI_API_KEY')
)

# Function to generate a code snippet using the OpenAI API
def get_snippet(prompt, n):
    snippets = []
    messages=[
            {"role": "system", "content": "You are an expert in Python and PyTorch, only respond with code and no comments"},
            {"role": "user", "content": prompt}
    ]
    for i in range(n):
        response = client.chat.completions.create(
            model="gpt-4o",
            top_p=0.95,
            temperature=0.4,
            # max_completion_tokens=128,
            messages=messages
        )
        snippet = clean_snippet(response.choices[0].message.content)
        snippets.append(snippet)
        messages.append({"role": "assistant", "content": snippet})
        messages.append({"role": "user", "content": f"{prompt}\nGenerate a new variation in terms of input data, tensor size/dimension, and api parameters"})
    return snippets

#unused func right now
def get_snippets(prompt, num_snippets=5):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_snippet, prompt, seed=i*420) for i in range(1, num_snippets + 1)]
        snippets = []
        for future in as_completed(futures):
            snippets.append(future.result())
    return snippets

def clean_snippet(snippet):
    cleaned = re.sub(r"```python|```", "", snippet)
    cleaned = "\n".join(
        line for line in cleaned.splitlines() if not re.match(r"^\s*print\(", line)
    )
    cleaned = cleaned.strip()
    return cleaned
#review this
def validate_snippet(snippet):
    env = {}
    try:
        exec(snippet, env)
        return True
    except Exception as e:
        print(f"Snippet failed with error: {e}")
        return False


