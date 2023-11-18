#api_interaction.py
from openai import OpenAI
from config import api_key, api_version, max_tokens

client = OpenAI(api_key=api_key)

def process_data_with_gpt4(prompt, temp):
    try:
        completion = client.chat.completions.create(
            model=api_version,
            messages=[{"role": "system", "content": prompt}],
            temperature=temp,
            max_tokens=max_tokens
        )
        response_message = completion.choices[0].message.content  # Extracting the content of the message
        return response_message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
