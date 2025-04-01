"""
LLM Service for Code Plagiarism Detection

This service:
1. Receives a user's code and the 3 most similar code files from the search API
2. Constructs a prompt for DeepSeek LLM
3. Sends the prompt to DeepSeek and gets a response
4. Returns "Yes" if the code is plagiarized, "No" otherwise
"""

import requests
import os
import json
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field


with open("key.json", "r") as f:
    key_data = json.load(f)
    API_KEY = key_data["api_key"]

# Initialize FastAPI app
app = FastAPI(
    title="Plagiarism Detection LLM Service",
    description="Service that uses DeepSeek LLM to detect code plagiarism",
    version="1.0.0"
)

# Models
class SimilarFile(BaseModel):
    file_path: str
    similarity_score: float
    content: str = ""  # This will hold the actual code content

class PlagiarismCheckRequest(BaseModel):
    user_code: str
    similar_files: List[SimilarFile]

class PlagiarismCheckResponse(BaseModel):
    is_plagiarized: bool
    explanation: str = ""  # Optional explanation from the LLM
    llm_response: str = ""  # Raw LLM response for debugging

# Configuration
class LLMConfig:
    def __init__(self):
        self.api_key = API_KEY
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.model = "deepseek-coder"  # Default model

# Get LLM config as a dependency
def get_llm_config():
    return LLMConfig()

# Construct the prompt for the LLM
def construct_prompt(user_code: str, similar_files: List[SimilarFile]) -> str:
    prompt = """You are a code plagiarism detection system. Your task is to determine if the submitted code is plagiarized from any of the reference code files.

Please analyze the following submitted code:

```
{0}
```

Compare it with these reference code files that were found to be similar:

""".format(user_code)
    
    # Add each similar file to the prompt
    for i, file in enumerate(similar_files, 1):
        prompt += f"Reference File {i} ({file.file_path}):\n```\n{file.content}\n```\n\n"
    
    prompt += """Based on your analysis, is the submitted code plagiarized from any of the reference files?

Consider the following as strong indicators of plagiarism:
1. Nearly identical code structure or algorithm implementation
2. Same variable names and function structures
3. Similar comments, especially distinctive ones
4. Identical code sections with only minor changes like variable renaming
5. Same code patterns, especially if it's a unique approach

For the purpose of this analysis, consider plagiarism as code that appears to be copied, with or without minor modifications, from one of the reference files.

Reply with ONLY "Yes" if the code shows clear signs of plagiarism from any reference file, or "No" if it appears to be original.

Your response:"""
    
    return prompt

