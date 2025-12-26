import os
import re

# Configuration
folder_path = "."   # Current directory (or change to '_talks')
target_layout = "page"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Split Front Matter (YAML) and Body
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    
    if not match:
        print(f"Skipping {filepath}: No valid front matter found.")
        return

    yaml_block = match.group(1)
    body = match.group(2)
    yaml_lines = yaml_block.strip().split('\n')
    
    # 2. Update YAML: Add layout
    if not any(line.startswith('layout:') for line in yaml_lines):
        yaml_lines.insert(0, f'layout: {target_layout}')
    
    # 3. Update YAML: Add description
    if not any(line.startswith('description:') for line in yaml_lines):
        # Insert after title if possible, otherwise at end
        insert_idx = len(yaml_lines)
        for i, line in enumerate(yaml_lines):
            if line.startswith('title:'):
                insert_idx = i + 1
                break
        yaml_lines.insert(insert_idx, 'description: ""')

    # 4. Fix Broken Links in Body
    # This regex looks for:
    #   ] followed by (
    #   optional http/https domain
    #   then /files/
    #   then captures the filename
    
    # Pattern explanation:
    # \[.*?\]   -> matches the link text like [Slides]
    # \(        -> literal opening parenthesis
    # (?:https?://[^)]+)? -> non-capturing group for optional domain (e.g. https://github.io)
    # /files/   -> the old folder path we want to replace
    # ([^)]+)   -> capture the filename (everything until the closing paren)
    # \)        -> literal closing parenthesis
    
    # We use a simpler substitution approach to replace the path part specifically.
    # We replace "https://.../files/" or just "/files/" with "/assets/files/"
    
    new_body = re.sub(r'\(https?://.*?/files/', '(/assets/files/', body)
    new_body = re.sub(r'\(/files/', '(/assets/files/', new_body)

    # Reconstruct content
    new_yaml = '\n'.join(yaml_lines)
    new_content = f"---\n{new_yaml}\n---\n{new_body}"

    # Write back only if changes were made (simple check)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
    else:
        print(f"No changes needed for: {filepath}")

def main():
    count = 0
    # Walk through the directory
    for filename in os.listdir(folder_path):
        if filename.endswith(".md"):
            process_file(os.path.join(folder_path, filename))
            count += 1
    
    print(f"--- Processing Complete. Scanned {count} files. ---")

if __name__ == "__main__":
    main()
