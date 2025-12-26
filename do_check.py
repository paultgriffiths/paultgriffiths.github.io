import os

# 1. Where are your assets stored?
ASSET_DIR = "assets"

# 2. Which file types should we scan for references? (The code files)
# We search INSIDE these files to see if they mention an image/pdf.
SEARCH_EXTENSIONS = {'.md', '.html', '.yml', '.yaml', '.json', '.liquid', '.xml', '.js', '.css'}

# 3. Directories to exclude from the search (to save time/noise)
SKIP_DIRS = {'.git', '_site', '.jekyll-cache', '.sass-cache', 'node_modules'}

def get_all_assets(directory):
    """Recursively finds all files in the assets directory."""
    asset_files = {}
    for root, _, files in os.walk(directory):
        for file in files:
            # key = filename (e.g., 'profile.jpg'), value = full relative path
            # We use filename as the key because sometimes you just link 'profile.jpg'
            asset_files[file] = os.path.join(root, file)
    return asset_files

def find_unused_assets():
    print(f"--- 🕵️‍♀️ Scanning {ASSET_DIR}/ for files... ---")
    assets = get_all_assets(ASSET_DIR)
    total_assets = len(assets)
    print(f"Found {total_assets} asset files.")

    # We will remove assets from this set as we find references to them
    unused_candidates = set(assets.keys())

    print("--- 🔍 Searching source files for references... ---")
    for root, dirs, files in os.walk("."):
        # Skip system directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for file in files:
            # Only read text-based source files
            ext = os.path.splitext(file)[1]
            if ext in SEARCH_EXTENSIONS:
                filepath = os.path.join(root, file)
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Check against our list of remaining candidates
                        # We iterate over a COPY (list) so we can modify the set
                        for asset_name in list(unused_candidates):
                            if asset_name in content:
                                # Found a mention! Remove from candidates.
                                unused_candidates.remove(asset_name)
                except Exception as e:
                    # Skip binary files or weird encoding errors
                    continue
        
        # Optimization: If we found everything, stop early
        if not unused_candidates:
            break

    print("--- 📋 Results ---")
    if not unused_candidates:
        print("✅ Amazing! Every single file in assets/ is being used.")
    else:
        print(f"⚠️  Found {len(unused_candidates)} files that might be unused:")
        print("-" * 40)
        # Sort them by their full path for easier reading
        orphans = []
        for name in unused_candidates:
            orphans.append(assets[name])
        
        for path in sorted(orphans):
            print(path)
        print("-" * 40)
        print("💡 NOTE: Double-check these before deleting! (e.g., make sure they aren't favicons or backgrounds defined in CSS)")

if __name__ == "__main__":
    find_unused_assets()
