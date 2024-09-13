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
        pattern = '.*' + re.escape(pattern[1:-1]) + '.*'
    elif pattern.startswith('*'):
        pattern = '.*' + re.escape(pattern[1:])
    elif pattern.endswith('*'):
        pattern = re.escape(pattern[:-1]) + '.*'
    else:
        pattern = f'^{re.escape(pattern)}$'
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

            if pattern_regex and severity_regex:
                if check_pattern_match(pattern, cleaned_line) and check_pattern_match(severity, line_severity):
                    count += 1
                continue

            if severity_regex:
                if check_pattern_match(severity, line_severity):
                    count += 1
                continue

            if pattern_regex:
                if check_pattern_match(pattern, cleaned_line):
                    count += 1
                continue

    return count

def check_pattern_match(pattern, line):
    if not pattern.startswith('*') and not pattern.endswith('*'):
        return pattern == line

    if pattern.startswith('*') and not pattern.endswith('*'):
        return line.endswith(pattern[1:])

    if pattern.endswith('*') and not pattern.startswith('*'):
        return line.startswith(pattern[:-1])

    if pattern.startswith('*') and pattern.endswith('*'):
        return pattern[1:-1] in line

    return False

def main():
    parser = argparse.ArgumentParser(description="Counts a specific pattern and/or severity in the log file.")
    parser.add_argument('command', choices=['count'], help='The action you want to perform')
    parser.add_argument('--text', help='The text or pattern you want to search for')
    parser.add_argument('--severity', help='The severity level you want to search for')
    parser.add_argument('log_file', help='The path to the log file')

    args = parser.parse_args()

    if args.command == 'count':
        pattern = args.text
        severity = args.severity
        log_file = args.log_file

        if pattern and severity:
            count_combined = count_occurrences(pattern=pattern, severity=severity, file_path=log_file)
            print(f'Matched logs with severity "{severity}" and text "{pattern}": {count_combined}')
        elif pattern:
            count_text = count_occurrences(pattern=pattern, file_path=log_file)
            print(f'Matched logs with text "{pattern}": {count_text}')
        elif severity:
            count_severity = count_occurrences(severity=severity, file_path=log_file)
            print(f'Matched logs with severity "{severity}": {count_severity}')

if __name__ == '__main__':
    main()
