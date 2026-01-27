#!/usr/bin/env python3
"""
Fast commit to GitHub Pages repo using Git Data API
Creates a single commit with all files at once
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

REPO = "rc979/EEIntake-Pages"
SOURCE_DIR = Path(__file__).parent.parent.parent / "gh-pages-ready"

def get_ref_sha(ref="heads/main"):
    """Get SHA of the ref"""
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/ref/{ref}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # Try alternative: get from commits API
        result2 = subprocess.run(
            ["gh", "api", f"repos/{REPO}/commits/main"],
            capture_output=True, text=True
        )
        if result2.returncode == 0:
            data = json.loads(result2.stdout)
            return data["sha"]
        return None
    data = json.loads(result.stdout)
    return data["object"]["sha"]

def create_blob(content_bytes):
    """Create a blob and return its SHA"""
    # Try to decode as UTF-8 first (for text files)
    try:
        content_text = content_bytes.decode('utf-8')
        # Use utf-8 encoding for text files
        payload = {"content": content_text, "encoding": "utf-8"}
    except UnicodeDecodeError:
        # Binary file - use base64
        content_b64 = base64.b64encode(content_bytes).decode('utf-8')
        payload = {"content": content_b64, "encoding": "base64"}
    
    result = subprocess.run(
        ["gh", "api", "-X", "POST", f"repos/{REPO}/git/blobs"],
        input=json.dumps(payload),
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    data = json.loads(result.stdout)
    return data["sha"]

def create_tree(base_tree_sha, tree_entries):
    """Create a tree and return its SHA"""
    payload = {"tree": tree_entries}
    if base_tree_sha:
        payload["base_tree"] = base_tree_sha
    
    result = subprocess.run(
        ["gh", "api", "-X", "POST", f"repos/{REPO}/git/trees"],
        input=json.dumps(payload),
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error creating tree: {result.stderr}", file=sys.stderr)
        return None
    data = json.loads(result.stdout)
    return data["sha"]

def create_commit(tree_sha, parent_sha, message):
    """Create a commit and return its SHA"""
    payload = {
        "message": message,
        "tree": tree_sha,
        "parents": [parent_sha] if parent_sha else []
    }
    
    result = subprocess.run(
        ["gh", "api", "-X", "POST", f"repos/{REPO}/git/commits"],
        input=json.dumps(payload),
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Error creating commit: {result.stderr}", file=sys.stderr)
        return None
    data = json.loads(result.stdout)
    return data["sha"]

def update_ref(ref, commit_sha):
    """Update ref to point to new commit"""
    payload = {"sha": commit_sha}
    result = subprocess.run(
        ["gh", "api", "-X", "PATCH", f"repos/{REPO}/git/refs/{ref}"],
        input=json.dumps(payload),
        capture_output=True, text=True
    )
    return result.returncode == 0

def main():
    print(f"Preparing to commit files from {SOURCE_DIR}...")
    
    # Get current HEAD
    head_sha = get_ref_sha("heads/main")
    if not head_sha:
        print("Error: Could not get current HEAD", file=sys.stderr)
        sys.exit(1)
    
    print(f"Current HEAD: {head_sha[:7]}")
    
    # Get base tree SHA
    commit_result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/git/commits/{head_sha}"],
        capture_output=True, text=True
    )
    base_tree_sha = None
    if commit_result.returncode == 0:
        commit_data = json.loads(commit_result.stdout)
        base_tree_sha = commit_data["tree"]["sha"]
    
    # Collect all files
    files = [f for f in SOURCE_DIR.rglob("*") if f.is_file() and ".git" not in str(f)]
    print(f"Processing {len(files)} files...")
    
    # Create blobs and tree entries
    tree_entries = []
    for i, file_path in enumerate(files):
        rel_path = file_path.relative_to(SOURCE_DIR)
        repo_path = str(rel_path).replace("\\", "/")
        
        # Skip .DS_Store files
        if repo_path.endswith(".DS_Store"):
            continue
        
        print(f"Creating blob {i+1}/{len(files)}: {repo_path}", end="\r")
        
        content = file_path.read_bytes()
        blob_sha = create_blob(content)
        
        if blob_sha:
            tree_entries.append({
                "path": repo_path,
                "mode": "100644",
                "type": "blob",
                "sha": blob_sha
            })
        else:
            print(f"\nWarning: Failed to create blob for {repo_path}", file=sys.stderr)
    
    print(f"\nCreated {len(tree_entries)} blobs")
    
    # Create tree
    print("Creating tree...")
    tree_sha = create_tree(base_tree_sha, tree_entries)
    if not tree_sha:
        print("Error: Failed to create tree", file=sys.stderr)
        sys.exit(1)
    
    print(f"Tree SHA: {tree_sha[:7]}")
    
    # Create commit
    print("Creating commit...")
    commit_sha = create_commit(tree_sha, head_sha, f"Update Pages site from main repo")
    if not commit_sha:
        print("Error: Failed to create commit", file=sys.stderr)
        sys.exit(1)
    
    print(f"Commit SHA: {commit_sha[:7]}")
    
    # Update ref
    print("Updating ref...")
    if update_ref("heads/main", commit_sha):
        print(f"\n✅ Successfully committed and pushed!")
        print(f"Commit: https://github.com/{REPO}/commit/{commit_sha}")
        print(f"Site: https://rc979.github.io/EEIntake-Pages/")
    else:
        print("Error: Failed to update ref", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
