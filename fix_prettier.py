import os
import re

# Directories to skip to avoid breaking site builds or git
SKIP_DIRS = {".git", "_site", ".jekyll-cache", ".sass-cache", "assets", "_includes", "_layouts", "_sass"}

def fix_markdown_files():
    print("--- 🧹 Scanning for .md files ---")
    
    for root, dirs, files in os.walk("."):
        # Prevent walking into skip directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                fix_single_file(filepath)

    print("--- ✨ Done ---")

def fix_single_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️  Skipped {filepath}: {e}")
        return

    original_content = content
    modified = False

    # ---------------------------------------------------------
    # FIX 1: Quote UNQUOTED dates only
    # ---------------------------------------------------------
    # Logic:
    # ^date:\s+   -> Find 'date:' at start of line followed by space
    # (?=[0-9])   -> LOOKAHEAD: Ensure the next character is a DIGIT (0-9)
    # (.*?)       -> Capture the date content
    # \s*$        -> Handle end of line
    #
    # If the date starts with " or ', the lookahead (?=[0-9]) fails, 
    # so it skips the line.
    # ---------------------------------------------------------
    date_pattern = r'(^date:\s+)(?=[0-9])(.*?)\s*$'
    
    if re.search(date_pattern, content, re.MULTILINE):
        # Result: date: "2025-01-04 08:59:00"
        content = re.sub(date_pattern, r'\1"\2"', content, flags=re.MULTILINE)
        
        # Double check we actually changed something
        if content != original_content:
            modified = True
            print(f"📅 Fixed Date: {filepath}")

    # ---------------------------------------------------------
    # FIX 2: Add single newline at end of file (EOF)
    # ---------------------------------------------------------
    if len(content) > 0 and not content.endswith('\n'):
        content += '\n'
        modified = True
        print(f"⏎  Fixed EOF : {filepath}")

    # Save
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_markdown_files()
