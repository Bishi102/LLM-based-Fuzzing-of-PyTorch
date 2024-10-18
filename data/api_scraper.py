import re
import sys
import random

from io import StringIO

def extract_sig(api_name):
    
    buffer = StringIO()
    sys.stdout = buffer

    try:
        help(api_name)
    except Exception:
        sys.stdout = sys.__stdout__
        return None
    sys.stdout = sys.__stdout__

    help_output = buffer.getvalue()
    first_five_lines = help_output.splitlines()[:5] # observed: api signature occurs in first 5 lines 
    api_base = api_name.split('.')[-1]
    occurrences = [line for line in first_five_lines if f"{api_base}(" in line]

    if len(occurrences) >= 2:
        chosen_line_index = first_five_lines.index(occurrences[1])
    elif len(occurrences) == 1:
        chosen_line_index = first_five_lines.index(occurrences[0])
    else:
        return ''

    lines_to_search = first_five_lines[chosen_line_index:]
    signature = ''
    counter = 0
    found_opening_paren = False

    for line in lines_to_search:
        for char in line:
            if char == '(':
                counter += 1
                found_opening_paren = True
            elif char == ')':
                counter -= 1
            if found_opening_paren:
                signature += char
            if found_opening_paren and counter == 0: 
                break
        if found_opening_paren and counter == 0:
            break
    if signature.startswith('(') and signature.endswith(')'):
        signature = signature[1:-1].strip()
    if signature == '' or signature == '...':
        return ''
    return signature if signature else ''

# Function to read the file containing the list of APIs
def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Function to write the extracted signatures to an output file
def write_file(output_file, api_signatures):
    with open(output_file, 'w') as file:
        for api, signature in api_signatures:
            file.write(f"{api}({signature})\n")

# 100 api signatures from titanfuzz list
def get_sample_100():
    api_list = read_file('api_list.txt')
    api_signatures = []
    random_apis = random.sample(api_list, 100)
    for api in random_apis:
        try:
            signature = extract_sig(api)
            api_signatures.append((api, signature))
        except Exception as e:
            print(f"Error while fetching help for {api}: {e}")
    write_file('api_signatures.txt', api_signatures)