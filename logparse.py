import argparse
import re

def clean_line(line):
    line = re.sub(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]+:\s*', '', line)
    return line.strip()

def extract_severity(line):
    match = re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} ([A-Z]+):', line)
    return match.group(1) if match else ''

def count_occurrences(pattern=None, severity=None, file_path=None):
    count = 0
    if pattern:
        pattern = pattern.replace('*', '.*')
        regex = re.compile(pattern)
    else:
        regex = None

    if severity:
        severity = severity.replace('*', '.*')
        severity_regex = re.compile(severity)
    else:
        severity_regex = None

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            line_severity = extract_severity(line)
            
            if severity_regex and severity_regex.match(line_severity):
                if not regex:
                    count += 1
                elif regex.search(clean_line(line)):
                    count += 1
            elif not severity_regex and regex:
                if regex.search(clean_line(line)):
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
