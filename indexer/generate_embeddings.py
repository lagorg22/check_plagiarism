'''
This script generates embeddings for processed code files using the embedding API.
The embeddings are then indexed using FAISS and saved to disk.
Now uses the embedding_api service instead of loading the model directly.
'''

import os
import glob
import faiss
import numpy as np
import json
import requests
from pathlib import Path
from tqdm import tqdm
from typing import List, Dict, Any

# Constants
EMBEDDING_DIM = 768  # Dimension of the snowflake-arctic-embed-m embeddings
BATCH_SIZE = 8  # Adjust based on your available RAM
EMBEDDING_API_URL = "http://embedding_api:8002/embed_batch"  # URL of the embedding API

def get_root_dir():
    """Get the root directory of the project."""
    return Path("/app")

def setup_directories():
    """Create necessary directories if they don't exist."""
    embeddings_dir = Path("/app/shared/embeddings")
    embeddings_dir.mkdir(exist_ok=True, parents=True)
    return embeddings_dir

def check_embedding_api():
    """Check if the embedding API is available."""
    try:
        response = requests.get("http://embedding_api:8002/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("Successfully connected to embedding API")
            return True
        else:
            print(f"ERROR: Embedding API is not healthy: {response.json()}")
            return False
    except Exception as e:
        print(f"ERROR: Could not connect to embedding API: {str(e)}")
        return False

def read_code_files(processed_codefiles_dir: Path) -> Dict[str, str]:
    """Read all processed code files."""
    print("Reading code files...")
    code_files = {}
    
    # Get all files recursively
    all_files = list(processed_codefiles_dir.glob("**/*"))
    all_files = [f for f in all_files if f.is_file()]
    
    print(f"Found {len(all_files)} files")
    
    for file_path in tqdm(all_files, desc="Loading files"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():  # Skip empty files
                    # Store relative path as key
                    rel_path = str(file_path.relative_to(processed_codefiles_dir))
                    code_files[rel_path] = content
                    print(f"Loaded: {rel_path} ({len(content)} characters)")
                else:
                    print(f"Skipping empty file: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
    
    return code_files

def generate_embeddings_batch(code_files: Dict[str, str]):
    """Generate embeddings for code files using the embedding API."""
    print("Generating embeddings via the embedding API...")
    
    file_paths = list(code_files.keys())
    embeddings_list = []
    
    # Process in batches to avoid overwhelming the API
    for i in tqdm(range(0, len(file_paths), BATCH_SIZE), desc="Generating embeddings"):
        batch_files = file_paths[i:i + BATCH_SIZE]
        
        # Create a dictionary of files for this batch
        batch_code_files = {file_path: code_files[file_path] for file_path in batch_files}
        
        print(f"\nProcessing batch {i//BATCH_SIZE + 1}/{(len(file_paths)-1)//BATCH_SIZE + 1}")
        for file_path in batch_files:
            print(f"  - Embedding file: {file_path}")
        
        # Call the embedding API
        try:
            response = requests.post(
                EMBEDDING_API_URL,
                json={"code_snippets": batch_code_files},
                timeout=120  # Longer timeout for batch processing
            )
            
            if response.status_code != 200:
                print(f"Error from embedding API: {response.text}")
                raise Exception(f"Embedding API returned status code {response.status_code}")
            
            # Extract embeddings from response
            embedding_data = response.json()
            batch_embeddings = []
            
            # Ensure we maintain the same order as file_paths
            for file_path in batch_files:
                if file_path in embedding_data["embeddings"]:
                    embedding = np.array(embedding_data["embeddings"][file_path], dtype="float32")
                    batch_embeddings.append(embedding)
                else:
                    print(f"WARNING: No embedding returned for {file_path}")
                    # Create a zero embedding as fallback
                    batch_embeddings.append(np.zeros(EMBEDDING_DIM, dtype="float32"))
            
            print(f"Batch {i//BATCH_SIZE + 1} complete: {len(batch_embeddings)} embeddings generated")
            embeddings_list.extend(batch_embeddings)
            
        except Exception as e:
            print(f"Error generating embeddings for batch: {str(e)}")
            # If the batch fails, add zero embeddings as placeholders
            for _ in batch_files:
                embeddings_list.append(np.zeros(EMBEDDING_DIM, dtype="float32"))
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings_list).astype('float32')
    print(f"All embeddings generated. Shape: {embeddings_array.shape}")
    
    return file_paths, embeddings_array

def create_faiss_index(embeddings: np.ndarray):
    """Create a FAISS index for the embeddings."""
    print("Creating FAISS index...")
    
    # Create a CPU-friendly index
    # L2 distance is commonly used for similarity search
    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    
    # Add vectors to the index
    index.add(embeddings)
    print(f"FAISS index created with {index.ntotal} vectors")
    
    return index

def save_data(embeddings_dir: Path, file_paths: List[str], embeddings: np.ndarray, index):
    """Save the embeddings, file paths, and FAISS index to disk."""
    print("Saving data to disk...")
    
    # Save file paths as JSON
    file_paths_path = embeddings_dir / "file_paths.json"
    with open(file_paths_path, 'w', encoding='utf-8') as f:
        json.dump(file_paths, f, indent=2)
    
    # Save embeddings
    embeddings_path = embeddings_dir / "embeddings.npy"
    np.save(embeddings_path, embeddings)
    
    # Save FAISS index
    index_path = embeddings_dir / "faiss_index.bin"
    faiss.write_index(index, str(index_path))
    
    print(f"Data saved to {embeddings_dir}")
    print(f"- File paths (JSON): {file_paths_path}")
    print(f"- Embeddings: {embeddings_path}")
    print(f"- FAISS index: {index_path}")

def main():
    """Main function."""
    print("=" * 80)
    print("Starting Code Embedding Generation")
    print("=" * 80)
    
    # First check if the embedding API is available
    if not check_embedding_api():
        print("ERROR: Embedding API is not available. Please ensure it's running at", EMBEDDING_API_URL)
        return
    
    # In Docker, we use absolute paths
    processed_codefiles_dir = Path("/app/shared/processed_codefiles")
    embeddings_dir = setup_directories()
    
    print(f"Code files directory: {processed_codefiles_dir}")
    print(f"Embeddings directory: {embeddings_dir}")
    
    # Check if processed code files directory exists
    if not processed_codefiles_dir.exists():
        print(f"Error: Directory {processed_codefiles_dir} does not exist!")
        return
    
    # Read code files
    code_files = read_code_files(processed_codefiles_dir)
    
    if not code_files:
        print("No code files found to process!")
        return
    
    print(f"Processing {len(code_files)} code files...")
    
    # Generate embeddings using the embedding API
    file_paths, embeddings = generate_embeddings_batch(code_files)
    
    # Create FAISS index
    index = create_faiss_index(embeddings)
    
    # Save data
    save_data(embeddings_dir, file_paths, embeddings, index)
    
    print("=" * 80)
    print("Embedding generation and indexing complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
