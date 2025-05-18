import os
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Folder to monitor
monitor_folder = './datas'

# Create folder if it doesn't exist
if not os.path.exists(monitor_folder):
    os.makedirs(monitor_folder)

# Save data in a readable format
def save_data(filename, data):
    # Assuming we save everything as text, but you can customize based on data
    txt_file = os.path.join(monitor_folder, f"{filename}.txt")
    json_file = os.path.join(monitor_folder, f"{filename}.json")
    csv_file = os.path.join(monitor_folder, f"{filename}.csv")

    # Saving as a text file
    with open(txt_file, 'w') as f:
        f.write(str(data))

    # Saving as a JSON file
    with open(json_file, 'w') as f:
        json.dump(data, f)

    # Saving as a CSV file
    with open(csv_file, 'w') as f:
        if isinstance(data, dict):
            for key, value in data.items():
                f.write(f"{key},{value}\n")
        else:
            for item in data:
                f.write(f"{item}\n")
    
    print(f"Data saved as {txt_file}, {json_file}, {csv_file}")

# Event handler class to monitor changes
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            filename = os.path.basename(event.src_path)
            # You can process the content of the file as per your requirement
            with open(event.src_path, 'r') as f:
                data = f.read()
                save_data(filename, data)

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            filename = os.path.basename(event.src_path)
            # You can process the content of the file as per your requirement
            with open(event.src_path, 'r') as f:
                data = f.read()
                save_data(filename, data)

# Watch the folder for changes
def monitor_folder_changes():
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=monitor_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    monitor_folder_changes()
