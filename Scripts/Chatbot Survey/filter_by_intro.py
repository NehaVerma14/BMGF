import os
import json
import csv
from collections import defaultdict
from pathlib import Path

def process_json_file(file_path):
    intro_counts = defaultdict(int)

    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for convo in data:
            for message in convo:
                if "meta" in message and "sender" in message["meta"]:
                    # Use get method to handle the KeyError
                    intro = message["meta"]["sender"]["custom_attributes"].get("intro", "Unknown")
                    intro_counts[intro] += 1

    return intro_counts

def write_combined_csv(output_csv_path, combined_intro_counts):
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        intro_list = ["महिला स्वास्थ्य स्वयमसेविका", "स्थानीय", "विद्यार्थी"]
        csv_writer.writerow(["File Name"] + intro_list + ['General Public'])  # Header

        for file_name, intro_counts in combined_intro_counts.items():
            row = [file_name]
            for intro in intro_list:
                row.append(intro_counts.get(intro, 0))
            row.append(row[2] + row[3])  # Adding 'General Public' count
            csv_writer.writerow(row)

def process_directory(input_directory):
    for subdir, _, files in os.walk(input_directory):
        json_files = [file for file in files if file.endswith(".json")]

        if json_files:
            # Create 'csv' folder inside the directory containing JSON files
            csv_folder = os.path.join(subdir, "csv")
            os.makedirs(csv_folder, exist_ok=True)

            combined_intro_counts = defaultdict(lambda: defaultdict(int))

            for file in json_files:
                file_path = Path(subdir) / file
                intro_counts = process_json_file(file_path)

                # Combine intro counts from multiple JSON files
                for intro, count in intro_counts.items():
                    combined_intro_counts[file].update({intro: count})

            # Save combined CSV file inside 'csv' folder
            output_csv_path = os.path.join(csv_folder, "combined_intro_counts.csv")
            write_combined_csv(output_csv_path, combined_intro_counts)

            print(f"Intro counts for {json_files} have been written to {output_csv_path}")

def main():
    input_directory = "Data/By_Turn"
    process_directory(input_directory)

if __name__ == "__main__":
    main()
