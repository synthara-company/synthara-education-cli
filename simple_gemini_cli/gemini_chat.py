#!/usr/bin/env python3
"""
Simple Gemini CLI - A chatbot-like interface for Gemini API
"""
import os
import sys
import json
import argparse
from pathlib import Path
import google.generativeai as genai
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

# Initialize console
console = Console()

# Configuration
CONFIG_DIR = Path.home() / ".gemini_cli"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

# Available models
AVAILABLE_MODELS = {
    "flash": "gemini-1.5-flash",
    "pro": "gemini-1.5-pro",
    "preview": "gemini-2.5-pro-preview-03-25"
}

# Default model
DEFAULT_MODEL = "flash"  # Use the flash model by default as it has higher quota limits

def ensure_config_dir():
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(exist_ok=True)

    # Create config file if it doesn't exist
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"api_key": None}, f)

def get_api_key():
    """Get the API key from the configuration file or environment."""
    # First check environment variable
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    # Then check config file
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config.get("api_key")
    except (json.JSONDecodeError, FileNotFoundError):
        return None

def save_api_key(api_key):
    """Save the API key to the configuration file."""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        config = {}

    config["api_key"] = api_key

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def setup_api_key(force_new=False):
    """Set up the API key.

    Args:
        force_new: If True, always ask for a new API key.
    """
    api_key = None if force_new else get_api_key()

    if api_key and not force_new:
        use_existing = Prompt.ask(
            "[bold yellow]Do you want to use your existing API key?[/bold yellow] (yes/no)",
            choices=["yes", "no"],
            default="yes"
        )

        if use_existing.lower() != "yes":
            api_key = None
        else:
            console.print(f"[bold green]Using existing API key[/bold green]")
            return api_key

    if not api_key or force_new:
        console.print("[bold yellow]Please enter your Gemini API key.[/bold yellow]")
        console.print("You can get an API key from [link=https://aistudio.google.com/app/apikey]https://aistudio.google.com/app/apikey[/link]")
        console.print("Make sure your API key has not exceeded its quota.")

        api_key = Prompt.ask("API Key", password=True)
        save_api_key(api_key)

        # Clear any environment variable to ensure we're using the new key
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]

        # Set the new key in the environment
        os.environ["GEMINI_API_KEY"] = api_key

    return api_key

