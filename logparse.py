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
        pattern = f'^{pattern}$'

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

            # Check severity if severity regex is provided
            if severity_regex:
                if not severity.startswith('*') and not severity.endswith('*'):
                    # Check if severity is the only word in the line
                    if line_severity == severity and line_severity == cleaned_line:
                        count += 1
                    continue
                elif severity.startswith('*') and not severity.endswith('*'):
                    # Check if severity ends with specified pattern
                    if re.search(severity_regex.pattern[2:] + '$', line_severity):
                        count += 1
                    continue
                elif severity.endswith('*') and not severity.startswith('*'):
                    # Check if severity starts with specified pattern
                    if re.search('^' + severity_regex.pattern[:-2], line_severity):
                        count += 1
                    continue
                elif severity.startswith('*') and severity.endswith('*'):
                    # Check if severity contains specified pattern
                    if severity_regex.search(line_severity):
                        count += 1
                    continue

            # Check pattern if pattern regex is provided
            if pattern_regex:
                if not pattern.startswith('*') and not pattern.endswith('*'):
                    # Check if pattern is the only word in the line
                    if cleaned_line == pattern and cleaned_line == cleaned_line.split()[0]:
                        count += 1
                    continue
                elif pattern.startswith('*') and not pattern.endswith('*'):
                    # Check if pattern ends with specified pattern
                    if re.search(pattern_regex.pattern[2:] + '$', cleaned_line):
                        count += 1
                    continue
                elif pattern.endswith('*') and not pattern.startswith('*'):
                    # Check if pattern starts with specified pattern
                    if re.search('^' + pattern_regex.pattern[:-2], cleaned_line):
                        count += 1
                    continue
                elif pattern.startswith('*') and pattern.endswith('*'):
                    # Check if pattern contains specified pattern
                    if pattern_regex.search(cleaned_line):
                        count += 1
                    continue

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

        if pattern:
            count_text = count_occurrences(pattern=pattern, file_path=log_file)
            print(f'Matched logs with text "{pattern}": {count_text}')
        if severity:
            count_severity = count_occurrences(pattern=None, severity=severity, file_path=log_file)
            print(f'Matched logs with severity "{severity}": {count_severity}')

if __name__ == '__main__':
    main()
