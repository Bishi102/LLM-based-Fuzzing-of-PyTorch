import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def gpt_generate_snippet(prompt):
    chat_history = []
    gpt_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    for attempt in range(5):
        chat_history.append({"role": "user", "content": prompt})
        try:
            completion = gpt_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=chat_history
            )
            snippet = clean_snippet(completion.choices[0].message.content)
            if validate_snippet(snippet):
                return snippet
            print(snippet)
            chat_history.append({"role": "assistant", "content": f"The code generated does not run due to the following issue."})
        except Exception as e:
            print(f"Exception occurred during snippet generation: {e}")
        prompt = f"The code generated does not run due to the following issue. Please try again with the same prompt: \n{prompt}"
        chat_history.append({"role": "user", "content": prompt})

    print("Failed to generate a valid snippet after multiple attempts.")
    return snippet

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


