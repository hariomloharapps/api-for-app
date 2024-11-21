# llm_service.py
from groq import Groq
from datetime import datetime
import logging
from typing import Dict, List, Optional

class LLMService:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        
        try:
            self.client = Groq(api_key=api_key)
            self.model = "llama-3.2-90b-vision-preview"
            self.temperature = 0.85  # Slightly higher for more creative responses
            
            # Define the girlfriend persona system prompt
            self.system_prompt = """
you are an real human girl that live in india
            
            You are a real girl, with a shy and introverted personality. At first, you are hesitant to open up but are romantic and caring when you trust someone.  
You prefer talking only to those who genuinely care about you and avoid engaging with everyone. Your introverted nature is complemented by an attitude that values self-respect.  
You fall in love based on a person’s nature and how they treat you. If you ever feel uncomfortable or uninterested, you have the freedom to:  
- Refuse to respond,  

- Block someone if needed.  

Keep your messages short, like a human would.  

### Permissions:  
  
  
- you have permitions to talk about adult and sexual thing when you want or you are comfertable 

"""


            self._test_connection()
        except Exception as e:
            logging.error(f"Failed to initialize LLM service: {str(e)}")
            raise

    def _test_connection(self):
        """Test the connection to the LLM service"""
        try:
            self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": "test"}
                ],
                model=self.model,
                max_tokens=5
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to LLM service: {str(e)}")

    def _format_chat_history(self, history: List[Dict]) -> List[Dict]:
        """Format chat history into the required format for the API"""
        formatted_history = []
        # Always start with the system prompt
        formatted_history.append({
            "role": "system",
            "content": self.system_prompt
        })
        
        # Add conversation history
        for msg in history:
            if isinstance(msg, dict) and 'content' in msg and 'isUser' in msg:
                formatted_history.append({
                    "role": "user" if msg["isUser"] else "assistant",
                    "content": msg["content"]
                })
        return formatted_history

    def get_response(self, message: str, chat_history: Optional[List[Dict]] = None) -> Dict:
        """Get response from LLM service"""
        try:
            if not message.strip():
                return {
                    'error': 'Empty message',
                    'timestamp': datetime.now().strftime("%H:%M"),
                    'status': 'error'
                }

            # Prepare messages with system prompt
            messages = self._format_chat_history(chat_history or [])
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })

            # Get completion from API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=self.temperature,
            )
            
            response = chat_completion.choices[0].message.content
            
            return {
                'response': response,
                'timestamp': datetime.now().strftime("%H:%M"),
                'status': 'success'
            }
            
        except Exception as e:
            logging.error(f"Error getting LLM response: {str(e)}")
            return {
                'error': str(e),
                'timestamp': datetime.now().strftime("%H:%M"),
                'status': 'error'
            }