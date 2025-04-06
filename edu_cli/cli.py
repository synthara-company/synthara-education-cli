"""
Command-line interface for the Education CLI.
"""
import sys
import datetime
from .gemini_client import GeminiClient
from .education_prompts import get_subjects_list, get_subject_prompt, SYSTEM_INSTRUCTION
from .utils.terminal import (
    print_header, print_message, print_error, print_subject_table,
    get_input, get_confirmation, stream_response, print_thinking
)
from .utils.config import get_api_key, save_api_key, save_to_history

class EducationCLI:
    def __init__(self):
        """Initialize the Education CLI."""
        self.api_key = get_api_key()
        self.client = None
        self.current_subject = None
        self.current_topic = None
    
    def setup_api_key(self):
        """Set up the API key."""
        if self.api_key:
            print_message(f"Using existing API key: {self.api_key[:5]}...{self.api_key[-5:]}")
            if not get_confirmation("Do you want to continue with this API key?"):
                self.api_key = None
        
        if not self.api_key:
            print_message("Please enter your Gemini API key to continue.")
            print_message("You can get an API key from https://aistudio.google.com/app/apikey")
            self.api_key = get_input("API Key: ", password=True)
            save_api_key(self.api_key)
        
        try:
            self.client = GeminiClient(api_key=self.api_key)
            print_message("API key validated successfully!", style="bold green")
            return True
        except Exception as e:
            print_error(f"Failed to initialize Gemini client: {str(e)}")
            self.api_key = None
            return False
    
    def select_subject(self):
        """Select a subject to study."""
        subjects = get_subjects_list()
        print_subject_table(subjects)
        
        valid_codes = [code for code, _, _ in subjects]
        while True:
            subject_code = get_input("Select a subject (enter code): ").lower()
            if subject_code in valid_codes:
                self.current_subject = subject_code
                subject_name = next(name for code, name, _ in subjects if code == subject_code)
                print_message(f"Selected subject: {subject_name}", style="bold green")
                return True
            else:
                print_error(f"Invalid subject code. Please choose from: {', '.join(valid_codes)}")
    
    def select_topic(self):
        """Select a topic within the subject."""
        print_message(f"What specific topic in {self.current_subject.capitalize()} do you want to learn about?")
        self.current_topic = get_input("Topic: ")
        return True
    
    def ask_question(self):
        """Ask a question about the selected topic."""
        print_message(f"What's your question about {self.current_topic}?")
        question = get_input("Question: ")
        
        prompt = get_subject_prompt(self.current_subject, self.current_topic, question)
        
        try:
            response_stream = self.client.generate_response(
                prompt=prompt,
                system_instruction=SYSTEM_INSTRUCTION,
                stream=True
            )
            
            full_response = stream_response(response_stream)
            
            # Save to history
            save_to_history(self.current_subject, self.current_topic, question, full_response)
            
            return True
        except Exception as e:
            print_error(f"Error generating response: {str(e)}")
            return False
    
    def run(self):
        """Run the Education CLI."""
        print_header()
        
        # Setup API key
        if not self.setup_api_key():
            print_message("Please restart the application with a valid API key.", style="bold red")
            return
        
        while True:
            # Select subject
            if not self.select_subject():
                continue
            
            # Select topic
            if not self.select_topic():
                continue
            
            # Ask questions in a loop
            while True:
                if not self.ask_question():
                    break
                
                if not get_confirmation("Do you want to ask another question about this topic?"):
                    break
            
            if not get_confirmation("Do you want to explore another subject?"):
                print_message("Thank you for using the Education CLI. Goodbye!", style="bold blue")
                break
