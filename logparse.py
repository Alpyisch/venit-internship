import argparse
import re

def count_occurrences(pattern, file_path):
    count = 0
    if '*' in pattern:
        pattern = pattern.replace('*', '.*')
    regex = re.compile(pattern)
    with open(file_path, 'r') as file:
        for line in file:
            matches = regex.findall(line)
            count += len(matches)
    return count

def main():
    parser = argparse.ArgumentParser(description="Counts a specific pattern in the log file.")
    parser.add_argument('command', choices=['count'], help='The action you want to perform')
    parser.add_argument('--text', required=True, help='The text or pattern you want to search for')
    parser.add_argument('log_file', help='The path to the log file')

    args = parser.parse_args()

    if args.command == 'count':
        pattern = args.text
        log_file = args.log_file
        count = count_occurrences(pattern, log_file)
        print(f'Matched logs with "{pattern}": {count}') #pattern regexleri saptamak için kullandığımız terim

if __name__ == '__main__':
    main()
