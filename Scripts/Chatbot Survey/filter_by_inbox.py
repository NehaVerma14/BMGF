import os
import json
import csv
from datetime import datetime

def main():
    # Input directory
    input_directory = "Data/By_Date"

    # Output directory
    output_directory = "Data/By_Inbox"

    # Inbox IDs to analyze with corresponding names
    inbox_ids_and_names = {
        262: 'Human',
        266: 'PGPT1',
        267: 'PGPT2',
        270: 'VGPT1',
        271: 'VGPT2',
        268: 'POS1',
        269: 'POS2',
        272: 'VOS1',
        273: 'VOS2',
        274: 'VOGPT1',
        275: 'VOGPT2'
    }

    # Initialize a list to store the summary rows
    summary_rows = []

    # Loop through each JSON file in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".json"):
            file_path = os.path.join(input_directory, file_name)

            # Read and parse the JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Loop through each inbox_id and save conversations
            for inbox_id, inbox_name in inbox_ids_and_names.items():
                conversations_for_inbox = []

                for conversation_list in data:
                    for conversation in conversation_list:
                        if 'inbox_id' in conversation and conversation['inbox_id'] == inbox_id:
                            conversations_for_inbox.append([conversation])

                # Save conversations for the current inbox_id if there is data
                if conversations_for_inbox:
                    folder_path = os.path.join(output_directory, f"{inbox_name}")
                    os.makedirs(folder_path, exist_ok=True)

                    # Save individual conversations as JSON file
                    conversation_file_name = f"{file_name}"
                    output_file_path = os.path.join(folder_path, conversation_file_name)
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        json.dump(conversations_for_inbox, output_file, ensure_ascii=False, indent=4)

                    # Update the summary list with file name, date, and inbox_id
                    summary_rows.append([inbox_id, inbox_name,file_name, len(conversations_for_inbox) ])

    # Sort the summary rows by Inbox_ID, File_name, and Date in ascending order
    summary_rows.sort(key=lambda x: (x[0], x[2], x[-1]))

    # Save the sorted summary to a single CSV file
    summary_csv_file_name = "Results/Bot_Survey/summary_all_inboxes.csv"
    with open(summary_csv_file_name, 'w', encoding='utf-8', newline='') as summary_csv_file:
        csv_writer = csv.writer(summary_csv_file)
        csv_writer.writerow(['Inbox_ID', 'Folder_name', 'File_name', 'Count'])
        csv_writer.writerows(summary_rows)

if __name__ == "__main__":
    main()