# Call the DeepSeek API
async def call_deepseek(prompt: str, config: LLMConfig) -> str:
    """Call the DeepSeek API with the given prompt."""
    if not config.api_key:
        print("ERROR: DeepSeek API key not configured!")
        raise HTTPException(
            status_code=500, 
            detail="DeepSeek API key not configured. Please set the DEEPSEEK_API_KEY environment variable."
        )
    
    # Save the prompt to a file
    try:
        with open("previous_prompt.txt", "w", encoding="utf-8") as f:
            f.write(prompt)
        print("Saved prompt to file: previous_prompt.txt")
    except Exception as e:
        print(f"Error saving prompt to file: {str(e)}")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.api_key}"
    }
    
    data = {
        "model": config.model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,  # Low temperature for more deterministic outputs
        "max_tokens": 100    # We only need a simple "Yes" or "No" response
    }
    
    try:
        print(f"Calling DeepSeek API with model: {config.model}")
        print(f"Prompt length: {len(prompt)} characters")
        
        response = requests.post(config.api_url, headers=headers, json=data)
        
        print(f"DeepSeek API response status code: {response.status_code}")
        
        # Log response content for debugging if there's an error
        if response.status_code != 200:
            print(f"DeepSeek API error response: {response.text}")
            
        response.raise_for_status()
        response_json = response.json()
        
        # Check if the expected fields are in the response
        if 'choices' not in response_json or not response_json['choices']:
            print(f"Unexpected response format from DeepSeek API: {response_json}")
            raise HTTPException(
                status_code=500, 
                detail=f"Unexpected response format from DeepSeek API: {response_json}"
            )
            
        return response_json['choices'][0]['message']['content'].strip()
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling DeepSeek API: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response content: {e.response.text}")
        raise HTTPException(status_code=500, detail=f"Error calling DeepSeek API: {str(e)}")
    
    except Exception as e:
        print(f"Unexpected error when calling DeepSeek API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

def get_file_content(file_path: str) -> str:
    """Read the content of a file given its path."""
    try:
        # Get root directory (resolving to absolute path)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        
        # Define the processed_codefiles directory (absolute path)
        processed_codefiles_dir = os.path.join(project_root, "shared", "processed_codefiles")
        
        # List of potential paths to try
        search_paths = [
            file_path,  # Try the exact path first
            os.path.join(project_root, file_path),  # Try relative to project root
            os.path.join(processed_codefiles_dir, file_path),  # Try in processed_codefiles
            os.path.join(processed_codefiles_dir, os.path.basename(file_path)),  # Try just the filename
        ]
        
        print(f"Looking for file: {file_path}")
        print(f"Current directory: {current_dir}")
        print(f"Project root (resolved): {project_root}")
        print(f"Processed codefiles directory: {processed_codefiles_dir}")
        
        # First try the predefined paths
        for path in search_paths:
            print(f"Trying path: {path}")
            if os.path.isfile(path):
                print(f"✓ File found at: {path}")
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(f"Successfully read {len(content)} characters")
                    return content
        
        # If file still not found, do a direct check of the processed_codefiles directory
        if os.path.exists(processed_codefiles_dir):
            print(f"Checking directory contents of: {processed_codefiles_dir}")
            files_in_dir = os.listdir(processed_codefiles_dir)
            print(f"Files in directory ({len(files_in_dir)} total):")
            
            # Print the first 10 files for debugging
            for i, f in enumerate(sorted(files_in_dir)[:10]):
                print(f"  {i+1}. {f}")
            if len(files_in_dir) > 10:
                print(f"  ... and {len(files_in_dir)-10} more files")
            
            # Check if our target file is in the directory (case sensitive and insensitive)
            filename = os.path.basename(file_path)
            if filename in files_in_dir:
                full_path = os.path.join(processed_codefiles_dir, filename)
                print(f"✓ Found exact filename match: {full_path}")
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(f"Successfully read {len(content)} characters")
                    return content
                    
            # Try case-insensitive match if exact match fails
            lower_filename = filename.lower()
            lower_files = {f.lower(): f for f in files_in_dir}
            if lower_filename in lower_files:
                actual_filename = lower_files[lower_filename]
                full_path = os.path.join(processed_codefiles_dir, actual_filename)
                print(f"✓ Found case-insensitive match: {full_path}")
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(f"Successfully read {len(content)} characters")
                    return content
        else:
            print(f"❌ Directory does not exist: {processed_codefiles_dir}")
            
        # If all attempts fail, return error message
        print(f"❌ ERROR: File not found: {file_path}")
        return f"[Error: File not found: {file_path}. Searched in {processed_codefiles_dir}]"
        
    except Exception as e:
        print(f"❌ ERROR reading file {file_path}: {str(e)}")
        return f"[Error reading file {file_path}: {str(e)}]"

# Endpoint to check for plagiarism
@app.post("/check_plagiarism", response_model=PlagiarismCheckResponse)
async def check_plagiarism(
    request: PlagiarismCheckRequest,
    config: LLMConfig = Depends(get_llm_config)
):
    """
    Check if the provided code is plagiarized from any of the similar files.
    
    The service:
    1. Takes the user's code and the similar files with their paths
    2. Reads the content of the files if not provided
    3. Constructs a prompt for the DeepSeek LLM
    4. Sends the prompt to DeepSeek and gets a response
    5. Returns "Yes" if the code is plagiarized, "No" otherwise
    """
    try:
        print(f"Received request to check plagiarism for code with {len(request.user_code)} characters")
        print(f"Number of similar files: {len(request.similar_files)}")
        
        # Validate input
        if not request.user_code.strip():
            raise HTTPException(status_code=400, detail="User code cannot be empty")
        
        if not request.similar_files:
            raise HTTPException(status_code=400, detail="At least one similar file is required")
        
        # Process similar files - read content if empty
        similar_files_with_content = []
        for i, file in enumerate(request.similar_files):
            # Create a copy of the file to avoid modifying the original
            similar_file = SimilarFile(
                file_path=file.file_path,
                similarity_score=file.similarity_score,
                content=file.content
            )
            
            # If content is empty, read it from the file
            if not similar_file.content.strip():
                print(f"Reading content for file: {file.file_path}")
                similar_file.content = get_file_content(file.file_path)
            
            similar_files_with_content.append(similar_file)
            
            print(f"Similar file {i+1}: {file.file_path} (Score: {file.similarity_score}, Content length: {len(similar_file.content)} chars)")
            # Print a small snippet of each file for easier debugging
            content_preview = similar_file.content[:100] + "..." if len(similar_file.content) > 100 else similar_file.content
            print(f"Content preview: {content_preview}")
        
        # Construct the prompt
        print("Constructing prompt for DeepSeek API...")
        prompt = construct_prompt(request.user_code, similar_files_with_content)
        
        # Call the DeepSeek API
        print("Calling DeepSeek API...")
        llm_response = await call_deepseek(prompt, config)
        
        print(f"Received response from DeepSeek API: '{llm_response}'")
        
        # Process the response - check for "Yes" case-insensitively
        is_plagiarized = "yes" in llm_response.lower()
        
        print(f"Plagiarism detection result: {is_plagiarized}")
        
        # Return the result
        return {
            "is_plagiarized": is_plagiarized,
            "explanation": "",  # Could extract an explanation if the LLM provides one
            "llm_response": llm_response
        }
    
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        print(f"Unexpected error in check_plagiarism: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check(config: LLMConfig = Depends(get_llm_config)):
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "llm_api_key_configured": bool(config.api_key),
        "llm_model": config.model
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "name": "Plagiarism Detection LLM Service",
        "description": "Service that uses DeepSeek LLM to detect code plagiarism",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "This information"},
            {"path": "/health", "method": "GET", "description": "Health check"},
            {"path": "/check_plagiarism", "method": "POST", "description": "Check if code is plagiarized"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 