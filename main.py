from generation import autoGenerator
from testing import differential

def main():
    snippets = []

    with open('prompt.txt', 'r') as prompt_file:
        prompt_structure = prompt_file.read()

    with open('data.txt', 'r') as api_file:
        api_signatures = api_file.readlines()

    for api_signature in api_signatures:
        api_signature = api_signature.strip()
        prompt = prompt_structure.format(api_signature)
        snippet = autoGenerator.gpt_generate_snippet(prompt)
        if autoGenerator.validate_snippet(snippet):
            differential.test_snippet(snippet)
            snippets.append(snippet)
        print("-----------------------------------------------------------------")

if __name__ == "__main__":
    main()
