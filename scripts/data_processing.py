import json
import re
import os
import sys

# Add the parent directory to the system path to access config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import json_file, prep_output_dir

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
    for input_key, responses in data.items():
        cleaned_responses = [clean_text(response) for response in responses]
        processed_data[input_key] = cleaned_responses
    return processed_data

# Example Usage
data = read_json(json_file)
processed_data = process_input_data_json_style(data)

# Ensure directory exists
os.makedirs(prep_output_dir, exist_ok=True)

# Writing to a single JSON file
output_file_path = os.path.join(prep_output_dir, "preprocessed_data.json")
with open(output_file_path, "w", encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=4)
