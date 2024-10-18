import os
import re
import time

from openai import OpenAI
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from data import fitness_score as fitness

load_dotenv()

client = OpenAI(
  api_key = os.getenv('OPENAI_API_KEY')
)

# Function to generate a code snippet using the OpenAI python SDK
def get_snippet(prompt, n):
    snippets = []
    messages=[
            {"role": "system", "content": "You are an expert in Python and PyTorch, only respond with code and no comments"},
            {"role": "user", "content": prompt}
    ]
    start_time = time.time()
    while len(snippets) < n:
        if time.time() - start_time > 15:
            print("Time limit reached. Stopping snippet generation.")
            break
        response = client.chat.completions.create(
            model="gpt-4o",
            top_p=0.95,
            max_completion_tokens=128,
            temperature=0.4,
            messages=messages
        )
        snippet = clean_snippet(response.choices[0].message.content)
        print(f"Fitness score: {fitness.calculate_dataflow_depth(snippet)}")
        print(snippet) 
        print("------------------\n")
        is_valid, error_message = validate_snippet(snippet)
        if is_valid:
            snippets.append(snippet)
            messages.append({"role": "assistant", "content": snippet})
            messages.append({"role": "user", "content": f"{prompt}\nGenerate a new variation in terms of input data, tensor size/dimension, and api parameters"})
        else:
            messages.append({"role": "assistant", "content": snippet})
            messages.append({"role": "user", "content": f"{prompt}\nThe previous response encountered the error below:\n{error_message}"})
    return snippets

def clean_snippet(snippet):
    cleaned = re.sub(r"```python|```", "", snippet)
    cleaned = "\n".join(
        line for line in cleaned.splitlines() 
        if not re.match(r"^\s*print\(", line) and not re.match(r"^\s*#", line)
    )
    cleaned = cleaned.strip()
    return cleaned

def validate_snippet(snippet):
    env = {}
    try:
        exec(snippet, env)
        return True, ""
    except Exception as e:
        print(f"Snippet failed with error: {e}")
        return False, str(e)


