
import subprocess
import os

def search_diary(term: str):
    """
    Searches for a given term in the user's ~/diary folder using ripgrep (rg).

    Args:
        term: The term to search for.

    Returns:
        The output from the rg command, or an error message if rg is not found or the command fails.
    """
    diary_path = os.path.expanduser("~/diary")
    
    # Check if rg is available
    try:
        subprocess.run(["rg", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        return "Error: ripgrep (rg) is not installed or not in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error checking rg version: {e.stderr.decode().strip()}"

    command = ["rg", "-i", "--color=always", term, diary_path]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return result.stdout
        elif result.returncode == 1: # No matches found
            return f"No matches found for '{term}' in {diary_path}"
        else:
            return f"Error executing rg command: {result.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_diary.py <search_term>")
        sys.exit(1)
    
    search_term = sys.argv[1]
    print(search_diary(search_term))
