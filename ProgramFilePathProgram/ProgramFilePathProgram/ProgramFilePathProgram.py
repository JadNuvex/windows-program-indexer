
import os
import json
from tqdm import tqdm

# Directories to search
DIRECTORIES_TO_SCAN = [
    r"C:\Program Files",
    r"C:\Program Files (x86)"
]

# Keywords to skip executables that are likely installers or not primary programs
SKIP_EXE_KEYWORDS = ["setup", "install", "uninstall"]

def should_skip_exe(filename):
    """Return True if this exe should be skipped based on keywords."""
    fname_lower = filename.lower()
    for kw in SKIP_EXE_KEYWORDS:
        if kw in fname_lower:
            return True
    return False

def count_entries(directories):
    """Count how many files and folders in the given directories."""
    print("[INFO]: Counting files and folders...")
    file_count = 0
    folder_count = 0
    for base_directory in directories:
        for root, dirs, files in os.walk(base_directory):
            folder_count += len(dirs)
            file_count += len(files)
    total = file_count + folder_count
    print(f"[INFO]: Found {file_count} files and {folder_count} folders to index across all directories.")
    return total, file_count, folder_count

def index_programs(directories, total):
    """
    Recursively walk through the given directories and index only .exe files 
    that are not installers (no setup/install/uninstall in their name).
    Returns a dictionary mapping filename keys to their full paths.
    """
    program_map = {}
    processed_count = 0

    with tqdm(total=total, desc="Indexing", unit="entry") as pbar:
        for base_directory in directories:
            for root, dirs, files in os.walk(base_directory):
                for filename in files:
                    processed_count += 1
                    pbar.update(1)
                    
                    # Check if it's an .exe
                    if filename.lower().endswith('.exe'):
                        if not should_skip_exe(filename):
                            key = filename.lower()
                            full_path = os.path.abspath(os.path.join(root, filename))
                            
                            # Handle duplicates
                            original_key = key
                            counter = 2
                            while key in program_map:
                                key = f"{original_key}_{counter}"
                                counter += 1
                            
                            program_map[key] = full_path
    return program_map

def main():
    total, file_count, folder_count = count_entries(DIRECTORIES_TO_SCAN)
    if total == 0:
        print("[INFO]: No files or folders found. Exiting.")
        return

    program_map = index_programs(DIRECTORIES_TO_SCAN, total)
    print(f"[INFO]: Indexed {len(program_map)} .exe programs after filtering.")

    # Save to JSON file
    with open("programs.json", 'w', encoding='utf-8') as f:
        json.dump(program_map, f, indent=4, ensure_ascii=False)
    print("[INFO]: programs.json saved.")

    print("[INFO]: Done!")

if __name__ == "__main__":
    main()
