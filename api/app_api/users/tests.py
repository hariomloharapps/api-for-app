import requests
import time
import json

# API endpoint URL
API_URL = "http://127.0.0.1:8000/api/chat/"  # Replace with your Django API endpoint

# Sample chat history
chat_history = [
 {"isUser": True, "content": "Hi, how are you today?"},
    {"isUser": False, "content": "I'm doing well, thank you! How about you?"},
    {"isUser": True, "content": "I'm good too. Can you help me with some coding advice?"},
    {"isUser": False, "content": "Of course! What do you need help with?"},
    {"isUser": True, "content": "I'm learning Python and struggling with list comprehensions."},
    {"isUser": False, "content": "List comprehensions can be tricky at first. What specifically is confusing?"},
    {"isUser": True, "content": "I don't get how to use conditions inside them."},
    {"isUser": False, "content": "You can use an `if` condition at the end. For example: `[x for x in range(10) if x % 2 == 0]`."},
    {"isUser": True, "content": "Oh, that makes sense. Can you give me a more complex example?"},
    {"isUser": False, "content": "Sure! `[x**2 for x in range(10) if x % 2 == 0]` generates squares of even numbers from 0 to 9."},
    {"isUser": True, "content": "Great! I'll try that. What else should I learn after list comprehensions?"},
    {"isUser": False, "content": "You might want to explore generators and how they differ from lists."},
    {"isUser": True, "content": "What's a generator?"},
    {"isUser": False, "content": "Generators produce items one at a time using `yield`, which is memory-efficient compared to lists."},
    {"isUser": True, "content": "How do I create one?"},
    {"isUser": False, "content": "You can use a function with the `yield` keyword. For example: `def gen(): yield 1; yield 2`."},
    {"isUser": True, "content": "That's interesting. Can I use them with loops?"},
    {"isUser": False, "content": "Yes, you can iterate over generators using a `for` loop."},
    {"isUser": True, "content": "Awesome! Can you recommend any Python books?"},
]

# User input
user_message = "What do you think about Python programming?"

# Data to send to the API
payload = {
    "message": user_message,
    "history": chat_history,
    "userId": "user123"
}

# Measure response time
start_time = time.time()

try:
    response = requests.post(API_URL, json=payload, timeout=10)  # Timeout set to 10 seconds
    end_time = time.time()

    # Calculate elapsed time
    response_time = end_time - start_time

    # Check response status
    if response.status_code == 200:
        response_data = response.json()
        print("Response Data:", json.dumps(response_data, indent=4))
        print(f"Response Time: {response_time:.2f} seconds")
    else:
        print(f"Error: Received status code {response.status_code}")
        print("Response Text:", response.text)

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
