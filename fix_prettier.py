import os
import re

# Directories to skip
SKIP_DIRS = {".git", "_site", ".jekyll-cache", ".sass-cache", "assets", "_includes", "_layouts", "_sass"}

def fix_markdown_files():
    print("--- 🧹 Scanning for .md files to normalize spacing ---")
    
    for root, dirs, files in os.walk("."):
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
    
    # ---------------------------------------------------------
    # STEP 1: Identify Front Matter and Body
    # ---------------------------------------------------------
    # Matches the YAML block at the start of the file: ^--- ... ---
    fm_pattern = r'(\A---\s*\n[\s\S]*?\n---)'
    match = re.match(fm_pattern, content, re.DOTALL)

    if match:
        front_matter = match.group(1)
        # Get everything after the front matter
        body = content[match.end():]

        # -----------------------------------------------------
        # FIX A: Quote Dates in Front Matter
        # -----------------------------------------------------
        date_pattern = r'(^date:\s+)(?=[0-9])(.*?)\s*$'
        if re.search(date_pattern, front_matter, re.MULTILINE):
            front_matter = re.sub(date_pattern, r'\1"\2"', front_matter, flags=re.MULTILINE)

        # -----------------------------------------------------
        # FIX B: Normalize Horizontal Rules in BODY
        # -----------------------------------------------------
        # This regex finds:
        # 1. Start of line (?m)^
        # 2. The dashes '---'
        # 3. Optional spaces/tabs
        # 4. The newline immediately following it
        # 5. ALL subsequent whitespace (\s*)
        # It replaces all of that with '---\n\n' (Force exactly 1 blank line)
        body = re.sub(r'(?m)^---[ \t]*\n\s*', '---\n\n', body)

        # -----------------------------------------------------
        # FIX C: Normalize Header Spacing
        # -----------------------------------------------------
        # Strip all leading newlines from the body so we can control the gap
        body = body.lstrip('\n\r')
        
        # Reconstruct: Front Matter + 2 Newlines (1 blank line) + Body
        if len(body) > 0:
            content = front_matter + '\n\n' + body
        else:
            content = front_matter + '\n'

    # ---------------------------------------------------------
    # FIX D: Ensure EOF Newline
    # ---------------------------------------------------------
    if len(content) > 0 and not content.endswith('\n'):
        content += '\n'
    # Check if there are multiple newlines at EOF and trim to one
    while content.endswith('\n\n'):
        content = content[:-1]

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"🔧 Fixed: {filepath}")

if __name__ == "__main__":
    fix_markdown_files()
