"""
Code Processor API Service

This service:
1. Provides a centralized API for processing code files
2. Removes comments, imports, and empty lines from code
3. Used by both the search_api and indexer to ensure consistent code processing
"""

import re
import os
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, List, Any, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Code Processor API",
    description="Service for cleaning and processing code files",
    version="1.0.0"
)

# Models for API requests and responses
class SingleCodeRequest(BaseModel):
    code: str

class BatchCodeRequest(BaseModel):
    code_snippets: Dict[str, str]  # key: file_path, value: code_content

class SingleCodeResponse(BaseModel):
    processed_code: str

class BatchCodeResponse(BaseModel):
    processed_snippets: Dict[str, str]  # key: file_path, value: processed_code_content

def remove_comments_and_empty_lines(content: str) -> str:
    """Remove comments, empty lines, and import statements from code.
    
    This function removes:
    1. Single-line comments (# and //)
    2. Multi-line comments (/* */, ''', \"\"\"')
    3. Import statements
    4. Empty lines
    
    Args:
        content: The code content to process
        
    Returns:
        Processed code without comments, imports, and empty lines
    """
    # Handle empty input
    if not content or not content.strip():
        return ""
    
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

@app.post("/process", response_model=SingleCodeResponse)
async def process_code(request: SingleCodeRequest):
    """
    Process a single code snippet by removing comments, imports, and empty lines.
    
    Args:
        request: SingleCodeRequest with the code to process
        
    Returns:
        Processed code without comments, imports, and empty lines
    """
    try:
        processed_code = remove_comments_and_empty_lines(request.code)
        return {"processed_code": processed_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing code: {str(e)}")

@app.post("/process_batch", response_model=BatchCodeResponse)
async def process_batch(request: BatchCodeRequest):
    """
    Process multiple code snippets in batch by removing comments, imports, and empty lines.
    
    Args:
        request: BatchCodeRequest with file_paths mapping to code content
        
    Returns:
        Dictionary mapping file_paths to processed code
    """
    try:
        processed_snippets = {}
        for file_path, code in request.code_snippets.items():
            processed_snippets[file_path] = remove_comments_and_empty_lines(code)
            
        return {"processed_snippets": processed_snippets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing batch: {str(e)}")

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "Code Processor API",
        "description": "Service for cleaning and processing code files",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This information"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/process", "method": "POST", "description": "Process a single code snippet (JSON)"},
            {"path": "/process_batch", "method": "POST", "description": "Process multiple code snippets"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True) 