import ollama


chat_history = []

def chat(user_message):
    chat_history.append({
        'role': 'user',
        'content': user_message
    })
    
    response = ollama.chat(
        model='llama3.2',
        messages=chat_history
    )
    
    reply = response['message']['content']
    chat_history.append({
        'role': 'assistant', 
        'content': reply
    })
    
    return reply

# Conversation
print(chat("I have a classification problem with imbalanced data"))
print(chat("What SMOTE techniques should I use?"))
print(chat("Show me the Python code for that"))