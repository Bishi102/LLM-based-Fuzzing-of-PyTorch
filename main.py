

from data import api_scraper as scraper
from generation import autoGenerator as gen
from testing import differential as dif

def main():
    api_list = scraper.read_file('api_list.txt')
    api_signatures = []
    for api in api_list:
        try:
            signature = scraper.extract_sig(api)
            api_signatures.append((api, signature))
        except Exception as e:
            print(f"Error while fetching help for {api}: {e}")
            
    scraper.write_file('api_signatures.txt', api_signatures)
    print("API signatures written to 'api_signatures_output.txt'.")
    prompt = """
Task 1: import torch
Task 2: Generate input data
Task 3: Call the API torch.meshgrid(*tensors, indexing: Optional[str] = None)
"""
    snippets = gen.get_snippet(prompt, 5)
    print(snippets[0])
    print(snippets[1])
    print(snippets[2])
    print(snippets[3])
    print(snippets[4])
    

if __name__ == "__main__":
    main()
