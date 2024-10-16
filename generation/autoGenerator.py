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
def get_snippet(prompt, seed):
    snippet = client.chat.completions.create(
        model="gpt-4o",
        top_p=0.95,
        max_completion_tokens=256,
        temperature=0.4,
        seed = seed,
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return snippet['choices'][0]['message']['content']

def get_snippets(prompt, num_snippets=5):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_snippet, prompt, seed=i) for i in range(1, num_snippets + 1)]
        snippets = []
        for future in as_completed(futures):
            snippets.append(future.result())
    return snippets

def clean_snippet(snippet):
    clean = []
    for line in snippet.splitlines():
        line = re.sub(r'#.*', '', line).rstrip()
        if line.startswith('```'):
            continue
        if line.strip():
            clean.append(line)
    return '\n'.join(clean)

def validate_snippet(snippet):
    env = {}
    try:
        exec(snippet, env)
        return True
    except Exception as e:
        print(f"Snippet failed with error: {e}")
        return False


