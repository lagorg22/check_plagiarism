import os
import re
import requests
from pathlib import Path
from tqdm import tqdm

# Code processor API URL
CODE_PROCESSOR_API_URL = "http://localhost:8004/process_batch"

def check_code_processor_api():
    """Check if the code processor API is available."""
    try:
        response = requests.get("http://localhost:8004/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("Successfully connected to code processor API")
            return True
        else:
            print(f"WARNING: Code processor API is not healthy: {response.json()}")
            return False
    except Exception as e:
        print(f"WARNING: Could not connect to code processor API: {str(e)}")
        return False

def process_files_batch(files_dict):
    """Process a batch of files using the code processor API."""
    try:
        # Call the code processor API
        response = requests.post(
            CODE_PROCESSOR_API_URL,
            json={"code_snippets": files_dict},
            headers={"Content-Type": "application/json"},
            timeout=120  # Longer timeout for batch processing
        )
        
        if response.status_code != 200:
            print(f"Error from code processor API: {response.text}")
            raise Exception(f"Code processor API returned status code {response.status_code}")
        
        # Extract processed code from response
        result = response.json()
        return result["processed_snippets"]
    except Exception as e:
        print(f"Error calling code processor API: {str(e)}")
        # If API call fails, return empty dict
        return {}

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
    
    # Check if the code processor API is available
    if not check_code_processor_api():
        print("WARNING: Code processor API is not available. Processing will be done locally.")
        use_api = False
    else:
        use_api = True
    
    # Keep track of processed files
    processed_count = 0
    empty_files_count = 0
    batch_size = 20  # Process files in batches of 20
    
    # Process each file in the input directory
    all_files = list(input_dir.glob('**/*'))
    file_paths = [f for f in all_files if f.is_file()]
    
    print(f"Found {len(file_paths)} files to process")
    
    # Process files in batches
    for i in range(0, len(file_paths), batch_size):
        batch_files = file_paths[i:i + batch_size]
        batch_dict = {}
        
        print(f"\nProcessing batch {i//batch_size + 1}/{(len(file_paths)-1)//batch_size + 1}")
        
        # Read all files in the batch
        for file_path in batch_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():  # Skip empty files
                        batch_dict[str(file_path)] = content
                    else:
                        print(f"Skipping empty file: {file_path}")
                        empty_files_count += 1
            except Exception as e:
                print(f"Error reading {file_path}: {str(e)}")
        
        # Process the batch using the code processor API
        if use_api and batch_dict:
            processed_batch = process_files_batch(batch_dict)
            
            # Write processed content to output files
            for file_path_str, processed_content in processed_batch.items():
                try:
                    file_path = Path(file_path_str)
                    # Skip if processed content is empty
                    if not processed_content.strip():
                        print(f"Skipping empty processed content for: {file_path}")
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
                    print(f"Error saving processed file {file_path}: {str(e)}")
        
        elif not use_api:
            print("API unavailable - please implement local processing fallback if needed")
    
    print(f"\nProcessing complete:")
    print(f"- Files processed: {processed_count}")
    print(f"- Empty files skipped: {empty_files_count}")

if __name__ == "__main__":
    process_files()

    # Get all the code files
    