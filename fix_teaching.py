import os
import frontmatter

# Path to your teaching directory
TEACHING_DIR = "./_teaching"

def fix_teaching_files():
    print(f"--- Fixing Teaching Files in {TEACHING_DIR} ---")
    
    if not os.path.exists(TEACHING_DIR):
        print("Error: Directory not found.")
        return

    for filename in os.listdir(TEACHING_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(TEACHING_DIR, filename)
            try:
                post = frontmatter.load(filepath)
                modified = False

                # 1. FIX LAYOUT
                # Change old layouts (archive, single, etc) to standard 'page'
                if post.metadata.get('layout') != 'page':
                    post.metadata['layout'] = 'page'
                    modified = True

                # 2. CLEANUP SIDEBARS
                # academic-pages sidebars break al-folio width
                if 'sidebar' in post.metadata:
                    del post.metadata['sidebar']
                    modified = True

                # 3. ENSURE PERMALINK (Optional safety)
                # If permalink is missing, al-folio might guess wrong. 
                # Usually safely ignored if collections config is correct, 
                # but good to clean if it points to old structure.
                
                if modified:
                    with open(filepath, 'wb') as f:
                        frontmatter.dump(post, f)
                    print(f"Fixed: {filename}")
            
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print("\nTeaching files updated.")

if __name__ == "__main__":
    fix_teaching_files()
