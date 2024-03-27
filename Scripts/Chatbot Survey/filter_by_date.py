import json
import csv
from datetime import datetime, timedelta
import os

class ConversationProcessor:
    def __init__(self, file_path, start_date_str, end_date_str, output_folder):
        self.file_path = file_path
        self.start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        self.end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        self.output_folder = output_folder
        self.data = None
        self.selected_conversations_by_date = None

    def load_data(self):
        with open(self.file_path, 'r') as file:
            self.data = json.load(file)

    def filter_conversations_by_date(self):
        self.selected_conversations_by_date = {str(date): [] for date in
                                               (self.start_date + timedelta(n) for n in range(
                                                   (self.end_date - self.start_date).days + 1))}

        for conversation_set in self.data:
            for conversation in conversation_set:
                initiated_at_timestamp = conversation['additional_attributes']['initiated_at']['timestamp']
                initiated_at_date_str = initiated_at_timestamp.split(' ')[1:4]
                initiated_at_date_str = ' '.join(initiated_at_date_str)
                initiated_at = datetime.strptime(initiated_at_date_str, "%b %d %Y")

                if self.start_date <= initiated_at.date() <= self.end_date:
                    date_str = initiated_at.date().strftime("%Y-%m-%d")
                    self.selected_conversations_by_date[date_str].append([conversation])

    def save_conversations_by_date(self):
        for date_str, conversations in self.selected_conversations_by_date.items():
            date_object = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_object.strftime("%b %d")
            output_file_path = f"{self.output_folder}/{formatted_date}.json"

            # Create the output folder if it doesn't exist
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(conversations, output_file, indent=2, ensure_ascii=False)
            print(f"Selected conversations for {date_str} saved to: {output_file_path}")

    def filter_and_save_all_conversations(self):
        selected_conversations = []

        for conversation_set in self.data:
            for conversation in conversation_set:
                initiated_at_timestamp = conversation['additional_attributes']['initiated_at']['timestamp']
                initiated_at_date_str = initiated_at_timestamp.split(' ')[1:4]
                initiated_at_date_str = ' '.join(initiated_at_date_str)
                initiated_at = datetime.strptime(initiated_at_date_str, "%b %d %Y")

                if self.start_date <= initiated_at.date() <= self.end_date:
                    selected_conversations.append([conversation])

        output_file_path = f"{self.output_folder}/selected_conversations.json"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(selected_conversations, output_file, indent=2, ensure_ascii=False)
        print(f"All selected conversations saved to: {output_file_path}")

    def generate_conversation_count_csv(self):
        conversation_count = {date: len(conversations) for date, conversations in self.selected_conversations_by_date.items()}
        csv_file_path = "Results/Bot_Survey/conversation_count.csv"
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Date', 'Conversation Count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for date, count in conversation_count.items():
                writer.writerow({'Date': date, 'Conversation Count': count})
        print(f"Conversation count CSV file saved to: {csv_file_path}")


def process_conversations(file_path, start_date_str, end_date_str, output_folder):
    processor = ConversationProcessor(file_path, start_date_str, end_date_str, output_folder)
    processor.load_data()
    processor.filter_conversations_by_date()
    processor.save_conversations_by_date()
    processor.filter_and_save_all_conversations()
    processor.generate_conversation_count_csv()

def main():
    file_path = "Data/BMGF.json"
    start_date_str = "2024-01-05"
    end_date_str = "2024-02-29"
    output_folder = "Data/By_Date"
    process_conversations(file_path, start_date_str, end_date_str, output_folder)

if __name__ == "__main__":
    main()
