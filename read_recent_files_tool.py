import os
import datetime

def read_recent_files(path: str = os.path.expanduser("~/diary"), months: int = 3) -> str:
    """
    Reads and concatenates the content of files modified within the last 'months' from the specified path.

    Args:
        path: The absolute path to the directory to search within. Defaults to the user's diary directory.
        months: The number of months back from the current date to consider for file modification. Defaults to 3.

    Returns:
        A string containing the concatenated content of all recent files, with each file's content
        preceded by '--- {file_path} ---'.
    """
    concatenated_content = []
    now = datetime.datetime.now()

    # Calculate the target month and year for the cutoff
    current_year, current_month = now.year, now.month
    
    target_month_num = current_month - (months - 1)
    target_year = current_year
    while target_month_num <= 0:
        target_month_num += 12
        target_year -= 1

    # Create a comparable date for the earliest month to include (e.g., Sept 1, 2025 for months=3 in Nov 2025)
    cutoff_comparison_date = datetime.datetime(target_year, target_month_num, 1)

    month_abbr_to_num = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    for root, _, files in os.walk(path):
        # Extract year and month from the path like '~/diary/2025/nov.2025'
        relative_path = os.path.relpath(root, path)
        parts = relative_path.split(os.sep)

        file_is_in_range = False
        if len(parts) >= 2:
            try:
                folder_year_str = parts[0] # e.g., "2025"
                folder_month_year_str = parts[1] # e.g., "nov.2025"
                
                # Check for format 'YYYY' (e.g., '2023')
                if folder_year_str.isdigit() and len(parts) >=3:
                    folder_month_str_val = parts[1].split('.')[0]
                    file_year = int(folder_year_str) 
                    file_month = month_abbr_to_num.get(folder_month_str_val.lower())
                elif folder_year_str.isdigit() and folder_month_year_str.lower().startswith('month'): # in this case month's subfolder names may be inconsistent
                    continue
                else: # Assuming format 'MON.YYYY' like 'nov.2025' directly under ~/diary
                    month_abbr = folder_month_year_str.split('.')[0]
                    file_month = month_abbr_to_num[month_abbr.lower()]
                    file_year = int(folder_month_year_str.split('.')[-1])


                if file_year and file_month:
                    folder_date = datetime.datetime(file_year, file_month, 1)
                    if folder_date >= cutoff_comparison_date:
                        file_is_in_range = True

            except (ValueError, KeyError) as e:
                # Handle cases where year/month cannot be parsed, or month abbr is not in map
                # print(f"Warning: Could not parse date from path segment '{relative_path}'. Skipping directory. Error: {e}")
                pass # Skip directories that don't match the expected naming convention

        if file_is_in_range or relative_path == ".": # Always check files directly in the base path or if folder is in range
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    # Check if it's a regular file
                    if os.path.isfile(file_path):
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        concatenated_content.append(f"--- {file_path} ---\n{content}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
                    continue


    if not concatenated_content:
        return "No files found or no files modified within the last 3 months in the specified directory."

    return "\n\n".join(concatenated_content)
