import itertools
import re
import string
from typing import Pattern
import whois
import argparse
import concurrent.futures
# Define the command line argument parser
parser = argparse.ArgumentParser(description='Find available domain names that match a given pattern')
parser.add_argument('pattern', type=str, help='Regular expression pattern for domain names')
parser.add_argument('tld', type=str, help='domain extension name (.com)')
parser.add_argument('output_file', type=str, help='Name of output file')
args = parser.parse_args()

# Get the regular expression pattern and output file name from the command line arguments
pattern = args.pattern
regex = re.compile(args.pattern)
tldpattern = r'^[a-zA-Z]{2,5}$'
tld = args.tld
if not re.match(tldpattern, tld):
    exit("tld name should be like  (com|ma|net)")
output_file = args.output_file
legal_chars = string.ascii_lowercase + string.digits + '-'
def get_max_length(pattern, legal_chars):
    # Find the longest substring of legal characters in the pattern
    matches = re.findall(r'[' + legal_chars + r']+', pattern)
    if matches:
        longest_match = max(matches, key=len)
        return len(longest_match)
    else:
        return 0
max_length = get_max_length(pattern, legal_chars)
def generate_combinations(regex:Pattern, legal_chars, tld, max_length):
    # Generate all possible combinations of legal characters up to the maximum length
    all_possible_names = []
    for i in range(2, max_length + 1):
        for name in itertools.product(legal_chars, repeat=i):
            all_possible_names.append(''.join(name))
    def check_pattern(name):
        _match = regex.match(name)
        if _match:
           return _match.string
    return [f'{name}.{tld}' for name in all_possible_names if check_pattern(name)]
# Generate a list of possible domain names
# domain_names = [f'{c1}{c2}.ma' for c1 in 'abcdefghijklmnopqrstuvwxyz' for c2 in 'abcdefghijklmnopqrstuvwxyz']
domain_names = generate_combinations(regex, legal_chars, tld, max_length)
# test  " r'^[a-zA-Z]{2}\.ma$' "
# Check if each domain name is available
available_domains = []
def is_registered(domain_name):
    """
    A function that returns a boolean indicating 
    whether a `domain_name` is registered
    """
    try:
        w = whois.query(domain_name)
        # print(w.registrant)
    except Exception:
        return None
    else:
        return w.name
with concurrent.futures.ThreadPoolExecutor(10) as executor:
       # Define a function to check if each name matches the pattern
       
       # Submit each name to the executor to check if it matches the pattern
       futures = [executor.submit(is_registered, name) for name in domain_names]
       # Collect the results of the futures and add each name that matches the pattern to the filtered list
       for future in concurrent.futures.as_completed(futures):
           if future.result():
               available_domains.append(future.result())

# Find the domain names that match the pattern
# matching_domains = [d for d in available_domains if re.match(pattern, d)]

# Write the results to the output file
with open(output_file, 'w') as f:
    f.write(f'The following domain names are available and match the pattern {pattern}:\n')
    for domain in available_domains:
        f.write(domain + '\n')

# Print a message indicating the output file name
print(f'The results have been written to {output_file}')
