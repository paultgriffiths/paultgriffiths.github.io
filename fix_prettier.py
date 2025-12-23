import os
import re

# Directories to skip
SKIP_DIRS = {".git", "_site", ".jekyll-cache", ".sass-cache", "assets", "_includes", "_layouts", "_sass"}

def fix_markdown_files():
    print("--- 🧹 Scanning for .md files ---")
    
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
    modified = False

    # ---------------------------------------------------------
    # STEP 1: Separate Front Matter (Header) from Body
    # ---------------------------------------------------------
    # We use this regex to split the file into 3 parts:
    # Group 1: The Front Matter (starting with ---, ending with --- and a newline)
    # Group 2: The rest of the Body content
    split_pattern = r'(\A---\s*\n[\s\S]*?\n---\s*\n)(.*)'
    match = re.match(split_pattern, content, re.DOTALL)

    if match:
        front_matter = match.group(1)
        body = match.group(2)
        
        # -----------------------------------------------------
        # FIX A: Quote Dates (Only in Front Matter)
        # -----------------------------------------------------
        date_pattern = r'(^date:\s+)(?=[0-9])(.*?)\s*$'
        if re.search(date_pattern, front_matter, re.MULTILINE):
            front_matter = re.sub(date_pattern, r'\1"\2"', front_matter, flags=re.MULTILINE)
            modified = True
            print(f"📅 Fixed Date: {filepath}")

        # -----------------------------------------------------
        # FIX B: Ensure Blank Line After Front Matter
        # -----------------------------------------------------
        # If the body doesn't start with a newline (and isn't empty), add one.
        if len(body) > 0 and not body.startswith('\n'):
            body = '\n' + body
            modified = True
            print(f"⬇️  Fixed Header Spacing: {filepath}")

        # -----------------------------------------------------
        # FIX C: Fix Horizontal Rules in Body (---)
        # -----------------------------------------------------
        # Look for '---' on its own line that is NOT followed by a blank line.
        # \n---\s*\n  -> Newline, dashes, optional space, newline
        # (?!\n)      -> Negative lookahead: NOT followed by another newline
        hr_pattern = r'(\n---\s*\n)(?!\n)'
        
        if re.search(hr_pattern, body):
            body = re.sub(hr_pattern, r'\1\n', body)
            modified = True
            print(f"➖ Fixed Horizontal Rule Spacing: {filepath}")

        # Reconstruct content
        content = front_matter + body

    else:
        # If no front matter found, we treat the whole thing as body (rare for Jekyll)
        # You could apply generic formatting here if needed.
        pass

    # ---------------------------------------------------------
    # FIX D: Ensure EOF Newline
    # ---------------------------------------------------------
    if len(content) > 0 and not content.endswith('\n'):
        content += '\n'
        modified = True
        print(f"⏎  Fixed EOF : {filepath}")

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    if modified or content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_markdown_files()
