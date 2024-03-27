import json
import os
import csv
from collections import OrderedDict
from datetime import datetime

def total_conversations(data):
    all_ids = []

    for conversation in data:
        for message_data in conversation:
            all_ids.append(message_data['id'])

    return all_ids

def multi_turn_conversations(data):
    multi_turn_ids = []

    for conversation in data:
        for message_data in conversation:
            messages = message_data.get('messages', [])

            contact_count = 0
            user_agent_count = 0

            for message in messages:
                sender_type = message['sender'].get('type')

                if sender_type == 'contact':
                    contact_count += 1

                if sender_type in ['user', 'agent_bot']:
                    user_agent_count += 1

            if len(messages) > 1 and contact_count >= 1 and user_agent_count > 1:
                multi_turn_ids.append(message_data['id'])
                break

    return multi_turn_ids

def single_turn_conversations(data):
    single_turn_ids = []

    for conversation in data:
        for message_data in conversation:
            messages = message_data.get('messages', [])

            contact_count = 0
            user_agent_count = 0

            for message in messages:
                sender_type = message['sender'].get('type')

                if sender_type == 'contact':
                    contact_count += 1

                if sender_type in ['user', 'agent_bot']:
                    user_agent_count += 1

            if contact_count >= 1 and user_agent_count == 1:
                single_turn_ids.append(message_data['id'])

    return single_turn_ids

def empty_messages_conversations(data):
    empty_messages_ids = []

    for conversation in data:
        for message_data in conversation:
            messages = message_data.get('messages', [])

            if not messages:
                empty_messages_ids.append(message_data['id'])

    return empty_messages_ids

def not_responded_conversations(data):
        not_responded_ids = []

        for conversation in data:
            for message_data in conversation:
                messages = message_data.get('messages', [])

                contact_count = 0
                user_agent_count = 0

                for message in messages:
                    sender_type = message['sender'].get('type')

                    if sender_type == 'contact':
                        contact_count += 1

                    if sender_type in ['user', 'agent_bot']:
                        user_agent_count += 1

                if contact_count >= 1 and user_agent_count == 0:
                    not_responded_ids.append(message_data['id'])

        return not_responded_ids



def remaining_ids(data, multi_turn, single_turn, not_responded, empty_messages):
    all_ids = set(total_conversations(data))
    used_ids = set(multi_turn + single_turn + not_responded + empty_messages)
    remaining = list(all_ids - used_ids)
    return remaining

def analyze_and_save_results(data_directory, output_directory):
    all_results = []

    # Define the ordered mapping of filenames to labels
    file_labels = OrderedDict([
        ("Phase1.json", "Phase1"),
        ("Phase2.json", "Phase2"),
        ("BMGF.json", "Total"),
        # ("Diyochat_2.json", "Total")
    ])

    for filename, label in file_labels.items():
        file_path = os.path.join(data_directory, filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                conversation_data = json.load(file)

            multi_turn = multi_turn_conversations(conversation_data)
            single_turn = single_turn_conversations(conversation_data)
            empty_messages = empty_messages_conversations(conversation_data)
            not_responded = not_responded_conversations(conversation_data)
            remaining = remaining_ids(conversation_data, multi_turn, single_turn, not_responded, empty_messages)

            result = {
                "File": label,
                "Multi Turn": len(multi_turn),
                "Single Turn": len(single_turn),
                "Empty Messages": len(empty_messages),
                "Not Responded": len(not_responded),
                "Remaining": len(remaining)
            }
            all_results.append(result)

    output_file = os.path.join("Results/Chatbot_Analysis", "conversation_analysis.csv")
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["File", "Multi Turn", "Single Turn", "Empty Messages", "Not Responded", "Remaining"])
        writer.writeheader()
        writer.writerows(all_results)

    print("Results have been saved to:", output_file)


def dump_conversation_contents(data, conversation_ids, output_file):
    selected_contents = []

    for conversation in data:
        for message_data in conversation:
            if message_data['id'] in conversation_ids:
                selected_contents.append([message_data])  

    with open(output_file, 'w') as outfile:
        json.dump(selected_contents, outfile, ensure_ascii=False, indent=2)

def dump_all_conversations(data, input_file, output_folder):
    multi_turn = multi_turn_conversations(data)
    single_turn = single_turn_conversations(data)
    not_responded = not_responded_conversations(data)
    empty_messages = empty_messages_conversations(data)
    remaining = remaining_ids(data, multi_turn, single_turn, not_responded, empty_messages)

    dump_conversation_contents(data, multi_turn, os.path.join(output_folder, 'multi_turn_contents.json'))
    dump_conversation_contents(data, single_turn, os.path.join(output_folder, 'single_turn_contents.json'))
    dump_conversation_contents(data, not_responded, os.path.join(output_folder, 'not_responded_contents.json'))
    dump_conversation_contents(data, empty_messages, os.path.join(output_folder, 'empty_messages_contents.json'))
    dump_conversation_contents(data, remaining, os.path.join(output_folder, 'remaining_contents.json'))

def organize_files_into_folders(data_directory, output_directory):
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(data_directory, filename)
            with open(file_path, "r") as file:
                conversation_data = json.load(file)

            folder_name = filename.split('.')[0]
            folder_path = os.path.join(output_directory, "Turn", folder_name)
            os.makedirs(folder_path, exist_ok=True)

            dump_all_conversations(conversation_data, file_path, folder_path)

            print(f"Processed data for file {filename} saved in folder {folder_name}")

def main():
    data_directory = "Data/"
    output_directory = "Data/"

    analyze_and_save_results(data_directory, output_directory)
    organize_files_into_folders(data_directory, output_directory)

if __name__ == "__main__":
    main()
