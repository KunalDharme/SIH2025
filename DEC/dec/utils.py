import os
import shutil
from tqdm import tqdm

def copy_file(src, dest_folder):
    """
    Copy file from src to dest_folder. Creates folder if missing.
    """
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, os.path.basename(src))
    try:
        shutil.copy2(src, dest_path)
        return dest_path
    except Exception as e:
        print(f"Copy failed for {src}: {e}")
        return None

def copy_with_progress(files, dest_root):
    """
    Copy multiple files with progress bar.
    Returns list of copied file paths.
    """
    copied_files = []
    for f in tqdm(files, desc="Copying files", unit="file"):
        category = f["category"]
        dest_folder = os.path.join(dest_root, category.capitalize())
        new_path = copy_file(f["path"], dest_folder)
        if new_path:
            copied_files.append(new_path)
    return copied_files
