import os
import json
import csv

def process_json_file(file_path, intros):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        enumerator_counts = {}

        for messages in data:
            for message in messages:
                if 'meta' in message and 'sender' in message['meta'] and 'custom_attributes' in message['meta']['sender']:
                    intro = message['meta']['sender']['custom_attributes'].get('intro', None)
                    enumerator = message['meta']['sender']['custom_attributes'].get('enumerator', None)

                    if intro in intros and enumerator is not None:
                        if enumerator not in enumerator_counts:
                            enumerator_counts[enumerator] = {intro: 0 for intro in intros}

                        enumerator_counts[enumerator][intro] = enumerator_counts[enumerator].get(intro, 0) + 1

        return enumerator_counts

def process_directory(input_directory, intros, all_enumerators):
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                enumerator_counts = process_json_file(file_path, intros)

                # Ensure all enumerators are included
                for enumerator in all_enumerators:
                    if enumerator not in enumerator_counts:
                        enumerator_counts[enumerator] = {intro: 0 for intro in intros}

                # Save results to CSV file
                output_directory = os.path.join(root, 'csv')
                os.makedirs(output_directory, exist_ok=True)
                output_file = os.path.join(output_directory, f'{file.replace(".json", "")}_results.csv')

                with open(output_file, 'w', newline='') as csvfile:
                    fieldnames = ['Enumerator'] + [f'{intro}' for intro in intros] + ['General Public']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for enumerator, counts in sorted(enumerator_counts.items(), key=lambda x: int(x[0])):
                        row_data = {'Enumerator': enumerator}
                        row_data.update(counts)
                        
                        # Sum values of स्थानीय and विद्यार्थी columns
                        row_data['General Public'] = row_data.get('स्थानीय', 0) + row_data.get('विद्यार्थी', 0)
                        
                        writer.writerow(row_data)

def main():
    input_directory = "Data/By_Turn"
    intros = ["महिला स्वास्थ्य स्वयमसेविका", "स्थानीय", "विद्यार्थी"]

    # Define all enumerators
    all_enumerators = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 27, 29,
        30, 9861439198, 9877, 89989, 1234, 9842629680, 1234, 1346, 98, 2025, 9864802923
    ]

    process_directory(input_directory, intros, all_enumerators)

if __name__ == "__main__":
    main()
