import os
import subprocess

# Change this to your repository's local path
repo_path = r"C:\Users\yousi\OneDrive\المستندات\Obsidian Vault\blog"

def run_command(command):
    """Run a shell command and handle errors."""
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr.strip()}")
        return None

def update_blog():
    """Automate Git process for updating blog content."""
    print("📤 Running Git commands...")

    # Change directory to the repo
    os.chdir(repo_path)

    # Add changes
    print("➕ Adding changes...")
    run_command(["git", "add", "."])

    # Commit changes
    print("📝 Committing changes...")
    commit_message = "Auto-update blog content"
    commit_result = run_command(["git", "commit", "-m", commit_message])
    if commit_result is None:
        print("❌ No changes to commit. Exiting...")
        return

    # Pull latest changes (to prevent push rejection)
    print("📥 Pulling latest changes...")
    pull_result = run_command(["git", "pull", "--rebase", "origin", "main"])
    if pull_result is None:
        print("⚠ Pull failed. Resolve conflicts before pushing.")
        return

    # Push changes
    print("📤 Pushing to GitHub...")
    push_result = run_command(["git", "push", "origin", "main"])
    if push_result:
        print("✅ Successfully pushed to GitHub!")

# Run the script
update_blog()
