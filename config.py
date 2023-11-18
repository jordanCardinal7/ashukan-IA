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
event_name = "du congrès 2023 de l’Ordre des ingénieurs forestiers du Québec"  # Name of the current event for contextualizing prompts
objective = "d'approfondir la réflexion sous le thème « Santé forestière : tracer une nouvelle trajectoire » et aider à formuler des propositions concrètes destinées à poser les fondements de la gestion forestière."

# Define questions here, and the function will generate the context prompts
questions = [
    "Quelles sont vos préoccupations et vos enjeux par rapport à la gestion des forêts ?",
    "Quel serait le modèle de gestion des forêts qui répondrait le mieux à vos aspirations ?",
    "À l’heure actuelle, quelles sont les contraintes à la réalisation de ce modèle ?"
]

# Base Prompt Templates
system_prompts = {
    1: """
    CONTEXTE:
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.
    Prends ton temps pour n'oublier aucune étape et analyse le problème dans son ensemble, de manière à faire ressortir de façon concise les idées les plus centrales/prédominantes à la discussion.

    TÂCHE:
    - Analyse chaque entrée des données en format JSON et regroupe-les pour leur contenu, leur sens et leurs thèmes (pertinence sémantique), sous une même IDÉE GÉNÉRALE qui en fait la synthèse. 
    - Classe toutes les IDÉES GÉNÉRALES dans une liste numérotée, par ordre de fréquence de mention (nombre d'entrées 3 > 2 > 1), en indiquant combien d'entrées composent chacune.
    - Pour chaque IDÉE GÉNÉRALE, ajoute dans une sous-liste des exemples résumant les idées originales associées (maximum 5). 

    SPÉCIFICATIONS:
    - Dans le cas où une entrée traite de plusieurs sujets à la fois, traite chacun des sujets comme une entrée distincte. 
    - Dans le cas où une entrée est ambigüe, regroupe-la avec les entrées ayant la probabilité de pertinence sémantique la plus proche.
    
    EXEMPLE DE FORMAT DE SORTIE: [
    
        Titre: << Question >>

        1. **Idée générale (mentionnée 'x>y' fois)**
            - idée originale associée
        
        2. **Idée générale (mentionnée 'y<x' fois)**
            - idée originale associée
    ]

    Voici les données en réponse à la question:
    """,

    2: """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.

    Génère un paragraphe de synthèse pour <CONTEXTE> résumant les idées essentielles/prédominantes répondant à la <<question>> formulée. Base-toi sur la liste ci-dessous en tenant compte de la hiérarchie entrées. Résume le tout en un paragraphe de synthèse de 150 mots reflétant les tendances générales, les défis ou les opportunités liées à chaque catégorie. Le tout doit être compréhensible pour les experts mais aussi pour un public plus large.
    
    <CONTEXTE>: Voici les données en réponse à la question: 

    """
}

context_general = """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.
    À partir des données des paragraphes de synthèse (CONTEXTE), résume dans une analyse globale les thèmes et les idées importants qui ont fait surface lors des discussions. Ta réponse doit comporter 300 mots.
    CONTEXTE:
""".format(event_name=event_name, objective=objective)

context_analysis = """
    En tant qu'analyste des données, tu dois traiter les informations recueillies lors {event_name}. Ton objectif est de {objective}.
    À partir de la synthèse générale (CONTEXTE), y a-t-il d’autres éléments qui ne sont pas apparus et qui semblent importants? Deuxièmement, les solutions proposées sont-elles pertinentes et réalisables? Troisièmement, lesquelles des solutions mentionnées font-elles déjà partie des pratiques en vigueur à l’échelle du Canada? Ta réponse doit comporter 500 mots. Formule-la en 3 paragraphes, répondant à chacune des 3 questions.
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