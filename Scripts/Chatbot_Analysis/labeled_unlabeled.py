import json
import csv

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

def count_labels_by_inbox(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        labeled_counts = {inbox_name: 0 for inbox_name in inbox_ids_and_names.values()}
        unlabeled_counts = {inbox_name: 0 for inbox_name in inbox_ids_and_names.values()}

        for conversation_list in data:
            for conversation in conversation_list:
                inbox_id = conversation.get('inbox_id')
                inbox_name = inbox_ids_and_names.get(inbox_id)
                if inbox_name is not None:
                    if conversation.get('labels'):
                        labeled_counts[inbox_name] += 1
                    else:
                        unlabeled_counts[inbox_name] += 1

    return labeled_counts, unlabeled_counts

def main():
    # Paths to JSON files
    file_paths = {
        'Data/Phase1.json': 'Phase 1',
        'Data/Phase2.json': 'Phase 2',
        'Data/BMGF.json': 'Total'
    }

    # Count labeled and unlabeled conversations for each file and inbox_id
    results = {'Phase 1': {'Labeled': {}, 'Unlabeled': {}}, 'Phase 2': {'Labeled': {}, 'Unlabeled': {}}, 'Total': {'Labeled': {}, 'Unlabeled': {}}}
    for file_path, phase in file_paths.items():
        labeled, unlabeled = count_labels_by_inbox(file_path)
        results[phase]['Labeled'] = labeled
        results[phase]['Unlabeled'] = unlabeled

    # Write results to CSV file
    csv_file = 'Results/Chatbot_Analysis/conversation_labels_by_inbox.csv'
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([''] + [f"{phase}_Labeled" for phase in results.keys()] + [f"{phase}_Unlabeled" for phase in results.keys()])
        for inbox_name in inbox_ids_and_names.values():
            row_data = [inbox_name]
            for phase in results.keys():
                row_data.append(results[phase]['Labeled'].get(inbox_name, 0))
            for phase in results.keys():
                row_data.append(results[phase]['Unlabeled'].get(inbox_name, 0))
            writer.writerow(row_data)

    print("CSV file created successfully:", csv_file)

if __name__ == "__main__":
    main()
