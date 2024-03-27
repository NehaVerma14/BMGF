import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
from tqdm import tqdm
import time

DIYOCHAT_URL = "https://llm.diyochat.com"
DIYOCHAT_BOT_TOKEN = "wVKAZtaJM6MjWZHBtL62hx1T"
output_json_filename = "/home/neha/BMGF/Data/BMGF.json"

class Diyochat:
    def __init__(self, diyochat_url: str, diyochat_bot_token: str, max_retries: int = 3):
        self.diyochat_url = diyochat_url
        self.diyochat_bot_token = diyochat_bot_token
        self.max_retries = max_retries
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()
        retries = Retry(total=self.max_retries, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def get_all_message(self, account: str, conversation: str) -> dict:
        url = f"{self.diyochat_url}/api/v1/accounts/{account}/conversations/{conversation}/messages"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api_access_token": f"{self.diyochat_bot_token}",
        }
        r = self.session.get(url, headers=headers)
        return r.json()

    def get_all_conversation(self, account: str, page: int = 1) -> dict:
        url = f"{self.diyochat_url}/api/v1/accounts/{account}/conversations?status=all&assignee_type=all&page={page}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api_access_token": f"{self.diyochat_bot_token}",
        }
        r = self.session.get(url, headers=headers)
        return r.json()

# Usage
diyochat_api = Diyochat(diyochat_url=DIYOCHAT_URL, diyochat_bot_token=DIYOCHAT_BOT_TOKEN, max_retries=5)

conversation_data = diyochat_api.get_all_conversation("22")
total_count = conversation_data["data"]["meta"]["all_count"]
total_number_pages = int(total_count / 25) + 1

print(f'Total Conversation: {total_count}')
print(f'Total Resolved Conversation: {len(conversation_data["data"]["payload"])}')
print(f'total_number_pages:', total_number_pages)

# List to store conversations
all_conversations = []

for page in tqdm(range(1, total_number_pages + 1), desc="Processing pages"):
    conversation_data = diyochat_api.get_all_conversation("22", page=page)

    for item in conversation_data["data"]["payload"]:
        conversation_id = item["id"]
        messages = diyochat_api.get_all_message("22", conversation_id)["payload"]

        conversation_messages = []

        for message in messages:
            if "sender" in message and "content" in message and message["content"]:
                message_data = {
                    "id": message["id"],
                    "content": message["content"],
                    "inbox_id": message["inbox_id"],
                    "conversation_id": message["conversation_id"],
                    "message_type": message["message_type"],
                    "content_type": message["content_type"],
                    "status": message["status"],
                    "content_attributes": message.get("content_attributes", {}),
                    "created_at": message["created_at"],
                    "private": message["private"],
                    "source_id": message["source_id"],
                    "sender": message["sender"]
                }
                conversation_messages.append(message_data)

        item["messages"] = conversation_messages

        if "last_non_activity_message" in item and "content_attributes" in item["last_non_activity_message"]:
            label_attribute = item["last_non_activity_message"]["content_attributes"].get("label")
            if label_attribute:
                # Add label to additional_attributes
                if "additional_attributes" not in item:
                    item["additional_attributes"] = {}
                item["additional_attributes"]["label"] = label_attribute

        # Wrap each conversation in square brackets
        all_conversations.append([item])

    time.sleep(1)

with open(output_json_filename, "w", encoding="utf-8") as json_file:
    json.dump(all_conversations, json_file, ensure_ascii=False, indent=2)

print(f"Filtered content saved to {output_json_filename}")
