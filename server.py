from fastmcp import FastMCP
import os
import subprocess

# Initialize FastMCP
mcp = FastMCP()

# Import the search_diary function
# Assuming search_diary.py is in the same directory or accessible via PYTHONPATH
from search_diary import search_diary
from read_md_files import read_and_concatenate_md_files
from read_recent_files_tool import read_recent_files

# Register search_diary as a tool
@mcp.tool()
def search_diary_tool(term: str):
    """
    Searches for a given term in the user's ~/diary folder using ripgrep (rg).
    """
    return search_diary(term)

# Register read_md_files as a tool
@mcp.tool()
def read_md_files_tool(file_paths: list[str]):
    """
    Reads the content of multiple Markdown files and concatenates them.

    Args:
        file_paths: A list of absolute paths to the Markdown files.

    Returns:
        The concatenated content of all files, with a separator between each file.
    """
    return read_and_concatenate_md_files(file_paths)

@mcp.tool()
def read_recent_files_tool(path: str = os.path.expanduser("~/diary"), months: int = 3):
    """
    Reads and concatenates the content of files modified within the last 'months' from the specified path.

    Args:
        path: The absolute path to the directory to search within. Defaults to the user's diary directory.
        months: The number of months back from the current date to consider for file modification. Defaults to 3.

    Returns:
        A string containing the concatenated content of all recent files, with each file's content
        preceded by '--- {file_path} ---'.
    """
    return read_recent_files(path, months)

if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run(transport="http", host="127.0.0.1", port=8000)
