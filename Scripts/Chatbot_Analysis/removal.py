import os
import json
import re

def process_single_turn_contents(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    conversations_to_keep = []

    for conversation in data:
        messages = conversation[0]['messages']
        labels = conversation[0].get('labels', [])
        keep_conversation = True
        for label in labels:
            if 'a-out-topic' in label or 'a-no-qn' in label:
                keep_conversation = False
                break

        if keep_conversation:
            for message in messages:
                content_attributes = message.get('content_attributes', {})
                if 'label' in content_attributes and ('a-out-topic' in content_attributes['label'] or 'a-no-qn' in content_attributes['label']):
                    keep_conversation = False
                    break

        if keep_conversation:
            conversations_to_keep.append(conversation)

    return conversations_to_keep

def remove_patterns(file_path, patterns):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    filtered_data = []
    for conversation in data:
        messages = conversation[0]['messages']
        for message in messages:
            if message['sender']['type'] == 'agent_bot' or message['sender']['type'] == 'user':
                content = message['content']
                if not any(pattern.search(content) for pattern in patterns):
                    filtered_data.append(conversation)
                    break

    return filtered_data

def process_multi_turn_contents(file_path, filtered_data):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    merged_data = data + filtered_data

    return merged_data

def main():
    input_dir = "Data/Turn"
    output_dir = "Data"
    
    patterns = [
    re.compile(r'माफ\s+गर्नुहोला', re.IGNORECASE),
    re.compile(r'Hello!\s*How\s*can\s*I\s*assist\??', re.IGNORECASE),
    re.compile(r'\b(hi|hola)\s*$', re.IGNORECASE),
    re.compile(r'Hajur\s+bhannus.*', re.IGNORECASE),
    re.compile(r'.*will\s+reply\s+soon', re.IGNORECASE),
    re.compile(r'I\'m\s+sorry,\s+but\s+I\s+can\s+only\s+respond', re.IGNORECASE),
    re.compile(r'तपाईंले\s+जसरी\s+प्रश्न\s+गर्नुभयो', re.IGNORECASE),
    re.compile(r'.*कृपया\s+थप\s+विवरण',re.IGNORECASE),
    re.compile(r'.*प्रश्न\s+सम्झिन\s+सक्दैन।',re.IGNORECASE),
    re.compile(r'###परिभाषा\s+अनुसार,', re.IGNORECASE),
    re.compile(r'I\'m\s+sorry,\s+but\s+I', re.IGNORECASE),
    re.compile(r'.*unrelated\s+to\s+sexual,',re.IGNORECASE),
    re.compile(r'.*कृपया\s+आफ्नो\s+प्रश्न',re.IGNORECASE),
    re.compile(r'.*सेक्सुअल,\s+मातृत्व\s+र\s+प्रजनन\s+स्वास्थ्य\s+सम्बन्धी\s+छैन',re.IGNORECASE),
    re.compile(r'.*यहाँ\s+सेक्सुअल,\s+मातृत्व\s+र\s+प्रजनन\s+स्वास्थ्य\s+सम्बन्धी',re.IGNORECASE),
    re.compile(r'.*मैले\s+सेक्सुअल,\s+मातृत्व\s+र\s+प्रजनन',re.IGNORECASE),
    re.compile(r'.*सहयोगी\s+सेक्सुअल,\s+मातृत्व\s+र\s+प्रजनन',re.IGNORECASE),
    re.compile(r'.*वेबसाइटले\s+सेक्सुअल,\s+मातृत्व\s+र\s+प्रजनन',re.IGNORECASE),
    re.compile(r'.*तपाईंले\s+सेक्सुअल,\s+मातृत्व\s+र\s+प्रजनन',re.IGNORECASE),
    re.compile(r'.*अंग्रेजीमा\s+पनि\s+रोमनाइज\s+नेपालीमा',re.IGNORECASE),
    re.compile(r'.*तपाईंको\s+सेक्सुअल,\s+मातृत्व\s+र\s+प्रजनन',re.IGNORECASE),
    re.compile(r'.*विषयमा\s+सल्लाह\s+दिन',re.IGNORECASE),
    re.compile(r'.*I\'m\s+here\s+to\s+help',re.IGNORECASE),
    re.compile(r'.*I\s+apologize',re.IGNORECASE),
    re.compile(r'.*response',re.IGNORECASE),
    re.compile(r'.*कस्तो\s+सहयोग\s+गर्न',re.IGNORECASE),
    re.compile(r'.*sex\s+sambandhi\s+sawal',re.IGNORECASE),
    re.compile(r'.*माफ\s+गर्नुहोस्,',re.IGNORECASE),
    re.compile(r'.*am\s+here\s+to\s+provide\s+information',re.IGNORECASE),
    re.compile(r'.*question\s+is\s+not\s+directly',re.IGNORECASE),
    re.compile(r'.*सोध्न\s+चाहनुहुन्छ?',re.IGNORECASE),
    re.compile(r'.*स्पष्ट\s+गर्नुहोस्।',re.IGNORECASE),
    re.compile(r'.*तपाईंलाई\s+सहायता\s+गर्न\s+सक्छु।',re.IGNORECASE),
    re.compile(r'नमस्ते!(?! धेरै धेरै मानिसहरूले)\s*\w*', re.IGNORECASE),
    re.compile(r'.*सम्बन्धित\s+कुनै\s+प्रश्न', re.IGNORECASE),
    re.compile(r'.*मलाई\s+लाग्छ\s+कि', re.IGNORECASE),
    re.compile(r'.*अंग्रेजी\s+वा\s+रोमनाइजड', re.IGNORECASE),
    re.compile(r'.*कृपया\s+तपाईंको\s+प्रश्नलाई', re.IGNORECASE),
    re.compile(r'.*hamro\s+scope',re.IGNORECASE),
    re.compile(r'.*क्षमा\s+गर्नुहोस्,\s+तपाईंले',re.IGNORECASE),
    re.compile(r'.*yo\s+mero\s+gopya\s+kura',re.IGNORECASE),
    re.compile(r'This\s+message\s+was\s+deleted',re.IGNORECASE),
    re.compile(r'.*k\s+janna\s+chahanu\s+huncha?',re.IGNORECASE),  
    
    
]
    
    for root, dirs, files in os.walk(input_dir):
        for directory in dirs:
            single_turn_file = os.path.join(root, directory, 'single_turn_contents.json')
            multi_turn_file = os.path.join(root, directory, 'multi_turn_contents.json')
            output_file = os.path.join(output_dir, directory + '.json')

            if os.path.exists(single_turn_file) and os.path.exists(multi_turn_file):
                # Process single turn contents
                conversations_to_keep = process_single_turn_contents(single_turn_file)
                
                temp_file_path = os.path.join("Data/", directory + '_processed.json')
                with open(temp_file_path, 'w', encoding='utf-8') as temp_file:
                    json.dump(conversations_to_keep, temp_file, ensure_ascii=False, indent=4)

                # Remove patterns
                filtered_data = remove_patterns(temp_file_path, patterns)

                # Merge with multi turn contents
                merged_data = process_multi_turn_contents(multi_turn_file, filtered_data)
                os.remove(temp_file_path)

                # Save the result
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(merged_data, file, ensure_ascii=False, indent=4)

                # os.remove(temp_file_path)    

                print(f"Processed {single_turn_file}, removed patterns, and merged with {multi_turn_file}. Saved to {output_file}")

if __name__ == "__main__":
    main()