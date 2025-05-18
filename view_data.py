import os
import json

# Folder where data is saved
monitor_folder = './datas'

def read_data(filename):
    txt_file = os.path.join(monitor_folder, f"{filename}.txt")
    json_file = os.path.join(monitor_folder, f"{filename}.json")
    csv_file = os.path.join(monitor_folder, f"{filename}.csv")

    # Read .txt file
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            print(f"Text File Content: \n{f.read()}")

    # Read .json file
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            print(f"\nJSON File Content: \n{json.dump(json.load(f), indent=2)}")

    # Read .csv file
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            print(f"\nCSV File Content: \n{f.read()}")

if __name__ == "__main__":
    filename = input("Enter the filename to view data (without extension): ")
    read_data(filename)
