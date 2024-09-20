import argparse
import re

def parse_user_format(user_format):
    log_format_regex = user_format
    log_format_regex = log_format_regex.replace('TIME', r'(?P<time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
    log_format_regex = log_format_regex.replace('LEVEL', r'(?P<level>[A-Z]+)')
    log_format_regex = log_format_regex.replace('MESSAGE', r'(?P<message>.+)')

    try:
        re.compile(log_format_regex)
    except re.error as e:
        raise ValueError(f"Regex format error: {e}. Provided log format: {log_format_regex}")

    return log_format_regex

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

def parse_log_line(line, log_format_regex):
    match = re.match(log_format_regex, line)
    if match:
        return match.groupdict()
    return None

def count_occurrences(pattern=None, severity=None, file_path=None, log_format=None):
    count = 0
    pattern_regex = create_regex(pattern) if pattern else None
    severity_regex = create_regex(severity) if severity else None

    with open(file_path, 'r') as file:
        for line in file:
            line_data = parse_log_line(line.strip(), log_format)

            if not line_data:
                continue

            line_severity = line_data['level']
            cleaned_line = line_data['message']

            if pattern_regex and severity_regex:
                if pattern_regex.search(cleaned_line) and severity_regex.search(line_severity):
                    count += 1
            elif severity_regex:
                if severity_regex.search(line_severity):
                    count += 1
            elif pattern_regex:
                if pattern_regex.search(cleaned_line):
                    count += 1

    return count

def find_first_or_last(pattern=None, severity=None, file_path=None, find_last=False, log_format_regex=None):
    pattern_regex = create_regex(pattern) if pattern else None
    severity_regex = create_regex(severity) if severity else None
    result_line = None

    with open(file_path, 'r') as file:
        lines = file.readlines()
        if find_last:
            lines.reverse()

        for line in lines:
            line = line.strip()
            line_data = parse_log_line(line, log_format_regex) 

            if not line_data:
                continue

            line_severity = line_data['level']
            cleaned_line = line_data['message']

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
    parser.add_argument('--format', help='Log file format (e.g. "TIME LEVEL: MESSAGE")', default='TIME LEVEL: MESSAGE')
    parser.add_argument('log_file', help='The path to the log file')

    args = parser.parse_args()
    pattern = args.text
    severity = args.severity
    log_file = args.log_file
    log_format = args.format

    log_format_regex = parse_user_format(log_format)
    if log_format_regex is None:
        return
    if args.command == 'first':
            result = find_first_or_last(pattern=pattern, severity=severity, file_path=log_file, find_last=False, log_format_regex=log_format_regex)
            print(f'First matching log entry: {result}' if result else "No matching entries found.")
    elif args.command == 'last':
            result = find_first_or_last(pattern=pattern, severity=severity, file_path=log_file, find_last=True, log_format_regex=log_format_regex)
            print(f'Last matching log entry: {result}' if result else "No matching entries found.")
    if args.command == 'count':
        if pattern and severity:
            count_combined = count_occurrences(pattern=pattern, severity=severity, file_path=log_file, log_format=log_format_regex)
            print(f'Matched logs with severity "{severity}" and text "{pattern}": {count_combined}')
        elif pattern:
            count_text = count_occurrences(pattern=pattern, file_path=log_file, log_format=log_format_regex)
            print(f'Matched logs with text "{pattern}": {count_text}')
        elif severity:
            count_severity = count_occurrences(severity=severity, file_path=log_file, log_format=log_format_regex)
            print(f'Matched logs with severity "{severity}": {count_severity}')

if __name__ == '__main__':
    main()
