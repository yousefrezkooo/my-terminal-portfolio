import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define paths
blog_folder = r"C:\Users\yousi\OneDrive\المستندات\Obsidian Vault\blog"
output_file = r"C:\Users\yousi\OneDrive\Desktop\MISSY\portofolio\blog_posts.json"

def get_blog_posts():
    blog_posts = {}
    for filename in os.listdir(blog_folder):
        if filename.endswith(".md"):
            file_path = os.path.join(blog_folder, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                blog_posts[filename] = content  
    return blog_posts

def update_blog():
    blog_posts = get_blog_posts()
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(blog_posts, json_file, indent=4)
    print("Blog content updated!")

# File change handler
class BlogFolderHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".md"):
            print(f"Change detected: {event.src_path}")
            update_blog()

# Monitor folder
def start_monitoring():
    event_handler = BlogFolderHandler()
    observer = Observer()
    observer.schedule(event_handler, blog_folder, recursive=False)
    observer.start()
    
    print("Monitoring started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)  # Keep script running
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoring stopped.")
    
    observer.join()

if __name__ == "__main__":
    update_blog()  # Initial update
    start_monitoring()  # Start watching for changes
