import os
import json
import csv
import pandas as pd

def count_attributes(json_data):
    counts = {}
    for conversation in json_data:
        for message in conversation:
            if "additional_attributes" in message and "browser" in message["additional_attributes"]:
                browser_info = message["additional_attributes"]["browser"]
                device_name = browser_info["device_name"]
                browser_name = browser_info["browser_name"]
                platform_name = browser_info["platform_name"]
                browser_version = browser_info["browser_version"]
                
                counts.setdefault("device_name", {}).setdefault(device_name, 0)
                counts["device_name"][device_name] += 1
                
                counts.setdefault("browser_name", {}).setdefault(browser_name, 0)
                counts["browser_name"][browser_name] += 1
                
                counts.setdefault("platform_name", {}).setdefault(platform_name, 0)
                counts["platform_name"][platform_name] += 1
                
                counts.setdefault("browser_version", {}).setdefault(browser_version, 0)
                counts["browser_version"][browser_version] += 1
                
    return counts

def write_to_csv(counts, attribute, filename, folder):
    output_filename = f"Results/Chatbot_Analysis/Devices/{folder}/{attribute}_counts.csv"
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Value", "Count"])
        for value, count in sorted(counts.items()):
            writer.writerow([value, count])

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            folder_name = filename.split('.')[0]
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                counts = count_attributes(json_data)
                for attribute, values in counts.items():
                    if not os.path.exists(f"Results/Chatbot_Analysis/Devices/{folder_name}"):
                        os.makedirs(f"/home/neha/Chatbot ANalysis/Results/Devices/{folder_name}")
                    write_to_csv(values, attribute, folder=folder_name, filename=filename)

def merge_csv(results_directory, folder_order):
    common_csv_dataframes = {}
    for folder_name in folder_order:
        folder_path = os.path.join(results_directory, folder_name)
        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".csv"):
                    file_path = os.path.join(folder_path, file_name)
                    df = pd.read_csv(file_path)
                    df = df.iloc[:, [0, 1]]
                    df.set_index("Value", inplace=True)
                    df.rename(columns={"Count": folder_name}, inplace=True)
                    common_csv_dataframes.setdefault(file_name, []).append(df)

    merged_dfs = {}
    for csv_file_name, dfs in common_csv_dataframes.items():
        merged_df = pd.concat(dfs, axis=1, ignore_index=False)
        merged_df = merged_df.reindex(columns=folder_order, fill_value=0)
        merged_df.reset_index(inplace=True)
        merged_folder_path = os.path.join(results_directory, "Merged")
        os.makedirs(merged_folder_path, exist_ok=True)
        output_file = os.path.join(merged_folder_path, f"{csv_file_name}_merged.csv")
        merged_df.to_csv(output_file, index=False)

    print("Merged CSV files have been saved to the 'Merged' folder.")

def main():
    input_directory = "Data"
    results_directory = "Results/Chatbot_Analysis/Devices/"
    folder_order = ["Phase1", "Phase2", "Total"]
    process_files(input_directory)
    merge_csv(results_directory, folder_order)

if __name__ == "__main__":
    main()
