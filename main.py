from generation import autoGenerator
from testing import differential

import re
from io import StringIO
import sys

def extract_signature(api_name):
    buffer = StringIO()
    sys.stdout = buffer
    try:
        help(api_name)
    except Exception:
        sys.stdout = sys.__stdout__
        return None
    sys.stdout = sys.__stdout__


    help_output = buffer.getvalue()
    first_five_lines = '\n'.join(help_output.splitlines()[:5])

    api_base = api_name.split('.')[-1]
    abbreviated_pattern = rf"{api_base}\(.*?\)"

    matches = re.findall(abbreviated_pattern, first_five_lines)
    if matches:
        if len(matches) >= 2:
            return matches[1]
        else:
            return matches[0]
    return None

def read_apis_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

def write_signatures_to_file(output_file, api_signatures):
    with open(output_file, 'w') as file:
        for api, signature in api_signatures:
            if signature:
                file.write(f"{api}({signature})\n")
            else:
                file.write(f"{api} (No signature found)\n")

def main():
    api_list = read_apis_from_file('test_data.txt')
    api_signatures = []
    for api in api_list:
        try:
            signature = extract_signature(api)
            api_signatures.append((api, signature))
        except Exception as e:
            print(f"Error while fetching help for {api}: {e}")
            
    write_signatures_to_file('api_signatures_output.txt', api_signatures)
    print("API signatures written to 'api_signatures_output.txt'.")

if __name__ == "__main__":
    main()
