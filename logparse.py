import argparse
import re

def clean_line(line):
    line = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]+:\s*', '', line)
    line = re.sub(r'[.,!?]*$', '', line)
    return line

def count_occurrences(pattern, file_path):
    count = 0
    if pattern.startswith('*') and not pattern.endswith('*'):
        core_pattern = re.escape(pattern[1:])
        regex = re.compile(rf'{core_pattern}$')
    elif pattern.endswith('*') and not pattern.startswith('*'):
        core_pattern = re.escape(pattern[:-1])
        regex = re.compile(rf'^{core_pattern}')
    elif pattern.startswith('*') and pattern.endswith('*'):
        core_pattern = re.escape(pattern[1:-1])
        regex = re.compile(rf'{core_pattern}')
    else:
        regex = re.compile(rf'^{re.escape(pattern)}$')

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            cleaned_line = clean_line(line)
            if regex.search(cleaned_line):
                count += 1
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
        print(f'Matched logs with "{pattern}": {count}')

if __name__ == '__main__':
    main()
