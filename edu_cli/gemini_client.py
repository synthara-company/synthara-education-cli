import os
import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key=None):
        """Initialize the Gemini client with an API key."""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Please provide it or set GEMINI_API_KEY environment variable.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-pro-preview-03-25")

    def set_api_key(self, api_key):
        """Set or update the API key."""
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-pro-preview-03-25")
        return True

    def generate_response(self, prompt, system_instruction=None, stream=True):
        """Generate a response from Gemini based on the prompt."""
        # Create the generation config
        generation_config = {
            "response_mime_type": "text/plain",
        }

        # Create the chat session
        chat = self.model.start_chat()

        # Combine system instruction with prompt if provided
        if system_instruction:
            full_prompt = f"{system_instruction}\n\nUser question: {prompt}"
        else:
            full_prompt = prompt

        # Send the user prompt and get response
        if stream:
            return chat.send_message(full_prompt, stream=True, generation_config=generation_config)
        else:
            response = chat.send_message(full_prompt, stream=False, generation_config=generation_config)
            return response.text
