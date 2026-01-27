#!/usr/bin/env python3
"""Upload files to GitHub Pages repo using GitHub API"""
import base64
import json
import subprocess
import sys
from pathlib import Path

REPO = "rc979/EEIntake-Pages"
SOURCE_DIR = Path(__file__).parent.parent.parent / "gh-pages-ready"

def upload_file(file_path: Path, repo_path: str) -> bool:
    """Upload file via gh API"""
    try:
        content_b64 = base64.b64encode(file_path.read_bytes()).decode('utf-8')
        
        # Check if file exists to get SHA for update
        check_cmd = ["gh", "api", f"repos/{REPO}/contents/{repo_path}"]
        check_result = subprocess.run(check_cmd, capture_output=True, text=True)
        
        cmd = ["gh", "api", "-X", "PUT", f"repos/{REPO}/contents/{repo_path}",
               "-f", f"message=Add {repo_path}",
               "-f", f"content={content_b64}"]
        
        # If file exists, get SHA and update
        if check_result.returncode == 0:
            data = json.loads(check_result.stdout)
            sha = data.get("sha")
            if sha:
                cmd.extend(["-f", f"sha={sha}"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        return False

def main():
    files = [f for f in SOURCE_DIR.rglob("*") if f.is_file() and ".git" not in str(f)]
    
    print(f"Uploading {len(files)} files...")
    uploaded = 0
    
    for file_path in files[:20]:  # Upload first 20 to test
        rel_path = file_path.relative_to(SOURCE_DIR)
        repo_path = str(rel_path).replace("\\", "/")
        
        if upload_file(file_path, repo_path):
            uploaded += 1
            print(f"✓ {repo_path}")
        else:
            print(f"✗ {repo_path}")
    
    print(f"\nUploaded {uploaded}/{len(files)} files")
    if uploaded > 0:
        print("✅ Success! Continuing with remaining files...")
        # Upload rest in batches
        for file_path in files[20:]:
            rel_path = file_path.relative_to(SOURCE_DIR)
            repo_path = str(rel_path).replace("\\", "/")
            if upload_file(file_path, repo_path):
                uploaded += 1
            if uploaded % 10 == 0:
                print(f"Progress: {uploaded}/{len(files)}")
    
    print(f"\n✅ Total uploaded: {uploaded}/{len(files)}")

if __name__ == "__main__":
    main()
