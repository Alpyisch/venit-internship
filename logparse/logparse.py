import argparse
import re
from datetime import datetime

def parse_log_line(line, log_format):
    log_format = log_format.replace('%Y', r'(?P<year>\d{4})')
    log_format = log_format.replace('%m', r'(?P<month>\d{2})')
    log_format = log_format.replace('%d', r'(?P<day>\d{2})')
    log_format = log_format.replace('%H', r'(?P<hour>\d{2})')
    log_format = log_format.replace('%M', r'(?P<minute>\d{2})')
    log_format = log_format.replace('%S', r'(?P<second>\d{2})')
    log_format = log_format.replace('%LEVEL', r'(?P<level>[A-Z]+)')
    log_format = log_format.replace('%MESSAGE', r'(?P<message>.+)')

    log_regex = re.compile(log_format)

    match = log_regex.match(line)
    if match:
        return {
            'timestamp': datetime(
                int(match.group('year')),
                int(match.group('month')),
                int(match.group('day')),
                int(match.group('hour')),
                int(match.group('minute')),
                int(match.group('second'))
            ),
            'level': match.group('level'),
            'message': match.group('message').strip()
        }
    return None

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
        pattern = '.*' + re.escape(pattern[1:]) + '$'
    elif pattern.endswith('*'):
        pattern = '^' + re.escape(pattern[:-1]) + '.*'
    else:
        pattern = '^' + re.escape(pattern) + '$'
        
    return re.compile(pattern)

def check_pattern_match(pattern, line):
    if not pattern.startswith('*') and not pattern.endswith('*'):
        return pattern == line

    if not pattern.startswith('*') and pattern.endswith('*'):
        return line.endswith(pattern[:-1])

    if pattern.startswith('*') and not pattern.endswith('*'):
        return line.startswith(pattern[1:])

    if pattern.startswith('*') and pattern.endswith('*'):
        return pattern[1:-1] in line

    return False

def count_occurrences(pattern=None, severity=None, file_path=None, log_format=None):
    count = 0
    pattern_regex = create_regex(pattern) if pattern else None
    severity_regex = create_regex(severity) if severity else None

    with open(file_path, 'r') as file:
        for line in file:
            line_data = parse_log_line(line, log_format)

            if not line_data:
                continue

            line_severity = line_data['level']
            cleaned_line = line_data['message']

            if pattern_regex and severity_regex:
                if pattern_regex.search(cleaned_line) and severity_regex.search(line_severity):
                    count += 1
                continue

            if severity_regex:
                if severity_regex.search(line_severity):
                    count += 1
                continue

            if pattern_regex:
                if pattern_regex.search(cleaned_line):
                    count += 1
                continue

    return count


def find_first_or_last(pattern=None, severity=None, file_path=None, find_last=False):
    pattern_regex = create_regex(pattern) if pattern else None
    severity_regex = create_regex(severity) if severity else None

    result_line = None

    with open(file_path, 'r') as file:
        lines = file.readlines()

        if find_last:
            lines.reverse()

        for line in lines:
            line = line.strip()
            line_severity = extract_severity(line)
            cleaned_line = clean_line(line)

            if pattern_regex and severity_regex:
                if pattern_regex.search(cleaned_line) and severity_regex.search(line_severity):
                    result_line = line
                    break

            elif severity_regex:
                if severity_regex.search(line_severity):
                    result_line = line
                    break

            elif pattern_regex:
                if pattern_regex.search(cleaned_line):
                    result_line = line
                    break

    return result_line


def main():
    parser = argparse.ArgumentParser(description="Counts or finds specific patterns in the log file.")
    parser.add_argument('command', choices=['count', 'first', 'last'], help='The action you want to perform')
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
    elif args.command == 'first':
        result = find_first_or_last(pattern=args.text, severity=args.severity, file_path=args.log_file, find_last=False)
        print(f'First matched log: {result}')
    elif args.command == 'last':
        result = find_first_or_last(pattern=args.text, severity=args.severity, file_path=args.log_file, find_last=True)
        print(f'Last matched log: {result}')

if __name__ == '__main__':
    main()