import json
import csv
import os

def process_json_file(json_file, turn_counts):
    with open(json_file, 'r', encoding='utf-8') as file:
        diyochat_data = json.load(file)

    file_turn_counts = {}

    for conversation in diyochat_data:
        messages = conversation[0]['messages']
        turn_count = 0  
        last_sender_type = None  

        for message in messages:
            sender_type = message['sender']['type']

            if sender_type != last_sender_type:
                turn_count += 1

            last_sender_type = sender_type

        if turn_count in file_turn_counts:
            file_turn_counts[turn_count] += 1
        else:
            file_turn_counts[turn_count] = 1

    for turn_count, count in file_turn_counts.items():
        if turn_count in turn_counts:
            turn_counts[turn_count].append(count)
        else:
            turn_counts[turn_count] = [count]

def main():
    output_directory = 'Results/Chatbot_Analysis/Turn'
    os.makedirs(output_directory, exist_ok=True)

    turn_counts = {}

    file_names = {
        "Data/Phase1.json": "Phase 1",
        "Data/Phase2.json": "Phase 2",
        "Data/BMGF.json": "Total"
    }

    json_files = list(file_names.keys())

    for json_file in json_files:
        process_json_file(json_file, turn_counts)

    sorted_turn_counts = sorted(turn_counts.items())

    output_csv_file = os.path.join(output_directory, 'combined_turn_counts.csv')
    with open(output_csv_file, 'w', newline='') as csvfile:
        fieldnames = ['Turn Count'] + [f'{file_names[json_file]}' for json_file in json_files]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for turn_count, counts_list in sorted_turn_counts:
            row_data = {'Turn Count': turn_count}
            for i, count in enumerate(counts_list):
                row_data[f'{file_names[json_files[i]]}'] = count
            writer.writerow(row_data)

    print(f"CSV file '{output_csv_file}' has been created with turn counts from all JSON files.")

if __name__ == "__main__":
    main()
