import os
import markdown
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# My Obsidian blog folder (fixed path issue)
blog_folder = r"C:\Users\yousi\OneDrive\المستندات\Obsidian Vault\blog"

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

# Handler to monitor folder changes
class BlogFolderHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".md"):
            print(f"Updated: {event.src_path}")
            blog_posts = get_blog_posts()
            save_blog_posts_to_json(blog_posts)
            print("Blog posts updated!")

    def on_created(self, event):
        if event.src_path.endswith(".md"):
            print(f"New post added: {event.src_path}")
            blog_posts = get_blog_posts()
            save_blog_posts_to_json(blog_posts)
            print("Blog posts updated!")

    def on_deleted(self, event):
        if event.src_path.endswith(".md"):
            print(f"Post deleted: {event.src_path}")
            blog_posts = get_blog_posts()
            save_blog_posts_to_json(blog_posts)
            print("Blog posts updated!")

# Start monitoring the blog folder
def start_monitoring():
    event_handler = BlogFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, blog_folder, recursive=False)
    observer.start()
    print("Monitoring started... Press Ctrl+C to stop.")

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
    print("Initial blog posts saved to blog_posts.json.")
    start_monitoring()
# This script monitors a folder for changes (additions, modifications, deletions) and updates a JSON file with the blog posts found in that folder. The blog posts are converted from Markdown to HTML using the Python markdown library. The script uses the watchdog library to monitor the folder and trigger events when changes occur. The BlogFolderHandler class defines event handlers for file modifications, creations, and deletions. The start_monitoring function sets up the observer and event handler, and starts the monitoring process. The script also includes functions to convert Markdown to HTML, get blog posts from the folder, and save the blog posts to a JSON file. The main block initializes the blog posts, saves them to a JSON file, and starts the monitoring process. The script can be run as a standalone program to monitor a specific folder for blog post changes.


import os
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
# This script automates the process of pushing the updated blog content to a GitHub repository. The push_to_github function defines the steps to add, commit, and push the changes to the main branch of the specified repository. The repo_path variable should be updated with the local path to the GitHub repository. The commit_message variable specifies the commit message to be used for the changes. The function uses the subprocess module to run Git commands in the specified repository directory. After saving the JSON and HTML files, the push_to_github function can be called to automatically push the changes to the GitHub repository.