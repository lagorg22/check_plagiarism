'''
This script generates embeddings for processed code files using the snowflake-arctic-embed-m model.
The embeddings are then indexed using FAISS and saved to disk.
Optimized for CPU-only usage.
'''

import os
import glob
import torch
import faiss
import numpy as np
import json
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel
from typing import List, Dict, Any

# Constants
MODEL_NAME = "Snowflake/snowflake-arctic-embed-m"
EMBEDDING_DIM = 768  # Dimension of the snowflake-arctic-embed-m embeddings
BATCH_SIZE = 8  # Adjust based on your available RAM

def get_root_dir():
    """Get the root directory of the project."""
    current_file = Path(__file__)
    return current_file.parent.parent  # Go up from indexer to project root

def setup_directories():
    """Create necessary directories if they don't exist."""
    root_dir = get_root_dir()
    embeddings_dir = root_dir / "shared" / "embeddings"
    embeddings_dir.mkdir(exist_ok=True, parents=True)
    return embeddings_dir

def load_model():
    """Load the embedding model and tokenizer."""
    print("Loading tokenizer and model...")
    
    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    # Load the model with CPU optimizations
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()  # Set to evaluation mode
    print(f"Successfully loaded {MODEL_NAME} model")
    
    return tokenizer, model

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

def generate_embeddings(model, tokenizer, code_files: Dict[str, str]):
    """Generate embeddings for code files."""
    print("Generating embeddings...")
    
    file_paths = list(code_files.keys())
    contents = list(code_files.values())
    embeddings = []
    
    # Process in batches to save memory
    for i in tqdm(range(0, len(contents), BATCH_SIZE), desc="Generating embeddings"):
        batch_texts = contents[i:i + BATCH_SIZE]
        batch_files = file_paths[i:i + BATCH_SIZE]
        
        print(f"\nProcessing batch {i//BATCH_SIZE + 1}/{(len(contents)-1)//BATCH_SIZE + 1}")
        for j, file_path in enumerate(batch_files):
            print(f"  - Embedding file: {file_path}")
        
        # Tokenize
        inputs = tokenizer(
            batch_texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        
        # Generate embeddings
        with torch.no_grad():
            outputs = model(**inputs)
            # Use mean pooling
            attention_mask = inputs["attention_mask"]
            token_embeddings = outputs.last_hidden_state
            input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
            batch_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
            batch_embeddings = batch_embeddings.cpu().numpy()
        
        print(f"Batch {i//BATCH_SIZE + 1} complete: {len(batch_embeddings)} embeddings generated")
        embeddings.extend(batch_embeddings)
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings).astype('float32')
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
    
    root_dir = get_root_dir()
    processed_codefiles_dir = root_dir / "shared" / "processed_codefiles"
    embeddings_dir = setup_directories()
    
    print(f"Root directory: {root_dir}")
    print(f"Code files directory: {processed_codefiles_dir}")
    print(f"Embeddings directory: {embeddings_dir}")
    
    # Check if processed code files directory exists
    if not processed_codefiles_dir.exists():
        print(f"Error: Directory {processed_codefiles_dir} does not exist!")
        return
    
    # Load model and tokenizer
    tokenizer, model = load_model()
    
    # Read code files
    code_files = read_code_files(processed_codefiles_dir)
    
    if not code_files:
        print("No code files found to process!")
        return
    
    print(f"Processing {len(code_files)} code files...")
    
    # Generate embeddings
    file_paths, embeddings = generate_embeddings(model, tokenizer, code_files)
    
    # Create FAISS index
    index = create_faiss_index(embeddings)
    
    # Save data
    save_data(embeddings_dir, file_paths, embeddings, index)
    
    print("=" * 80)
    print("Embedding generation and indexing complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()
