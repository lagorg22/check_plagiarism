"""
Test script for the LLM Plagiarism Detection Service.
This script:
1. Sends a code snippet to the search API to find similar files
2. Takes the search results and calls the LLM service
3. Prints the plagiarism check results
"""

import requests
import json
import os
from pathlib import Path

# Configuration
SEARCH_API_URL = "http://localhost:8000/search"
LLM_API_URL = "http://localhost:8001/check_plagiarism"

# Test code snippet - implementation of a Union-Find data structure
test_code = """
@Test
	public void testSameCount1() {
		List<String> a = stringToList("abbccc");
		List<String> b = stringToList("cccbba");
		assertEquals(3, Appearances.sameCount(a, b));
	}
	
	@Test
	public void testSameCount2() {
		// basic List<Integer> cases
		List<Integer> a = Arrays.asList(1, 2, 3, 1, 2, 3, 5);
		assertEquals(1, Appearances.sameCount(a, Arrays.asList(1, 9, 9, 1)));
		assertEquals(2, Appearances.sameCount(a, Arrays.asList(1, 3, 3, 1)));
		assertEquals(1, Appearances.sameCount(a, Arrays.asList(1, 3, 3, 1, 1)));
	}
"""

def get_file_content(file_path):
    """Read the content of a similar file from the processed codefiles directory."""
    try:
        # Get the root directory
        current_file = Path(__file__)
        root_dir = current_file.parent.parent  # Go up from llm_service to project root
        
        # Construct the full path
        full_path = root_dir / "shared" / "processed_codefiles" / file_path
        
        # Read the file content
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return f"[Error reading file: {str(e)}]"

def call_search_api(code):
    """Call the search API to get similar files."""
    print("\n1. Calling the Search API to find similar files...")
    
    try:
        # Make the request to the search API
        response = requests.post(
            SEARCH_API_URL,
            json={"code": code}
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Get the response data
        result = response.json()
        print(f"Search API found {len(result['similar_files'])} similar files:")
        for i, file in enumerate(result['similar_files'], 1):
            print(f"  {i}. {file['file_path']} (Score: {file['similarity_score']:.4f})")
        
        return result['similar_files'], result['processed_code']
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling search API: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return [], code

def call_llm_api(processed_code, similar_files):
    """Call the LLM API to check for plagiarism."""
    print("\n2. Calling the LLM API to check for plagiarism...")
    
    # Add content to similar files
    for file in similar_files:
        file['content'] = get_file_content(file['file_path'])
        print(f"  Added content for {file['file_path']} ({len(file['content'])} characters)")
    
    try:
        # Make the request to the LLM API
        response = requests.post(
            LLM_API_URL,
            json={
                "user_code": processed_code,
                "similar_files": similar_files
            }
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Get the response data
        result = response.json()
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return {"error": str(e)}

def main():
    """Main function to run the test."""
    print("=" * 80)
    print("Testing Code Plagiarism Detection System")
    print("=" * 80)
    
    # Call the search API
    similar_files, processed_code = call_search_api(test_code)
    
    if not similar_files:
        print("\nNo similar files found. Cannot proceed with plagiarism check.")
        return
    
    # Call the LLM API
    result = call_llm_api(processed_code, similar_files)
    
    # Print the result
    print("\n3. Results:")
    print("-" * 30)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Plagiarism detected: {result['is_plagiarized']}")
        print(f"LLM response: {result['llm_response']}")
    
    print("\nTest completed!")
    print("=" * 80)

if __name__ == "__main__":
    main() 