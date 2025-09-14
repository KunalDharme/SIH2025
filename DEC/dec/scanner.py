import subprocess
import os
import mimetypes

JAVA_HASHER = os.path.join("java", "Hasher.jar")

def get_file_hash(file_path):
    try:
        result = subprocess.run(
            ["java", "-jar", JAVA_HASHER, file_path],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Hashing failed for {file_path}: {e}")
        return None

def scan_directory(source_path):
    files_data = []
    for root, _, files in os.walk(source_path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                size = os.path.getsize(full_path)
                mime_type, _ = mimetypes.guess_type(full_path)
                file_hash = get_file_hash(full_path)
                files_data.append({
                    "path": full_path,
                    "size": size,
                    "mime": mime_type or "unknown",
                    "hash": file_hash
                })
            except Exception as e:
                print(f"Error reading {full_path}: {e}")
    return files_data