def test_api_key(api_key):
    """Test if the API key works by making a simple request."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Make a simple request to test the API key
        _ = model.generate_content("Hello, this is a test.")
        return True
    except Exception as e:
        error_msg = str(e)
        console.print(f"[bold red]API Key Test Failed: {error_msg}[/bold red]")

        # Handle quota exceeded error
        if "quota exceeded" in error_msg.lower() or "429" in error_msg:
            console.print(Panel(
                "[bold yellow]API quota exceeded.[/bold yellow]\n\n"
                "This usually means one of the following:\n"
                "1. You've used all your free credits\n"
                "2. Your API key is invalid\n"
                "3. You need to enable billing\n\n"
                "Visit [link=https://aistudio.google.com/app/apikey]https://aistudio.google.com/app/apikey[/link] "
                "to check your API key status or create a new one.",
                title="Quota Error",
                border_style="yellow"
            ))
        return False

def initialize_gemini(api_key, model_key=None):
    """Initialize the Gemini API.

    Args:
        api_key: The API key to use
        model_key: The model key to use (from AVAILABLE_MODELS)
    """
    try:
        # First test the API key
        if not test_api_key(api_key):
            return None

        # Use the specified model or default
        model_key = model_key or DEFAULT_MODEL
        if model_key not in AVAILABLE_MODELS:
            console.print(f"[bold yellow]Unknown model '{model_key}'. Using default model.[/bold yellow]")
            model_key = DEFAULT_MODEL

        model_name = AVAILABLE_MODELS[model_key]
        console.print(f"[bold green]Using model: {model_name}[/bold green]")

        genai.configure(api_key=api_key)

        # Configure the model to generate plain text
        # We'll handle markdown formatting ourselves
        generation_config = {
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name,
            generation_config=generation_config
        )
        return model
    except Exception as e:
        console.print(f"[bold red]Error initializing Gemini API: {str(e)}[/bold red]")
        return None

def stream_response(response_stream):
    """Stream the response to the console with markdown formatting."""
    import time
    import random

    full_response = ""

    # Create a newspaper-style header
    console.print("\n[bold]══════════════════════════════════════════════════════════════════════[/bold]")
    console.print("[bold gradient(blue,cyan)]SYNTHARA | THE EDUCATION TIMES[/bold gradient(blue,cyan)]")
    console.print("[dim italic]Your premium source for knowledge and insights[/dim italic]")
    console.print("[bold]══════════════════════════════════════════════════════════════════════[/bold]")
    console.print("")

    try:
        # Collect the entire response first
        for chunk in response_stream:
            # Handle different response formats
            if hasattr(chunk, 'text'):
                text = chunk.text
            elif hasattr(chunk, 'parts') and chunk.parts:
                text = chunk.parts[0].text
            else:
                text = str(chunk)

            if text:
                full_response += text

        # Format the response as markdown
        try:
            # Apply markdown formatting
            md = Markdown(full_response)
            console.print(md)
        except Exception:
            # If markdown parsing fails, just print the raw text with typing effect
            for char in full_response:
                delay = random.uniform(0.001, 0.01)  # Between 1-10ms
                time.sleep(delay)
                console.print(char, end="")
                sys.stdout.flush()
            console.print("\n")

        # Print a newspaper-style footer
        console.print("\n[bold]══════════════════════════════════════════════════════════════════════[/bold]")
        console.print("[dim italic]© " + time.strftime("%Y") + " Synthara | The Education Times. All rights reserved.[/dim italic]")
        console.print("[bold]══════════════════════════════════════════════════════════════════════[/bold]")
        console.print("\n")

    except Exception as e:
        console.print(f"\n[bold red]Error during streaming: {str(e)}[/bold red]")

    return full_response

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Simple Gemini CLI")
    parser.add_argument("--api-key", help="Gemini API key (overrides saved key)")
    args = parser.parse_args()

    # Set API key from command line if provided
    if args.api_key:
        os.environ["GEMINI_API_KEY"] = args.api_key

    # Print a fancy welcome message
    console.print("\n")
    console.print("[bold cyan]╔" + "═" * 60 + "╗[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + " " * 60 + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + "[bold blue]Synthara | Department of Education Gemini CLI[/bold blue]".center(60) + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + "[italic]A premium article-style interface for students[/italic]".center(60) + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + " " * 60 + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + "Commands:".center(60) + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + "[bold]'exit'[/bold] or [bold]'quit'[/bold] - End the conversation".center(60) + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + "[bold]'key'[/bold] - Update your API key".center(60) + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + "[bold]'model'[/bold] - Change the AI model".center(60) + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + " " * 60 + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + f"Available models: {', '.join(AVAILABLE_MODELS.keys())}".center(60) + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]║[/bold cyan]" + " " * 60 + "[bold cyan]║[/bold cyan]")
    console.print("[bold cyan]╚" + "═" * 60 + "╝[/bold cyan]")
    console.print("\n")

    # Setup API key - force a new key to ensure we're not using a cached one with quota issues
    api_key = setup_api_key(force_new=True)
    if not api_key:
        console.print("[bold red]No API key provided. Exiting...[/bold red]")
        return 1

    # Initialize Gemini
    model = initialize_gemini(api_key)
    if not model:
        return 1

    # Start chat session
    chat = model.start_chat(history=[])

    # Main chat loop
    try:
        while True:
            # Get user input with a newspaper-style prompt
            console.print("\n[bold]══════════════════════════════════════════════════════════════════════[/bold]")
            console.print("[bold gradient(green,yellow)]READER INQUIRY[/bold gradient(green,yellow)]")
            console.print("[dim italic]Submit your question or topic for our next article[/dim italic]")
            console.print("[bold]══════════════════════════════════════════════════════════════════════[/bold]")
            user_input = Prompt.ask("")

            # Check for special commands
            if user_input.lower() in ['exit', 'quit']:
                # Print a fancy goodbye message
                console.print("\n")
                console.print("[bold magenta]╔" + "═" * 40 + "╗[/bold magenta]")
                console.print("[bold magenta]║[/bold magenta]" + " " * 40 + "[bold magenta]║[/bold magenta]")
                console.print("[bold magenta]║[/bold magenta]" + "[bold blue]Thank you for using Synthara Gemini CLI![/bold blue]".center(40) + "[bold magenta]║[/bold magenta]")
                console.print("[bold magenta]║[/bold magenta]" + "[italic]Goodbye and have a wonderful day![/italic]".center(40) + "[bold magenta]║[/bold magenta]")
                console.print("[bold magenta]║[/bold magenta]" + " " * 40 + "[bold magenta]║[/bold magenta]")
                console.print("[bold magenta]╚" + "═" * 40 + "╝[/bold magenta]")
                console.print("\n")
                break
            elif user_input.lower() == 'key':
                console.print("[bold yellow]Updating API key...[/bold yellow]")
                # Force a new API key
                new_key = setup_api_key(force_new=True)
                if not new_key:
                    console.print("[bold red]No API key provided. Continuing with previous key.[/bold red]")
                    continue

                console.print("[bold green]API key updated. Reinitializing...[/bold green]")

                # Reinitialize with new key
                model = initialize_gemini(new_key)
                if not model:
                    console.print("[bold red]Failed to initialize with new key. Please try again.[/bold red]")
                    continue

                chat = model.start_chat(history=[])
                console.print("[bold green]Successfully connected with new API key![/bold green]")
                continue
            elif user_input.lower() == 'model':
                console.print("[bold yellow]Select a model:[/bold yellow]")
                console.print(f"Available models: {', '.join(AVAILABLE_MODELS.keys())}")
                model_key = Prompt.ask(
                    "Model",
                    choices=list(AVAILABLE_MODELS.keys()),
                    default=DEFAULT_MODEL
                )

                console.print(f"[bold green]Switching to model: {AVAILABLE_MODELS[model_key]}[/bold green]")

                # Reinitialize with new model
                model = initialize_gemini(api_key, model_key)
                if not model:
                    console.print("[bold red]Failed to initialize with new model. Please try again.[/bold red]")
                    continue

                chat = model.start_chat(history=[])
                console.print("[bold green]Successfully switched model![/bold green]")
                continue

            # Handle commands that might be mistaken for regular input
            elif user_input.lower() in AVAILABLE_MODELS.keys():
                console.print(f"[bold yellow]Switching to model: {AVAILABLE_MODELS[user_input.lower()]}[/bold yellow]")
                model = initialize_gemini(api_key, user_input.lower())
                if not model:
                    console.print("[bold red]Failed to initialize with new model. Please try again.[/bold red]")
                    continue
                chat = model.start_chat(history=[])
                console.print("[bold green]Successfully switched model![/bold green]")
                continue

            # Generate response
            try:
                # Add system instruction to format responses like a news article or blog post
                system_instruction = (
                    "IMPORTANT: Format your responses like a professional news article or blog post.\n\n"
                    "Your writing style should be:\n"
                    "1. Engaging and conversational\n"
                    "2. Include strong opinions and analysis\n"
                    "3. Use a journalistic tone with clear paragraphs\n"
                    "4. Include rhetorical questions to engage the reader\n"
                    "5. Use markdown formatting extensively\n\n"

                    "Format requirements:\n"
                    "- Start with a compelling introduction paragraph\n"
                    "- Use ## for section headings to break up content\n"
                    "- Bold important points with **text**\n"
                    "- Use blockquotes (>) for emphasis or quotes\n"
                    "- Include numbered lists for sequential points\n"
                    "- Use bullet points for related items\n"
                    "- End with a strong conclusion\n\n"

                    "Example format:\n"
                    "[Introduction paragraph with context and hook]\n\n"
                    "## First Important Point\n\n"
                    "[Detailed paragraph with **bold emphasis** on key points]\n\n"
                    "> Important quote or emphasized text here\n\n"
                    "[Another paragraph with supporting details]\n\n"
                    "## Second Important Point\n\n"
                    "1. First sequential item\n"
                    "2. Second sequential item\n\n"
                    "[Conclusion paragraph]\n\n"

                    "Your response MUST follow this journalistic style with proper markdown formatting."
                )

                # For the first message, include system instruction
                if not hasattr(chat, '_message_sent'):
                    full_prompt = f"{system_instruction}\n\nUser: {user_input}"
                    chat._message_sent = True
                else:
                    full_prompt = user_input

                # Send the message and stream the response
                response = chat.send_message(full_prompt, stream=True)
                stream_response(response)
            except Exception as e:
                error_msg = str(e)
                console.print(f"[bold red]Error: {error_msg}[/bold red]")

                # Handle quota exceeded error
                if "quota exceeded" in error_msg.lower() or "429" in error_msg:
                    console.print(Panel(
                        "[bold yellow]API quota exceeded.[/bold yellow]\n\n"
                        "This usually means one of the following:\n"
                        "1. You've used all your free credits\n"
                        "2. Your API key is invalid\n"
                        "3. You need to enable billing\n\n"
                        "Visit [link=https://aistudio.google.com/app/apikey]https://aistudio.google.com/app/apikey[/link] "
                        "to check your API key status or create a new one.\n\n"
                        "Type [bold]'key'[/bold] to enter a new API key or try a different model with [bold]'model'[/bold].",
                        title="Quota Error",
                        border_style="yellow"
                    ))

    except KeyboardInterrupt:
        # Print a fancy goodbye message
        console.print("\n")
        console.print("[bold magenta]╔" + "═" * 40 + "╗[/bold magenta]")
        console.print("[bold magenta]║[/bold magenta]" + " " * 40 + "[bold magenta]║[/bold magenta]")
        console.print("[bold magenta]║[/bold magenta]" + "[bold blue]Thank you for using Synthara Gemini CLI![/bold blue]".center(40) + "[bold magenta]║[/bold magenta]")
        console.print("[bold magenta]║[/bold magenta]" + "[italic]Goodbye and have a wonderful day![/italic]".center(40) + "[bold magenta]║[/bold magenta]")
        console.print("[bold magenta]║[/bold magenta]" + " " * 40 + "[bold magenta]║[/bold magenta]")
        console.print("[bold magenta]╚" + "═" * 40 + "╝[/bold magenta]")
        console.print("\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
