import argparse
import re

def clean_line(line):
    line = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]+:\s*', '', line)
    return line.strip()

def extract_severity(line):
    match = re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} ([A-Z]+):', line)
    return match.group(1) if match else ''

def create_regex(pattern):
    if pattern is None:
        return None
    
    if pattern.startswith('*') and pattern.endswith('*'):
        pattern = pattern.replace('*', '.*')
    elif pattern.startswith('*'):
        pattern = '.*' + pattern[1:]
    elif pattern.endswith('*'):
        pattern = pattern[:-1] + '.*'
    else:
        pattern = pattern
    return re.compile(pattern)

def count_occurrences(pattern=None, severity=None, file_path=None):
    count = 0
    pattern_regex = create_regex(pattern) if pattern else None
    severity_regex = create_regex(severity) if severity else None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            line_severity = extract_severity(line)
            cleaned_line = clean_line(line)
            
            if severity_regex and not severity_regex.match(line_severity):
                continue
            
            if pattern_regex:
                if pattern.startswith('*') and not pattern.endswith('*'):
                    if not re.search(pattern_regex.pattern[2:] + '$', cleaned_line):
                        continue
                elif pattern.endswith('*') and not pattern.startswith('*'):
                    if not re.search('^' + pattern_regex.pattern[:-2], cleaned_line):
                        continue
                elif pattern.startswith('*') and pattern.endswith('*'):
                    if not pattern_regex.search(cleaned_line):
                        continue
                else:
                    if not pattern_regex.search(cleaned_line):
                        continue
            
            count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description="Counts a specific pattern in the log file.")
    parser.add_argument('command', choices=['count'], help='The action you want to perform')
    parser.add_argument('--text', help='The text or pattern you want to search for')
    parser.add_argument('--severity', help='The severity level you want to search for')
    parser.add_argument('log_file', help='The path to the log file')

    args = parser.parse_args()
    if args.command == 'count':
        pattern = args.text
        severity = args.severity
        log_file = args.log_file
        count = count_occurrences(pattern, severity, log_file)
        if pattern:
            print(f'Matched logs with text "{pattern}": {count}')
        if severity:
            print(f'Matched logs with severity "{severity}": {count}')

if __name__ == '__main__':
    main()
