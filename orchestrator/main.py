"""
Orchestrator Service for Code Plagiarism Detection System

This service:
1. Accepts code as plain text input
2. Converts the code to JSON format internally
3. Calls the search API to find similar files
4. Retrieves the content of similar files
5. Calls the LLM service to check for plagiarism
6. Returns the final result as JSON
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field

# Initialize FastAPI app
app = FastAPI(
    title="Code Plagiarism Detection Orchestrator",
    description="Orchestrates the process of code plagiarism detection",
    version="1.0.0"
)

# Configuration
SEARCH_API_URL = "http://localhost:8000/search"
LLM_API_URL = "http://localhost:8001/check_plagiarism"

# Models for internal use
class SimilarFile(BaseModel):
    file_path: str
    similarity_score: float
    content: str = ""  # Keep this for backward compatibility

# Helper function to get the root directory of the project
def get_root_dir():
    """Get the root directory of the project."""
    return os.getenv("PROJECT_ROOT", "/app")

# Helper function to convert code text to JSON format
def convert_code_to_json(text):
    """Convert plain text code to a JSON payload."""
    return {"code": text}

# Call the search API to find similar files
async def call_search_api(code: str):
    """Call the search API to find similar files."""
    try:
        print(f"Calling search API with code of length: {len(code)}")
        
        # Convert code to JSON format
        json_data = convert_code_to_json(code)
        
        response = requests.post(
            SEARCH_API_URL,
            json=json_data,
            timeout=30
        )
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling search API: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Error calling search API: {str(e)}")

# Call the LLM API to check for plagiarism
async def call_llm_api(user_code: str, similar_files: List[SimilarFile]):
    """Call the LLM API to check for plagiarism."""
    try:
        print(f"Calling LLM API with {len(similar_files)} similar files")
        
        response = requests.post(
            LLM_API_URL,
            json={
                "user_code": user_code,
                "similar_files": [file.dict() for file in similar_files]
            },
            timeout=60
        )
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Error calling LLM API: {str(e)}")

# Main endpoint for text-based plagiarism check
@app.post("/check")
async def check_plagiarism(code: str = Body(..., media_type="text/plain")):
    """
    Check if the provided code text is plagiarized.
    
    This endpoint:
    1. Accepts plain text code
    2. Converts it to JSON format internally
    3. Calls the search API to find similar files
    4. Calls the LLM service to check for plagiarism (LLM service will read file contents)
    5. Returns a JSON response with the results
    """
    try:
        print(f"Received plagiarism check request for code of length: {len(code)}")
        
        # Call the search API
        search_results = await call_search_api(code)
        
        # Get the similar files and processed code
        similar_files_data = search_results.get("similar_files", [])
        processed_code = search_results.get("processed_code", code)
        
        print(f"Search API found {len(similar_files_data)} similar files")
        
        # If no similar files found, return not plagiarized
        if not similar_files_data:
            return {
                "plagiarism": False,
                "llm_response": "No similar files found",
                "similar_files": []
            }
        
        # Prepare the similar files (without reading content)
        similar_files = []
        for file_data in similar_files_data:
            similar_file = SimilarFile(
                file_path=file_data["file_path"],
                similarity_score=file_data["similarity_score"],
                content=""  # Empty content - LLM service will read the files
            )
            similar_files.append(similar_file)
            
            print(f"Added file path: {file_data['file_path']}")
        
        # Call the LLM API
        llm_results = await call_llm_api(processed_code, similar_files)
        
        is_plagiarized = llm_results.get("is_plagiarized", False)
        llm_response = llm_results.get("llm_response", "")
        
        print(f"LLM result: is_plagiarized={is_plagiarized}, response='{llm_response}'")
        
        # Return the result in the specified format
        return {
            "plagiarism": is_plagiarized,
            "llm_response": llm_response,
            "similar_files": [
                {
                    "file_path": file.file_path,
                    "similarity_score": file.similarity_score
                }
                for file in similar_files
            ]
        }
    
    except Exception as e:
        print(f"Error in check_plagiarism: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "plagiarism": False,
            "llm_response": f"Error: {str(e)}",
            "similar_files": []
        }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check search API
        search_health = requests.get("http://localhost:8000/health", timeout=5)
        search_status = "healthy" if search_health.status_code == 200 else "unhealthy"
        
        # Check LLM API
        llm_health = requests.get("http://localhost:8001/health", timeout=5)
        llm_status = "healthy" if llm_health.status_code == 200 else "unhealthy"
        
        return {
            "status": "healthy" if search_status == "healthy" and llm_status == "healthy" else "unhealthy",
            "search_api": search_status,
            "llm_service": llm_status
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "Code Plagiarism Detection Orchestrator",
        "description": "Orchestrates the process of code plagiarism detection",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This information"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/check", "method": "POST", "description": "Check if code is plagiarized (text input)"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True) 