import argparse
import re

def validate_log_format(log_format):
    expected_format_regex = r'^%Y-%m-%d %H:%M:%S %LEVEL: %MESSAGE$'
    return re.match(expected_format_regex, log_format)

def parse_log_format(log_format):
    log_format_regex = log_format.replace('%MESSAGE', r'(?P<message>.+)')
    log_format_regex = log_format_regex.replace('%Y', r'(?P<year>\d{4})')
    log_format_regex = log_format_regex.replace('%m', r'(?P<month>\d{2})')
    log_format_regex = log_format_regex.replace('%d', r'(?P<day>\d{2})')
    log_format_regex = log_format_regex.replace('%H', r'(?P<hour>\d{2})')
    log_format_regex = log_format_regex.replace('%M', r'(?P<minute>\d{2})')
    log_format_regex = log_format_regex.replace('%S', r'(?P<second>\d{2})')
    log_format_regex = log_format_regex.replace('%LEVEL', r'(?P<level>[A-Z]+)')

    try:
        re.compile(log_format_regex)
    except re.error as e:
        print(f"Regex format error: {e}")
        print(f"Provided log format: {log_format_regex}")
        return None

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
    parser.add_argument('--format', help='Log file format (e.g. "%Y-%m-%d %H:%M:%S %LEVEL: %MESSAGE")', default='%Y-%m-%d %H:%M:%S %LEVEL: %MESSAGE')
    parser.add_argument('log_file', help='The path to the log file')

    args = parser.parse_args()
    pattern = args.text
    severity = args.severity
    log_file = args.log_file
    log_format = args.format

    if log_format and not validate_log_format(log_format):
        print(f"Hata: Geçersiz format. Doğru format: '%Y-%m-%d %H:%M:%S %LEVEL: %MESSAGE'")
        return

    log_format_regex = parse_log_format(log_format)
    if log_format_regex is None:
        return

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
    elif args.command == 'first':
        result = find_first_or_last(pattern=pattern, severity=severity, file_path=log_file, find_last=False)
        print(f'First matching log entry: {result}' if result else "No matching entries found.")
    elif args.command == 'last':
        result = find_first_or_last(pattern=pattern, severity=severity, file_path=log_file, find_last=True)
        print(f'Last matching log entry: {result}' if result else "No matching entries found.")

if __name__ == '__main__':
    main()
