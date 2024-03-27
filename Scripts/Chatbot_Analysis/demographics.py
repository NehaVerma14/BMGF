import json
import csv

# Function to count intro occurrences
def count_intro(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        intro_count = {}
        for conversation_list in data:
            for conversation in conversation_list:
                intro = conversation.get('meta', {}).get('sender', {}).get('custom_attributes', {}).get('intro')
                if intro:
                    if intro == 'महिला स्वास्थ्य स्वयमसेविका':
                        intro = 'FCHV'
                    elif intro == 'विद्यार्थी':
                        intro = 'Youth'
                    elif intro == 'स्थानीय':
                        intro = 'Community'
                    if intro in intro_count:
                        intro_count[intro] += 1
                    else:
                        intro_count[intro] = 1
    return intro_count

# Function to map gender to the desired labels
def map_gender(gender):
    if gender == 'Female':
        return 'महिला'
    elif gender == 'Male':
        return 'पुरुष'
    elif gender == 'Non-binary':
        return 'अन्य'
    else:
        return gender

# Function to count gender occurrences
def count_gender(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        gender_count = {}
        for conversation_list in data:
            for conversation in conversation_list:
                gender = conversation.get('meta', {}).get('sender', {}).get('custom_attributes', {}).get('gender')
                if gender:
                    gender = map_gender(gender)
                    if gender in gender_count:
                        gender_count[gender] += 1
                    else:
                        gender_count[gender] = 1
    return gender_count

# Function to count location occurrences
def count_location(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        location_count = {}
        for conversation_list in data:
            for conversation in conversation_list:
                location = conversation.get('meta', {}).get('sender', {}).get('custom_attributes', {}).get('location')
                if location:
                    # Group "Lalitpur" and "KTM" under "Bagmati Province"
                    if location == "Lalitpur" or location == "KTM":
                        location = "Bagmati Province"
                    if location in location_count:
                        location_count[location] += 1
                    else:
                        location_count[location] = 1
    return location_count

# Function to count age occurrences
def count_age(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        age_count = {'0-10': 0, '11-20': 0, '21-30': 0, '31-40': 0, '41-50': 0, '51-60': 0, '60+': 0}
        for conversation_list in data:
            for conversation in conversation_list:
                age = conversation.get('meta', {}).get('sender', {}).get('custom_attributes', {}).get('age')
                if age:
                    age = int(age)
                    if age <= 10:
                        age_group = '0-10'
                    elif age <= 20:
                        age_group = '11-20'
                    elif age <= 30:
                        age_group = '21-30'
                    elif age <= 40:
                        age_group = '31-40'
                    elif age <= 50:
                        age_group = '41-50'
                    elif age <= 60:
                        age_group = '51-60'
                    else:
                        age_group = '60+'
                    
                    age_count[age_group] += 1
    return age_count

# Function to count municipality occurrences
def count_municipality(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        municipality_count = {}
        for conversation_list in data:
            for conversation in conversation_list:
                municipality = conversation.get('meta', {}).get('sender', {}).get('custom_attributes', {}).get('muncipality')
                if municipality:
                    if municipality in municipality_count:
                        municipality_count[municipality] += 1
                    else:
                        municipality_count[municipality] = 1
    return municipality_count

# Paths to JSON files
file_paths = {
    'Data/BMGF.json': 'Total',
    'Data/Phase1.json': 'Phase1',
    'Data/Phase2.json': 'Phase2',
    # 'Data/GPT1.json': 'GPT1',
    # 'Data/GPT2.json': 'GPT2',
    # '/Human.json': 'Human',
    # 'Data/Opensource.json': 'OpenSource',
    
}

def perform_demographic_analysis(analysis_function, result_file_prefix):
    all_results = {}
    for file_path, label in file_paths.items():
        result = analysis_function(file_path)
        all_results[label] = result

    result_file = f'Results/Chatbot_Analysis/Demographics/{result_file_prefix}_count.csv'
    with open(result_file, 'w', newline='') as f:
        writer = csv.writer(f)
        header = [result_file_prefix] + list(file_paths.values())
        writer.writerow(header)
        categories = sorted(all_results[list(file_paths.values())[0]].keys())  # Sort categories
        for category in categories:
            row = [category]
            for label in file_paths.values():
                row.append(all_results[label].get(category, 0))
            writer.writerow(row)
    print(f"Result saved to {result_file}")


# Main function
def main():
    # Perform demographic analyses
    perform_demographic_analysis(count_intro, 'Introduction')
    perform_demographic_analysis(count_gender, 'Gender')
    perform_demographic_analysis(count_location, 'Location')
    perform_demographic_analysis(count_age, 'Age')
    perform_demographic_analysis(count_municipality, 'Municipality')

if __name__ == "__main__":
    main()
