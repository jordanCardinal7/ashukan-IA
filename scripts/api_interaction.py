from openai import OpenAI
from config import api_key

client = OpenAI(api_key=api_key)

def process_data_with_gpt4(prompt, max_tokens, api_version):
    try:
        # API Call using the chat completions endpoint
        completion = client.chat.completions.create(
            model=api_version,
            messages=[{"role": "system", "content": prompt}],
            max_tokens=max_tokens
        )

        # Accessing and returning the response message
        response_message = completion.choices[0].message
        return response_message

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
