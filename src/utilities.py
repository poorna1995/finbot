import json
import csv

def save_metadata(metadata, json_path):
    with open(json_path, "w") as f:
        json.dump(metadata, f, indent=4)

def save_csv(metadata, csv_path):
    with open(csv_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metadata.keys())
        writer.writeheader()
        writer.writerow(metadata)
