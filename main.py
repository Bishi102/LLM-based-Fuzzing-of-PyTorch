

from data import api_scraper as scraper
from generation import autoGenerator as gen
from testing import differential as dif

def main():
    
    api_signatures = scraper.get_sample_100()

    with open('api_signatures.txt', 'r') as file:
        api_signatures = [line.strip() for line in file.readlines()]

    for i, signature in enumerate(api_signatures):
        prompt = f"""
        Task 1: import torch
        Task 2: Generate input data
        Task 3: Call the API {i}
        """
        snippets = gen.get_snippet(prompt, 5)
            


if __name__ == "__main__":
    main()
