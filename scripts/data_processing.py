#data_processing.py
import json
import re
import os
import sys

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def clean_text(text):
    # Remove unnecessary white spaces and normalize punctuation
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespaces with a single space
    text = re.sub(r'\r\n|\r|\n', ' ', text)  # Replace newlines with spaces
    text = re.sub(r'[“”]', '"', text)  # Normalize quotation marks
    return text.strip()

def process_input_data_json_style(data):
    processed_data = {}
    for index, (input_key, responses) in enumerate(data.items(), start=1):
        cleaned_responses = [clean_text(response) for response in responses]
        processed_data[str(index)] = cleaned_responses  # Using numerical string keys
    return processed_data

def process_data(input_file, output_dir):
    data = read_json(input_file)
    processed_data = process_input_data_json_style(data)

    # Ensure directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Writing to a single JSON file
    output_file_path = os.path.join(output_dir, "preprocessed_data.json")
    with open(output_file_path, "w", encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Add the parent directory to the system path to access config.py
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import json_file, prep_output_dir

    process_data(json_file, prep_output_dir)
