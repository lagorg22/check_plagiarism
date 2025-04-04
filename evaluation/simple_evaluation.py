#!/usr/bin/env python3
"""
Simple evaluation script for code plagiarism detection.

This script:
1. Reads files from 'original' and 'plagiarized' directories in the current folder
2. Sends each file to the plagiarism detection service
3. Creates a pandas DataFrame with the results
4. Prints a summary of the findings
"""

import os
import requests
import pandas as pd
from pathlib import Path

# Configuration
ORCHESTRATOR_URL = "http://orchestrator:8000"
CHECK_URL = f"{ORCHESTRATOR_URL}/check"

# Directories for test data (in current directory)
PLAGIARIZED_DIR = "plagiarized"
ORIGINAL_DIR = "original"

def read_file_content(file_path):
    """Read content from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def check_plagiarism(code_text):
    """Send code to the plagiarism detection service."""
    try:
        response = requests.post(
            CHECK_URL, 
            data=code_text,
            headers={"Content-Type": "text/plain"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Exception when calling API: {str(e)}")
        return None

def main():
    """Main function to run the evaluation."""
    # Check if directories exist
    if not os.path.exists(ORIGINAL_DIR):
        print(f"Error: '{ORIGINAL_DIR}' directory not found")
        return
    
    if not os.path.exists(PLAGIARIZED_DIR):
        print(f"Error: '{PLAGIARIZED_DIR}' directory not found")
        return
    
    # Get files
    plagiarized_files = list(Path(PLAGIARIZED_DIR).glob("*.*"))
    original_files = list(Path(ORIGINAL_DIR).glob("*.*"))
    
    print(f"Found {len(plagiarized_files)} plagiarized files and {len(original_files)} original files")
    
    # List to store results
    results = []
    
    # Process plagiarized files
    print("Processing plagiarized files...")
    for file_path in plagiarized_files:
        print(f"  Testing: {file_path}")
        code = read_file_content(file_path)
        api_result = check_plagiarism(code)
        
        if api_result:
            # Convert the similar files to a more readable format
            similar_files = [(sf["file_path"], sf["similarity_score"]) for sf in api_result["similar_files"]]
            
            results.append({
                "file": file_path.name,
                "expected_result": "Yes",
                "similar_files": similar_files,
                "result": "Yes" if api_result["plagiarism"] else "No",
                "llm_response": api_result.get("llm_response", "")
            })
    
    # Process original files
    print("Processing original files...")
    for file_path in original_files:
        print(f"  Testing: {file_path}")
        code = read_file_content(file_path)
        api_result = check_plagiarism(code)
        
        if api_result:
            # Convert the similar files to a more readable format
            similar_files = [(sf["file_path"], sf["similarity_score"]) for sf in api_result["similar_files"]]
            
            results.append({
                "file": file_path.name,
                "expected_result": "No",
                "similar_files": similar_files,
                "result": "Yes" if api_result["plagiarism"] else "No",
                "llm_response": api_result.get("llm_response", "")
            })
    
    # Create DataFrame
    if not results:
        print("No results were obtained. Please check API connection.")
        return
    
    df = pd.DataFrame(results)
    
    # Calculate simple metrics
    correct = (df["expected_result"] == df["result"]).sum()
    total = len(df)
    accuracy = correct / total if total > 0 else 0
    
    # Print results
    print("\n===== EVALUATION RESULTS =====")
    print(f"Total files tested: {total}")
    print(f"Correct predictions: {correct} ({accuracy:.1%})")
    
    # Calculate false positives and false negatives
    false_positives = ((df["expected_result"] == "No") & (df["result"] == "Yes")).sum()
    false_negatives = ((df["expected_result"] == "Yes") & (df["result"] == "No")).sum()
    
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")
    
    # Show results for each file
    print("\n===== DETAILED RESULTS =====")
    for _, row in df.iterrows():
        print(f"File: {row['file']}")
        print(f"  Expected: {row['expected_result']}, Result: {row['result']}")
        print(f"  LLM Response: {row['llm_response']}")
        print("  Similar files:")
        for sf in row['similar_files']:
            print(f"    - {sf[0]} (Score: {sf[1]:.3f})")
        print()
    
    # Save results to CSV
    csv_path = "evaluation_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"Results saved to {csv_path}")

if __name__ == "__main__":
    main() 