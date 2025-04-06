# Simple Gemini CLI

A simple, Ollama-like chatbot interface for the Gemini API.

## Features

- Clean, simple chat interface
- Streaming responses
- API key management
- Easy to use

## Requirements

- Python 3.7 or higher
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Installation

1. Make sure you have the required dependencies:
   ```
   pip install google-generativeai rich
   ```

2. Run the script:
   ```
   ./gemini-chat
   ```

## Usage

1. On first run, you'll be prompted to enter your Gemini API key
2. Type your messages and press Enter
3. Type 'exit' or 'quit' to end the conversation

## API Key

You can provide your API key in several ways:
- Enter it when prompted on first run
- Set the GEMINI_API_KEY environment variable
- Pass it as a command-line argument: `./gemini-chat --api-key YOUR_API_KEY`
