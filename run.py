#run.py
import json
import sys
import os
from config import context_prompts_1, inputs_file, api_version, max_tokens

# Add the scripts directory to the system path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import api_interaction

def load_preprocessed_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def main():
    data = load_preprocessed_data(inputs_file)
    output_dir = 'data/processed/step_1/'

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if "input_1" in data:
        input_data = data["input_1"]
        for prompt_key, prompt_value in context_prompts_1.items():
            combined_input = " ".join(input_data)
            complete_prompt = f"{prompt_value} DATA: {combined_input}"
            response = api_interaction.process_data_with_gpt4(complete_prompt, max_tokens, api_version)

            if response:
                # Writing the response to a file
                file_path = os.path.join(output_dir, f'response_input_1_{prompt_key}.txt')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response)
                print(f"Response for {prompt_key} with input_1: {response}")
            else:
                print(f"Failed to process {prompt_key} with input_1")

if __name__ == "__main__":
    main()
