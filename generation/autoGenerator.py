from dotenv import load_dotenv
from openai import OpenAI
import os
import anthropic
import sys
import traceback
import re

load_dotenv()
claude_client = anthropic.Anthropic(
    api_key = os.getenv('ANTHROPIC_API_KEY')
)

gpt_client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))

def gpt_generate_snippet(prompt):
    completion = gpt_client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": "You are an expert in Python and PyTorch."},
            {"role": "user", "content": prompt}
        ]
    )
    return clean_snippet(completion.choices[0].message.content)

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


