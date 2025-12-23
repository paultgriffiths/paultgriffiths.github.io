import os
import re

# Directories to skip
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
    # FIX 1: Quote UNQUOTED dates
    # ---------------------------------------------------------
    # Looks for 'date: 2025...' (starting with digit) and quotes it.
    date_pattern = r'(^date:\s+)(?=[0-9])(.*?)\s*$'
    if re.search(date_pattern, content, re.MULTILINE):
        new_content = re.sub(date_pattern, r'\1"\2"', content, flags=re.MULTILINE)
        if new_content != content:
            content = new_content
            modified = True
            print(f"📅 Fixed Date: {filepath}")

    # ---------------------------------------------------------
    # FIX 2: Insert Blank Line After Front Matter
    # ---------------------------------------------------------
    # Looks for the Front Matter block (\A...---) that is NOT followed by a newline.
    # \A        = Start of file
    # [\s\S]*?  = Non-greedy match of any char (including newlines)
    # (?!\n)    = Negative Lookahead: Next char is NOT a newline
    fm_pattern = r'(\A---\s*\n[\s\S]*?\n---\s*\n)(?!\n)'
    
    if re.search(fm_pattern, content):
        # We replace the block with itself + a newline (\n)
        content = re.sub(fm_pattern, r'\1\n', content, count=1)
        modified = True
        print(f"↔️  Fixed Space: {filepath}")

    # ---------------------------------------------------------
    # FIX 3: Add single newline at EOF
    # ---------------------------------------------------------
    if len(content) > 0 and not content.endswith('\n'):
        content += '\n'
        modified = True
        print(f"⏎  Fixed EOF : {filepath}")

    # ---------------------------------------------------------
    # SAVE (Only if changes were made)
    # ---------------------------------------------------------
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_markdown_files()
