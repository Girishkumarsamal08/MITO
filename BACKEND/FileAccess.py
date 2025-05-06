import os

def list_all_files(start_path="/", max_depth=5):
    result = []
    def _walk(path, depth):
        if depth > max_depth:
            return
        try:
            for entry in os.scandir(path):
                if entry.is_dir(follow_symlinks=False):
                    _walk(entry.path, depth + 1)
                else:
                    result.append(entry.path)
        except Exception as e:
            pass  # Permissions or hidden folders
    _walk(start_path, 0)
    return result
