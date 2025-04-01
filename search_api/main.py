"""
FastAPI service for code similarity search.
This service:
1. Receives code from user as text
2. Calls the code processor API to clean the code (removes comments, empty lines, imports)
3. Calls the embedding API to generate embeddings for the processed code
4. Searches for the 3 most similar files using FAISS
5. Returns the filepaths of these similar files
"""

import os
import json
import numpy as np
import requests
import faiss
from pathlib import Path
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Code Similarity Search API",
    description="API for finding similar code files using embeddings and FAISS",
    version="1.0.0"
)

# Constants
EMBEDDING_DIM = 768
TOP_K = 3  # Number of similar files to return
EMBEDDING_API_URL = "http://embedding_api:8002/embed"  # URL of the embedding API
CODE_PROCESSOR_API_URL = "http://code_processor:8004/process"  # URL of the code processor API

# Path setup
def get_root_dir():
    """Get the root directory of the project."""
    # In Docker, the app directory is /app
    return Path("/app")

# Paths
ROOT_DIR = get_root_dir()
EMBEDDINGS_DIR = Path("/app/shared/embeddings")
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

# Load the model and tokenizer
@app.on_event("startup")
async def startup_load_index():
    """Load the FAISS index and file paths on startup."""
    global index, file_paths, embeddings
    
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
    
    # Check if embedding API is available
    try:
        response = requests.get("http://embedding_api:8002/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("Successfully connected to embedding API")
        else:
            print("WARNING: Embedding API may not be available!")
    except Exception as e:
        print(f"WARNING: Could not connect to embedding API: {str(e)}")

# Process code by calling the code processor API
async def process_code(code: str):
    """Process code by removing comments, imports, and empty lines using the code processor API."""
    try:
        response = requests.post(
            CODE_PROCESSOR_API_URL,
            json={"code": code},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Error from code processor API: {response.text}")
            raise Exception(f"Code processor API returned status code {response.status_code}")
        
        processing_result = response.json()
        processed_code = processing_result["processed_code"]
        return processed_code
    except Exception as e:
        print(f"Error calling code processor API: {str(e)}")
        raise Exception(f"Failed to process code: {str(e)}")

# Generate embedding for code by calling the embedding API
async def generate_embedding(code: str):
    """Generate embedding for a single code snippet using the embedding API."""
    try:
        response = requests.post(
            EMBEDDING_API_URL,
            json={"code": code},  # Changed from data=code to json={"code": code}
            headers={"Content-Type": "application/json"},  # Changed content type
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"Error from embedding API: {response.text}")
            raise Exception(f"Embedding API returned status code {response.status_code}")
        
        embedding_data = response.json()
        embedding = np.array(embedding_data["embedding"], dtype="float32")
        return embedding
    except Exception as e:
        print(f"Error calling embedding API: {str(e)}")
        raise Exception(f"Failed to generate embedding: {str(e)}")

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
    
    The code is processed by the code processor API to remove comments, empty lines, and import statements,
    and then converted to an embedding via the embedding API. This embedding is 
    used to search for similar files in the FAISS index.
    
    Returns the top 3 most similar files.
    """
    try:
        # Process code using the code processor API
        processed_code = await process_code(request.code)
        
        if not processed_code.strip():
            raise HTTPException(
                status_code=400, 
                detail="After processing, the code is empty. Please provide valid code."
            )
        
        # Generate embedding using the embedding API
        embedding = await generate_embedding(processed_code)
        
        # Search for similar files
        similar_files = find_similar_files(embedding)
        
        return {
            "similar_files": similar_files,
            "processed_code": processed_code
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Check service dependencies on startup
@app.on_event("startup")
async def check_dependencies():
    """Check if the code processor API is available at startup."""
    try:
        response = requests.get("http://code_processor:8004/health")
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("Successfully connected to code processor API")
        else:
            print("WARNING: Code processor API may not be available!")
    except Exception as e:
        print(f"WARNING: Could not connect to code processor API: {str(e)}")

# Basic health check endpoint
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "files_indexed": len(file_paths) if file_paths else 0}

# Root endpoint
@app.get("x/")
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