#api_interaction.py
import requests
import openai
import os

# Add the parent directory to the system path to access config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import api_key

# Set the OpenAI API key
openai.api_key = api_key

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
        with open(f'data/processed/prompt_{prompt_count}.txt', 'w', encoding='utf-8') as f:
            f.write(prompt)

        # API Call
        response = openai.Completion.create(
            model=api_version,
            prompt=prompt,
            max_tokens=max_tokens
        )

        # Extracting and returning the response
        response_text = response.choices[0].text

        # Writing the response to a file for logging
        with open(f'data/processed/experiment_2/response_{prompt_count}.txt', 'w', encoding='utf-8') as f:
            f.write(response_text)

        return response_text

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
