#run.py
import json
import sys
import os
import argparse
import glob
import time
from config import context_prompts_1, context_prompts_2, context_prompts_3, api_version, max_tokens

# Add the scripts directory to the system path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts'))
import api_interaction
from data_processing import process_data

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_text(file_path, text):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def process_question_responses(data, context_prompts, output_dir):
    responses = {}
    for key, context_prompt in context_prompts.items():
        # Combine context prompt with corresponding data
        full_prompt = f"{context_prompt} DATA: {data[str(key)]}"  # Ensure data[key] is a string
        response = api_interaction.process_data_with_gpt4(full_prompt, 0.55)
        save_text(os.path.join(output_dir, f"organized_list_{key}.txt"), response)
        responses[key] = response
    return responses

def generate_synthesis_paragraphs(data, context_prompts, output_dir):
    synthesis_paragraphs = {}
    for key, context_prompt in context_prompts.items():
        # Combine context prompt with corresponding response data
        full_prompt = f"{context_prompt} DATA: {data[f'organized_list_{key}']}"  # Ensure the key matches the file naming convention
        synthesis = api_interaction.process_data_with_gpt4(full_prompt, 0.7)
        save_text(os.path.join(output_dir, f"synthesis_{key}.txt"), synthesis)
        synthesis_paragraphs[key] = synthesis
        time.sleep(2)
    return synthesis_paragraphs

def generate_final_output(data, context_prompts, output_dir):
    # Combine the three synthesis paragraphs into a single text
    combined_synthesis = "\n\n".join([data[f'synthesis_{i}'] for i in range(1, 4)])

    # Generate the general synthesis
    full_prompt_general = f"{context_prompts['general']} DATA: {combined_synthesis}"
    general_synthesis = api_interaction.process_data_with_gpt4(full_prompt_general, 0.7)

    # Generate the AI's perspective on the general synthesis
    full_prompt_analysis = f"{context_prompts['analysis']} DATA: {general_synthesis}"
    ai_analysis = api_interaction.process_data_with_gpt4(full_prompt_analysis, 0.7)

    # Combine general synthesis and AI analysis into final output
    final_output = f"General Synthesis:\n{general_synthesis}\n\nAI's Perspective:\n{ai_analysis}"
    save_text(os.path.join(output_dir, "final_output.txt"), final_output)

def wrap_up_project(input_files, output_dirs):
    # Step 1 and 2 data
    organized_lists = read_text_files(output_dirs[0])
    # Step 3 data
    synthesis_paragraphs = read_text_files(output_dirs[1])
    # Step 4 data (General Synthesis and AI Analysis)
    final_output_path = os.path.join(output_dirs[2], 'final_output.txt')
    final_output = read_text_file(final_output_path)

    # Compile the report
    report = "Project Wrap\n\n"
    for i in range(1, 4):  # Assuming there are 3 keys (1, 2, 3)
        organized_list_key = f'organized_list_{i}'
        synthesis_paragraph_key = f'synthesis_{i}'

        report += f"- List {i}\n{organized_lists[organized_list_key]}\n"
        report += f"- Synthesis paragraph {i}\n{synthesis_paragraphs[synthesis_paragraph_key]}\n\n"

    report += f"- General Synthesis and AI Analysis\n{final_output}\n"
    # Save the final report
    save_text(os.path.join(output_dirs[2], "project_wrap.txt"), report)

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def read_text_files(directory):
    files_content = {}
    for file_path in glob.glob(os.path.join(directory, '*.txt')):
        key = os.path.basename(file_path).split('.')[0]
        with open(file_path, 'r', encoding='utf-8') as file:
            files_content[key] = file.read()
    return files_content

def main(mode):
    input_files = ['data/interim/preprocessed_data.json', 'data/processed/step_1/', 'data/processed/step_2/']
    output_dirs = ['data/processed/step_1/', 'data/processed/step_2/', 'data/processed/final/']
    context_prompts_mapping = [context_prompts_1, context_prompts_2, context_prompts_3]

    if mode == 0:
        input_file = 'data/raw/compiled_data.json'
        output_dir = 'data/interim'
        process_data(input_file, output_dir)
    elif mode == 1:
        data = load_json(input_files[0])
        process_question_responses(data, context_prompts_mapping[0], output_dirs[0])
    elif mode == 2:
        data = read_text_files(input_files[1])
        generate_synthesis_paragraphs(data, context_prompts_mapping[1], output_dirs[1])
    elif mode == 3:
        synthesis_paragraphs = read_text_files(input_files[2])
        generate_final_output(synthesis_paragraphs, context_prompts_mapping[2], output_dirs[2])
    elif mode == 4:
        wrap_up_project(input_files, output_dirs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process data in different stages.")
    parser.add_argument('mode', type=int, choices=[0, 1, 2, 3, 4], help="Processing mode: 0, 1, 2, 3, or 4")
    args = parser.parse_args()
    main(args.mode)
