import json
# import pandas as pd
from datetime import datetime

def modify_and_save_json(input_file, output_directory):
    # Load data from the input JSON file
    with open(input_file, 'r', encoding='utf-8') as file:
        diyochat_data = json.load(file)


    # Save the modified JSON file
    output_file = output_directory + "/BMGF.json"
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(diyochat_data, file, indent=4, ensure_ascii=False)

    print("Modified JSON file has been saved successfully at:", output_file)
    return output_file

def extract_conversations(file_path, cutoff_date):
    with open(file_path, "r") as file:
        data = json.load(file)

    conversations_before_cutoff = []
    conversations_after_cutoff = []

    for conversation_set in data:
        for conversation in conversation_set:
            initiated_at_timestamp = conversation['additional_attributes']['initiated_at']['timestamp']
            initiated_at_date_str = initiated_at_timestamp.split(' ')[1:4]
            initiated_at_date_str = ' '.join(initiated_at_date_str)
            initiated_at = datetime.strptime(initiated_at_date_str, "%b %d %Y").date()
            
            if initiated_at < cutoff_date:
                conversations_before_cutoff.append([conversation])
            else:
                conversations_after_cutoff.append([conversation])

    return conversations_before_cutoff, conversations_after_cutoff

def main():
    # Define file path and cutoff date
    input_file_path = "Data/BMGF.json"
    output_directory = "Data"
    cutoff_date = datetime.strptime("2024-01-22", "%Y-%m-%d").date()

    # Modify and save JSON file
    modified_file_path = modify_and_save_json(input_file_path, output_directory)

    # Extract conversations from the modified JSON file
    conversations_before_cutoff, conversations_after_cutoff = extract_conversations(modified_file_path, cutoff_date)
    
    print("Number of conversations before {}: {}".format(cutoff_date, len(conversations_before_cutoff)))
    print("Number of conversations after {}: {}".format(cutoff_date, len(conversations_after_cutoff)))
    
    # Dump conversations before cutoff into a JSON file
    with open(output_directory + "/Phase1.json", "w", encoding="utf-8") as file:
        json.dump(conversations_before_cutoff, file, indent=4, ensure_ascii=False)

    # Dump conversations after cutoff into a JSON file
    with open(output_directory + "/Phase2.json", "w", encoding="utf-8") as file:
        json.dump(conversations_after_cutoff, file, indent=4, ensure_ascii=False)

    print("JSON files have been created successfully.")

if __name__ == "__main__":
    main()
