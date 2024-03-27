import os
import json
import csv

class ConversationAnalyzer:
    def __init__(self, input_directory, output_directory="Data/By_Turn"):
        self.input_directory = input_directory
        self.output_directory = output_directory
        self.summary_file =  "Results/Bot_Survey/summary_turn_count.csv"

        # Create necessary directories
        os.makedirs(self.output_directory, exist_ok=True)

        # Create or overwrite the summary CSV file with headers
        with open(self.summary_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Inbox Name","File Name", "Total Conversations", "Multi-Turn Conversations", "Single-Turn Conversations",
                             "Not Responded Conversations", "Empty Messages Conversations", "Remaining Conversations"])


    def read_json_files_from_subfolder(self, file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None

    def total_conversations(self, data):
        return [message_data['id'] for conversation in data for message_data in conversation]

    def multi_turn_conversations(self, data):
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

    def single_turn_conversations(self, data):
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

    def not_responded_conversations(self, data):
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

    def empty_messages_conversations(self, data):
        empty_messages_ids = []

        for conversation in data:
            for message_data in conversation:
                messages = message_data.get('messages', [])

                if not messages:
                    empty_messages_ids.append(message_data['id'])

        return empty_messages_ids

    def remaining_ids(self, data, multi_turn, single_turn, not_responded, empty_messages):
        all_ids = set(self.total_conversations(data))
        used_ids = set(multi_turn + single_turn + not_responded + empty_messages)
        remaining = list(all_ids - used_ids)
        return remaining

    def dump_conversation_contents(self, data, conversation_ids, output_file):
        selected_contents = []

        for conversation in data:
            for message_data in conversation:
                if message_data['id'] in conversation_ids:
                    selected_contents.append([message_data])  # Wrap each conversation in []

        with open(output_file, 'w') as outfile:
            json.dump(selected_contents, outfile, ensure_ascii=False, indent=2)

    def dump_all_conversations(self, data, input_file, output_folder):
        multi_turn = self.multi_turn_conversations(data)
        single_turn = self.single_turn_conversations(data)
        not_responded = self.not_responded_conversations(data)
        empty_messages = self.empty_messages_conversations(data)

        self.dump_conversation_contents(data, multi_turn, os.path.join(output_folder, 'multi_turn_contents.json'))
        self.dump_conversation_contents(data, single_turn, os.path.join(output_folder, 'single_turn_contents.json'))
        self.dump_conversation_contents(data, not_responded, os.path.join(output_folder, 'not_responded_contents.json'))
        self.dump_conversation_contents(data, empty_messages, os.path.join(output_folder, 'empty_messages_contents.json'))

        remaining = self.remaining_ids(data, multi_turn, single_turn, not_responded, empty_messages)
        self.dump_conversation_contents(data, remaining, os.path.join(output_folder, 'remaining_contents.json'))

    def print_summary(self, folder_name, file_name, data):
        total_conversations = len(data)
        multi_turn = len(self.multi_turn_conversations(data))
        single_turn = len(self.single_turn_conversations(data))
        not_responded = len(self.not_responded_conversations(data))
        empty_messages = len(self.empty_messages_conversations(data))
        remaining = total_conversations - (multi_turn + single_turn + not_responded + empty_messages)

        with open(self.summary_file, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([folder_name, file_name, total_conversations, multi_turn, single_turn, not_responded, empty_messages, remaining])


    def print_results(self):
        subfolder_paths = self.get_subfolder_paths()

        for subfolder_path in subfolder_paths:
            if os.path.isdir(subfolder_path):
                json_files = [f for f in sorted(os.listdir(subfolder_path)) if f.endswith('.json')]  # Sort files alphabetically
                for json_file in json_files:
                    file_path = os.path.join(subfolder_path, json_file)
                    data = self.read_json_files_from_subfolder(file_path)
                    if data:
                        folder_name = os.path.basename(subfolder_path)
                        output_folder = os.path.join(self.output_directory, folder_name, os.path.splitext(json_file)[0])
                        os.makedirs(output_folder, exist_ok=True)

                        self.dump_all_conversations(data, file_path, output_folder)
                        self.print_summary(folder_name, json_file, data)

                        print(f"\nProcessing completed for file: {json_file} in subfolder: {folder_name}")
            else:
                print(f"Skipping non-directory file: {subfolder_path}")

    def get_subfolder_paths(self):
        subfolder_paths = [os.path.join(self.input_directory, f) for f in os.listdir(self.input_directory) if os.path.isdir(os.path.join(self.input_directory, f))]
        return subfolder_paths
    
def main():
    analyzer = ConversationAnalyzer('Data/By_Inbox')
    analyzer.print_results()

if __name__ == "__main__":
    main()