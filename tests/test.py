#config.py
import os

# API Configuration

# Load the API key from an environment variable for security
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")
api_version = "gpt-4-1106-preview"

# File Paths
json_file = "data/raw/compiled_data.json"  # Path to the raw JSON data file
prep_output_dir = "data/interim"
inputs_file = os.path.join(prep_output_dir, "preprocessed_data.json")

# Event Configuration
event_name = "name of current event"  # Name of the current event for contextualizing prompts
objective = "synthétiser les idées sur la gouvernance en contexte autochtone et de proposer des améliorations pour l’aménagement forestier au Québec."

# GPT-4 Interaction Settings
max_tokens = 2048  # Maximum number of tokens for GPT-4 requests

# Define questions here, and the function will generate the context prompts
questions = [
    "Quelles sont vos préoccupations et vos enjeux par rapport à la gestion des forêts ?",
    "Quel serait le modèle de gestion des forêts qui répondrait le mieux à vos aspirations ?",
    "À l’heure actuelle, quelles sont les contraintes à la réalisation de ce modèle ?"
]

# Base Prompt Templates
system_prompts = {
    1: """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors de {event_name}. Ton objectif est de {objective}.

    Réaliser toutes les étapes en une sortie:
    - Identifier et regrouper les propositions similaires abordant le même thème ou contenu.
    - Créer une liste numérotée des catégories regroupées.
    - Classer les catégories par ordre de priorité basé sur la fréquence de mention.
    - Pour chaque catégorie, indiquer le nombre de fois qu'elle a été mentionnée.
    - Ajouter une sous-liste pour chaque catégorie principale, contenant les propositions originales associées.
    """,
    2: """system prompt 2""",
    3: """system prompt 3"""
}

# Dynamic Context Prompts
def generate_context_prompts(questions):
    prompts = {}
    for i, question in enumerate(questions, start=1):
        prompt_key = f"context_{i}"
        prompt_value = f" << {question} >>"  # Only include the specific question
        prompts[prompt_key] = prompt_value
    return prompts

context_prompts = generate_context_prompts(questions)

###

#run.py
import sys
import os
from config import system_prompts, context_prompts, inputs_file, api_version, max_tokens

# Add the scripts directory to the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, 'scripts')
sys.path.append(scripts_dir)

import api_interaction

# Load preprocessed data
def load_preprocessed_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


    # This below needs to be modified: the first step/iteration of the 'main()' function could be resumed in a function that:
    # 1. for each 'input' from 'inputs_file', it must combine the data as to build a prompt respecting this format:
    # INSTRUCTIONS: 'system_prompts[1]' + CONTEXT: 'context_prompts[#]' + DATA: 'input_data[# (same # as context prompts[#])]'

# Main execution function
def main():
    data = load_preprocessed_data(inputs_file)

    # Process each input with GPT-4
    for input_key, input_data in data.items():
        for prompt_key, system_prompt in context_prompts.items():
            # Combine each input with each context prompt and send it to GPT-4
            combined_input = " ".join(input_data)
            response = api_interaction.process_data_with_gpt4(combined_input, system_prompt[1], max_tokens, api_version)
            if response:
                print(f"Response for {prompt_key} with {input_key}: {response}")
            else:
                print(f"Failed to process {prompt_key} with {input_key}")

if __name__ == "__main__":
    main()


###

#api_interaction.py
import requests
from openai import OpenAI

client = OpenAI(api_key=api_key)
import os

# Add the parent directory to the system path to access config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import api_key

# Set the OpenAI API key


# Global variable for prompt count
prompt_count = 0

def process_data_with_gpt4(prompt, max_tokens, api_version):
    """
    Processes the given data with GPT-4 and returns the response.

    :param prompt: The prompt to be sent to GPT-4.
    :param max_tokens: The maximum number of tokens for the GPT-4 response.
    :param api_version: The version of the GPT-4 model to use.
    :return: The response from GPT-4.
    """
    global prompt_count
    prompt_count += 1
    try:
        # Writing the prompt to a file for logging
        with open(f'data/processed/experiment_2/prompt_{prompt_count}.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)

        # API Call
        response = client.completions.create(model=api_version,
        prompt=prompt,
        max_tokens=max_tokens)

        # Extracting and returning the response
        response_text = response.choices[0].text

        # Writing the response to a file for logging
        with open(f'data/processed/experiment_2/response_{prompt_count}.txt', 'w', encoding='utf-8') as f:
            f.write(response_text)

        return response_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
