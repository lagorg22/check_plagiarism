import os
import re
from pathlib import Path

def remove_comments_and_empty_lines(content):
    # Remove single line comments (# and //)
    content = re.sub(r'^\s*#.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*//.*$', '', content, flags=re.MULTILINE)
    
    # Remove C-style multi-line comments (/* */)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    
    # Remove Python triple single-quote docstrings
    content = re.sub(r"'''.*?'''", '', content, flags=re.DOTALL)
    
    # Remove Python triple double-quote docstrings
    content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)
    
    # Split into lines
    lines = content.split('\n')
    
    # Remove empty lines and import statements
    non_empty_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith('import') and not line.startswith('from'):
            non_empty_lines.append(line)
            
    return '\n'.join(non_empty_lines)

def process_files():
    # Define paths
    # Get the root directory (check_plagiarism)
    current_file = Path(__file__)
    root_dir = current_file.parent.parent  # Go up from indexer to check_plagiarism
    
    input_dir = root_dir / 'shared' / 'codefiles'
    output_dir = root_dir / 'shared' / 'processed_codefiles'
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create shared directory if it doesn't exist
    (root_dir / 'shared').mkdir(exist_ok=True)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Keep track of processed files
    processed_count = 0
    empty_files_count = 0
    
    # Process each file in the input directory
    for file_path in input_dir.glob('**/*'):
        if file_path.is_file():
            try:
                # Read the content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Process the content
                processed_content = remove_comments_and_empty_lines(content)
                
                # Skip empty files
                if not processed_content.strip():
                    print(f"Skipping empty file: {file_path}")
                    empty_files_count += 1
                    continue
                
                # Create corresponding output file path
                relative_path = file_path.relative_to(input_dir)
                output_file = output_dir / relative_path
                
                # Create necessary subdirectories
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Write the processed content
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                processed_count += 1
                print(f"Processed: {file_path} -> {output_file}")
                
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
    
    print(f"\nProcessing complete:")
    print(f"- Files processed: {processed_count}")
    print(f"- Empty files skipped: {empty_files_count}")

if __name__ == "__main__":
    process_files()

    # Get all the code files
    