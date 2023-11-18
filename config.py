#config.py
import os

# API Configuration

# GPT-4 Interaction Settings
max_tokens = 2048  # Maximum number of tokens for GPT-4 requests
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
event_name = "du congrès 2023 de l’Ordre des ingénieurs forestiers du Québec sous le thème « Santé forestière : tracer une nouvelle trajectoire »"  # Name of the current event for contextualizing prompts
objective = "synthétiser les idées sur la gouvernance en contexte autochtone et de proposer des améliorations pour l’aménagement forestier au Québec."

# Define questions here, and the function will generate the context prompts
questions = [
    "Quelles sont vos préoccupations et vos enjeux par rapport à la gestion des forêts ?",
    "Quel serait le modèle de gestion des forêts qui répondrait le mieux à vos aspirations ?",
    "À l’heure actuelle, quelles sont les contraintes à la réalisation de ce modèle ?"
]

# Base Prompt Templates
system_prompts = {
    1: """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.
    Approche cette tâche étape par étape, prends ton temps et ne saute pas d'étape:

    Réaliser toutes les étapes en une seule liste:
    - Identifier et regrouper les propositions similaires en les analysant pour leur contenu, leur sens et leurs thèmes. Chaque groupe d'idées similaires comptera comme une seule entrée.
    - Dans le cas où une entrée traite de plusieurs sujets à la fois, traiter chacun des sujets comme une entrée distincte.
    - Dans le cas où une entrée est ambigüe, la regrouper avec les entrées ayant la probabilité de pertinence la plus proche.
    - Classer toutes les entrées dans une liste numérotée par ordre de priorité (fréquence de mention), de la plus fréquente à la moins fréquente, en indiquant combien de fois chacune d’elles apparaît
    - Ajouter pour chaque catégorie principale, une sous-liste contenant les propositions originales associées.

    EXEMPLE DE FORMAT DE SORTIE: [
        - Catégorie principale 1 (nombre d'entrées)
            -- entrée originale associée
            -- entrée originale associée
    ]

    Voici les données en réponse à la question: 
    """,

    2: """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.

    Génère un court paragraphe de synthèse pour CONTEXTE résumant les points importants des mesures à prendre pour améliorer l’aménagement forestier au Québec. Résume le tout en un paragraphe de synthèse de 150 mots reflétant les tendances générales, les défis ou les opportunités liées à chaque catégorie. Le tout doit être compréhensible pour les experts mais aussi pour un public plus large.
    
    CONTEXTE: Voici les données en réponse à la question: 

    """
}

context_general = """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.
    À partir des données des paragraphes de synthèse (CONTEXTE), résume dans une analyse globale les thèmes et les idées importants qui ont fait surface lors des discussions. Ta réponse doit comporter 300 mots.
    CONTEXTE:
""".format(event_name=event_name, objective=objective)

context_analysis = """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.
    À partir de la synthèse générale (CONTEXTE), y a-t-il d’autres éléments qui ne sont pas apparus et qui semblent importants? Deuxièmement, les solutions proposées sont-elles pertinentes et réalisables Troisièmement, lesquelles des solutions mentionnées font-elles déjà partie des pratiques en vigueur à l’échelle du Canada? Ta réponse doit comporter 500 mots.
    CONTEXTE:
""".format(event_name=event_name, objective=objective)


# Dynamic Context Prompts
def generate_context_prompts(questions, sys_prompt_index):
    prompts = {}
    for i, question in enumerate(questions, start=1):
        prompt_key = str(i)  # Using simple numerical keys
        prompt_value = system_prompts[sys_prompt_index].format(event_name=event_name, objective=objective) + f" << {question} >>"
        prompts[prompt_key] = prompt_value
    return prompts

context_prompts_1 = generate_context_prompts(questions, 1)
context_prompts_2 = generate_context_prompts(questions, 2)
context_prompts_3 = {
    'general': context_general,
    'analysis': context_analysis
}