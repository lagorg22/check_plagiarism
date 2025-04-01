"""
Embedding API Service

This service:
1. Provides a centralized API for generating embeddings using the snowflake-arctic-embed-m model
2. Exposes endpoints for generating embeddings for individual code snippets or batches
3. Used by both the search_api and indexer to ensure consistent embedding generation
"""

import os
import torch
import numpy as np
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModel

# Constants
MODEL_NAME = "Snowflake/snowflake-arctic-embed-m"
EMBEDDING_DIM = 768  # Dimension of the snowflake-arctic-embed-m embeddings

# Initialize FastAPI app
app = FastAPI(
    title="Code Embedding API",
    description="Service for generating code embeddings using snowflake-arctic-embed-m model",
    version="1.0.0"
)

# Models for API requests and responses
class CodeEmbeddingRequest(BaseModel):
    code: str

class BatchEmbeddingRequest(BaseModel):
    code_snippets: Dict[str, str]  # key: file_path, value: code_content

class EmbeddingResponse(BaseModel):
    embedding: List[float]

class BatchEmbeddingResponse(BaseModel):
    embeddings: Dict[str, List[float]]  # key: file_path, value: embedding

# Global variables for the model and tokenizer
model = None
tokenizer = None

def get_root_dir():
    """Get the root directory of the project."""
    current_file = Path(__file__)
    return current_file.parent.parent  # Go up from embedding_api to project root

# Load the model and tokenizer on startup
@app.on_event("startup")
async def startup_load_model():
    """Load the model and tokenizer on startup."""
    global model, tokenizer
    
    print("Loading tokenizer and model...")
    try:
        # Load the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        
        # Load the model with CPU optimizations
        model = AutoModel.from_pretrained(MODEL_NAME)
        model.eval()  # Set to evaluation mode
        print(f"Successfully loaded {MODEL_NAME} model")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise RuntimeError(f"Failed to load model: {str(e)}")

def generate_single_embedding(code: str):
    """Generate embedding for a single code snippet."""
    # Check if model and tokenizer are loaded
    if model is None or tokenizer is None:
        raise RuntimeError("Model or tokenizer not loaded!")
    
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
        embedding = embedding.cpu().numpy()[0]  # Get the first (and only) embedding
    
    return embedding.astype('float32').tolist()

def generate_batch_embeddings(code_snippets: Dict[str, str]):
    """Generate embeddings for multiple code snippets."""
    # Check if model and tokenizer are loaded
    if model is None or tokenizer is None:
        raise RuntimeError("Model or tokenizer not loaded!")
    
    file_paths = list(code_snippets.keys())
    contents = list(code_snippets.values())
    
    if not contents:
        return {}
    
    # Tokenize
    inputs = tokenizer(
        contents,
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
    
    # Create a dictionary mapping file paths to embeddings
    result = {}
    for i, file_path in enumerate(file_paths):
        result[file_path] = batch_embeddings[i].astype('float32').tolist()
    
    return result

@app.post("/embed", response_model=EmbeddingResponse)
async def embed_code(request: CodeEmbeddingRequest):
    """Generate embedding for a single code snippet."""
    try:
        embedding = generate_single_embedding(request.code)
        return {"embedding": embedding}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embedding: {str(e)}")

@app.post("/embed_batch", response_model=BatchEmbeddingResponse)
async def embed_batch(request: BatchEmbeddingRequest):
    """Generate embeddings for multiple code snippets."""
    try:
        embeddings = generate_batch_embeddings(request.code_snippets)
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating batch embeddings: {str(e)}")

@app.get("/health")
async def health():
    """Health check endpoint."""
    if model is None or tokenizer is None:
        return {"status": "unhealthy", "message": "Model or tokenizer not loaded"}
    return {"status": "healthy", "model": MODEL_NAME}

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "Code Embedding API",
        "description": "Service for generating code embeddings using snowflake-arctic-embed-m model",
        "model": MODEL_NAME,
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This information"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/embed", "method": "POST", "description": "Generate embedding for single code snippet"},
            {"path": "/embed_batch", "method": "POST", "description": "Generate embeddings for multiple code snippets"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True) 