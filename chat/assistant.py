

import requests
import json
import os

API_KEY = ''  # Replace with your OpenAI API key
MODEL = 'gpt-4o-mini'  
HISTORY_FILE = 'chat_history.json'

def load_history():
    """Load conversation history from a file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_history(history):
    """Save conversation history to a file."""
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file, indent=4)

def get_gpt_response(messages):
    """Get a response from the ChatGPT API."""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': MODEL,
        'messages': messages,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return "Error: Could not get response from the API."

    response_data = response.json()
    
    
    if 'choices' in response_data and len(response_data['choices']) > 0:
        return response_data['choices'][0]['message']['content']
    else:
        print("Unexpected response format:", response_data)
        return "Error: Unexpected response format from the API."

def main():
   
    conversation_history = load_history()

    print("ChatGPT Chat - Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        
        conversation_history.append({'role': 'user', 'content': user_input})

       
        gpt_response = get_gpt_response(conversation_history)
        
    
        conversation_history.append({'role': 'assistant', 'content': gpt_response})

       
        print(f"GPT: {gpt_response}")


        save_history(conversation_history)

if __name__ == "__main__":
    main()






