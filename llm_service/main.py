"""
LLM Service for Code Plagiarism Detection

This service:
1. Receives a user's code and the 3 most similar code files from the search API
2. Constructs a prompt for DeepSeek LLM
3. Sends the prompt to DeepSeek and gets a response
4. Returns "Yes" if the code is plagiarized, "No" otherwise
"""

import os
import requests
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

# Endpoint to check for plagiarism
@app.post("/check_plagiarism", response_model=PlagiarismCheckResponse)
async def check_plagiarism(
    request: PlagiarismCheckRequest,
    config: LLMConfig = Depends(get_llm_config)
):
    """
    Check if the provided code is plagiarized from any of the similar files.
    
    The service:
    1. Takes the user's code and the similar files with their content
    2. Constructs a prompt for the DeepSeek LLM
    3. Sends the prompt to DeepSeek and gets a response
    4. Returns "Yes" if the code is plagiarized, "No" otherwise
    """
    try:
        print(f"Received request to check plagiarism for code with {len(request.user_code)} characters")
        print(f"Number of similar files: {len(request.similar_files)}")
        
        # Validate input
        if not request.user_code.strip():
            raise HTTPException(status_code=400, detail="User code cannot be empty")
        
        if not request.similar_files:
            raise HTTPException(status_code=400, detail="At least one similar file is required")
        
        # Log similar files info
        for i, file in enumerate(request.similar_files):
            print(f"Similar file {i+1}: {file.file_path} (Score: {file.similarity_score}, Content length: {len(file.content)} chars)")
            # Print a small snippet of each file for easier debugging
            content_preview = file.content[:100] + "..." if len(file.content) > 100 else file.content
            print(f"Content preview: {content_preview}")
        
        # Construct the prompt
        print("Constructing prompt for DeepSeek API...")
        prompt = construct_prompt(request.user_code, request.similar_files)
        
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