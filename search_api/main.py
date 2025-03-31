"""
FastAPI service for code similarity search.
This service:
1. Receives code from user as text
2. Cleans the code (removes comments, empty lines, imports)
3. Generates embeddings for the code
4. Searches for the 3 most similar files using FAISS
5. Returns the filepaths of these similar files
"""

import os
import re
import json
import numpy as np
import torch
import faiss
from pathlib import Path
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModel

# Initialize FastAPI app
app = FastAPI(
    title="Code Similarity Search API",
    description="API for finding similar code files using embeddings and FAISS",
    version="1.0.0"
)

# Constants
MODEL_NAME = "Snowflake/snowflake-arctic-embed-m"
EMBEDDING_DIM = 768
TOP_K = 3  # Number of similar files to return

# Path setup
def get_root_dir():
    """Get the root directory of the project."""
    current_file = Path(__file__)
    return current_file.parent.parent  # Go up from search_api to project root

# Paths
ROOT_DIR = get_root_dir()
EMBEDDINGS_DIR = ROOT_DIR / "shared" / "embeddings"
FILE_PATHS_JSON = EMBEDDINGS_DIR / "file_paths.json"
EMBEDDINGS_NPY = EMBEDDINGS_DIR / "embeddings.npy"
FAISS_INDEX = EMBEDDINGS_DIR / "faiss_index.bin"

# Load file paths, embeddings and FAISS index at startup
file_paths = []
index = None

# Input and output models
class CodeRequest(BaseModel):
    code: str

class SimilarFile(BaseModel):
    file_path: str
    similarity_score: float

class SimilarFilesResponse(BaseModel):
    similar_files: List[SimilarFile]
    processed_code: str

# Code cleaning function (copied from process_codefiles.py)
def remove_comments_and_empty_lines(content):
    """Remove comments, empty lines, and import statements from code."""
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

# Load the model and tokenizer
@app.on_event("startup")
async def startup_load_model():
    """Load the model, tokenizer, and FAISS index on startup."""
    global model, tokenizer, index, file_paths, embeddings
    
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME)
    model.eval()
    
    print("Loading FAISS index and file paths...")
    if not FAISS_INDEX.exists() or not FILE_PATHS_JSON.exists() or not EMBEDDINGS_NPY.exists():
        raise RuntimeError(
            "FAISS index, file paths, or embeddings not found! "
            "Please run generate_embeddings.py first."
        )
    
    # Load file paths
    with open(FILE_PATHS_JSON, 'r') as f:
        file_paths = json.load(f)
    
    # Load embeddings
    embeddings = np.load(EMBEDDINGS_NPY)
    
    # Load FAISS index
    index = faiss.read_index(str(FAISS_INDEX))
    
    print(f"Successfully loaded {len(file_paths)} file paths and FAISS index with {index.ntotal} vectors")

# Generate embedding for code
def generate_embedding(code: str):
    """Generate embedding for a single code snippet."""
    # Tokenize
    inputs = tokenizer(
        code,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )
    
    # Generate embedding
    with torch.no_grad():
        outputs = model(**inputs)
        # Use mean pooling
        attention_mask = inputs["attention_mask"]
        token_embeddings = outputs.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        embedding = torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        embedding = embedding.cpu().numpy()
    
    return embedding.astype('float32')

# Find similar files
def find_similar_files(embedding: np.ndarray, top_k: int = TOP_K):
    """Find top_k similar files using FAISS."""
    # Reshape to (1, EMBEDDING_DIM)
    embedding = embedding.reshape(1, -1)
    
    # Search in FAISS index
    distances, indices = index.search(embedding, top_k)
    
    # Flatten arrays
    distances = distances.flatten()
    indices = indices.flatten()
    
    # Get file paths and create result
    similar_files = []
    for i, (idx, distance) in enumerate(zip(indices, distances)):
        if idx < len(file_paths):
            similar_files.append({
                "file_path": file_paths[idx],
                "similarity_score": float(1.0 / (1.0 + distance))  # Convert distance to similarity score
            })
    
    # Sort by similarity score (descending)
    similar_files.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return similar_files

# API endpoint for code similarity search
@app.post("/search", response_model=SimilarFilesResponse)
async def search_similar_code(request: CodeRequest):
    """
    Search for similar code files based on the provided code snippet.
    
    The code is processed to remove comments, empty lines, and import statements,
    and then converted to an embedding. This embedding is used to search for
    similar files in the FAISS index.
    
    Returns the top 3 most similar files.
    """
    try:
        # Process code (remove comments, empty lines, imports)
        processed_code = remove_comments_and_empty_lines(request.code)
        
        if not processed_code.strip():
            raise HTTPException(
                status_code=400, 
                detail="After processing, the code is empty. Please provide valid code."
            )
        
        # Generate embedding
        embedding = generate_embedding(processed_code)
        
        # Search for similar files
        similar_files = find_similar_files(embedding)
        
        return {
            "similar_files": similar_files,
            "processed_code": processed_code
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Basic health check endpoint
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "files_indexed": len(file_paths) if file_paths else 0}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "Code Similarity Search API",
        "description": "API for finding similar code files using embeddings and FAISS",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This information"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/search", "method": "POST", "description": "Search for similar code files"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 