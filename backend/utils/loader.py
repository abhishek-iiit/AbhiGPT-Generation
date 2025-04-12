import os

def load_code_files(repo_path, extensions=('.py', '.js', '.java')):
    code_files = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(extensions):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    code_files.append(f.read())
    return code_files
