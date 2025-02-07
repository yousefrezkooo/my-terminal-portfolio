import os
import markdown
import json
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# My Obsidian blog folder
blog_folder = r"C:\Users\yousi\OneDrive\المستندات\Obsidian Vault\blog"
repo_path = r"C:\Users\yousi\OneDrive\Desktop\MISSY\portofolio"

# Function to convert Markdown to HTML
def convert_md_to_html(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        content = file.read()
        return markdown.markdown(content)

# Function to get blog posts
def get_blog_posts():
    if not os.path.exists(blog_folder):
        raise FileNotFoundError(f"Folder not found: {blog_folder}")

    posts = {}
    for file in os.listdir(blog_folder):
        if file.endswith(".md"):
            file_path = os.path.join(blog_folder, file)
            posts[file] = convert_md_to_html(file_path)
    return posts

# Save blog posts to JSON file
def save_blog_posts_to_json(blog_posts):
    with open("blog_posts.json", "w", encoding="utf-8") as file:
        json.dump(blog_posts, file, ensure_ascii=False, indent=4)

# Function to push changes to GitHub
def push_to_github():
    commit_message = "Auto-update blog content"
    os.chdir(repo_path)

    print("📤 Running Git commands...")  # Debugging print
    subprocess.run("git status", shell=True)  # Check if files are being tracked

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ Successfully pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git error: {e}")

    commit_message = "Auto-update blog content"

    try:
        os.chdir(repo_path)  # Navigate to the repo
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ Blog content pushed to GitHub successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error pushing to GitHub: {e}")

# Handler to monitor folder changes
class BlogFolderHandler(FileSystemEventHandler):
    def update_blog(self, action, file_path):
        """Updates blog and pushes changes to GitHub."""
        print(f"{action}: {file_path}")
        blog_posts = get_blog_posts()
        save_blog_posts_to_json(blog_posts)
        print("✅ Blog posts updated!")
        push_to_github()  # Push changes to GitHub

    def on_modified(self, event):
        print(f"🔄 File modified: {event.src_path}")  # Debugging print
        if event.src_path.endswith(".md"):
            self.update_blog("Updated", event.src_path)


    def on_created(self, event):
        if event.src_path.endswith(".md"):
            self.update_blog("New post added", event.src_path)

    def on_deleted(self, event):
        if event.src_path.endswith(".md"):
            self.update_blog("Post deleted", event.src_path)

# Start monitoring the blog folder
def start_monitoring():
    event_handler = BlogFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, blog_folder, recursive=False)
    observer.start()
    print("📡 Monitoring started... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Run the monitoring process
if __name__ == "__main__":
    blog_posts = get_blog_posts()
    save_blog_posts_to_json(blog_posts)
    print("📂 Initial blog posts saved to blog_posts.json.")
    start_monitoring()
