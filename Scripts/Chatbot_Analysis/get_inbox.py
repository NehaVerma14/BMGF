import json
import os
import csv

def count_conversations(file_path, inbox_ids_and_names):
    with open(file_path, "r") as file:
        data = json.load(file)

    # Initialize a dictionary to store the count of conversations for each inbox_id
    conversation_count = {inbox_ids_and_names[inbox_id]: 0 for inbox_id in inbox_ids_and_names}

    # Iterate through the conversations in the data
    for conversation_list in data:
        for conversation in conversation_list:
            inbox_id = conversation['inbox_id']
            inbox_name = inbox_ids_and_names.get(inbox_id, 'Unknown')
            # Increment the count for the corresponding inbox_id
            conversation_count[inbox_name] += 1

    return conversation_count

def main():
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
    directory = "Data/"
    output_directory = "Results/Chatbot_Analysis"
    file_order = ["Phase1.json", "Phase2.json", "Diyochat_1.json"]

    file_labels = {
        "Phase1.json": "Phase1",
        "Phase2.json": "Phase2",
        "BMGF.json": "Total",
    }

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # List to store all counts
    all_counts = []

    # Iterate through each file in the specified order
    for filename in file_order:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            print("Processing file:", file_path)
            counts = count_conversations(file_path, inbox_ids_and_names)
            # Update the "File" field with the desired label
            counts["File"] = file_labels.get(filename, filename)
            all_counts.append(counts)

    # Get all unique inbox names
    all_inbox_names = set()
    for counts in all_counts:
        all_inbox_names.update(counts.keys())
        
    # Define the order of fields for the CSV
    field_order = ["File","Human",  "VGPT1", "VGPT2", "VOGPT1", "VOGPT2", "PGPT1", "PGPT2","POS1", "VOS1", "POS2", "VOS2" ]

    # Write the counts to a CSV file
    output_file = os.path.join(output_directory, "conversation_counts.csv")
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_order, delimiter='\t')
        writer.writeheader()
        for counts in all_counts:
            writer.writerow(counts)

    print("Results have been saved to:", output_file)

if __name__ == "__main__":
    main()
