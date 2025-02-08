import os
import json
import subprocess


def push_to_github():
    repo_path = r"C:\Users\yousi\OneDrive\Desktop\MISSY\portofolio"
    commit_message = "Auto-update blog content"

    try:
        # Navigate to the repo
        os.chdir(repo_path)

        # Run Git commands
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("✅ Blog content pushed to GitHub successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to GitHub: {e}")

# Call this function after saving the JSON & HTML files
push_to_github()
