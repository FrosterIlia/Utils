import argparse
from pathlib import Path

FILE_EXTENSIONS = ['.py', '.c', '.h', '.cpp', '.ino']
EXCLUDE_FOLDERS = ['venv', '.venv', '.pio']
FILE_NAMES_EXCLUDE = []


def count_lines_in_file(file_path):
    with file_path.open('r', encoding='utf-8', errors='ignore') as file:
        return sum(1 for _ in file)

def main():
    parser = argparse.ArgumentParser(description="Count lines in .py, .c, .h, and .cpp files.")
    parser.add_argument('folder', type=str, help='Path to the folder to scan for source code files.')
    parser.add_argument(
        '--folders_exclude', '-e',
        action='append',
        nargs='+', # Accepting multiple arguments
        default=[],
        help='Additional folder names to exclude'
    )
    parser.add_argument(
        '--file_ext', '-f',
        action='append',
        nargs='+', # Accepting multiple arguments
        default=[],
        help='Additional file extensions to count'
    )
    
    parser.add_argument(
        '--file_names_exclude', '-fn',
        action='append',
        nargs='+', # Accepting multiple arguments
        default=[],
        help='Additional file names to exclude'
    )
    
    args = parser.parse_args()
    
    exclude_folders = EXCLUDE_FOLDERS
    file_extensions = FILE_EXTENSIONS
    file_names_exclude = FILE_NAMES_EXCLUDE
    
    if args.folders_exclude:
        exclude_folders = EXCLUDE_FOLDERS + args.folders_exclude[0] # Adding custom exclude folders names
    if args.file_ext:
        file_extensions = FILE_EXTENSIONS + args.file_ext[0] # Adding custom file extensions
    if args.file_names_exclude:
        file_names_exclude = FILE_NAMES_EXCLUDE + args.file_names_exclude[0] # Adding custon file names to exclude
        
    folder_path = Path(args.folder)
    
    total_lines = 0
    file_line_counts = {}

    for file_path in folder_path.rglob('*'):
        if any(part in exclude_folders for part in file_path.parts):
            continue
        
        if file_path.suffix in file_extensions and file_path.name not in file_names_exclude:
            line_count = count_lines_in_file(file_path)
            total_lines += line_count
            file_line_counts[str(file_path)] = line_count

    for file, line_count in file_line_counts.items():
        print(f'{file}: {line_count} lines')

    print(f'Total lines in all files: {total_lines}')

if __name__ == "__main__":
    main()
