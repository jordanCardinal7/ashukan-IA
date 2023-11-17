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
def generate_context_prompts(questions, sys_prompt_index):
    prompts = {}
    for i, question in enumerate(questions, start=1):
        prompt_key = f"context_{i}"
        prompt_value = system_prompts[sys_prompt_index].format(event_name=event_name, objective=objective) + f" << {question} >>"
        prompts[prompt_key] = prompt_value
    return prompts

context_prompts_1 = generate_context_prompts(questions, 1)
context_prompts_2 = generate_context_prompts(questions, 2)
context_prompts_3 = generate_context_prompts(questions, 3)
