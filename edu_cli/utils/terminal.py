"""
Terminal utilities for the Education CLI.
"""
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.table import Table
import pyfiglet

console = Console()

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header."""
    clear_screen()
    header = pyfiglet.figlet_format("Edu Assistant", font="slant")
    console.print(Panel(header, subtitle="Department of Education CLI", style="bold blue"))

def print_message(message, style="green"):
    """Print a styled message."""
    console.print(message, style=style)

def print_error(message):
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")

def print_thinking():
    """Print a thinking message."""
    with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
        yield

def print_subject_table(subjects):
    """Print a table of available subjects."""
    table = Table(title="Available Subjects")
    table.add_column("Code", style="cyan")
    table.add_column("Subject", style="green")
    table.add_column("Description", style="yellow")

    for code, name, description in subjects:
        table.add_row(code, name, description)

    console.print(table)

def get_input(prompt, password=False):
    """Get user input with a styled prompt."""
    return Prompt.ask(prompt, password=password)

def get_confirmation(prompt):
    """Get user confirmation."""
    return Confirm.ask(prompt)

def print_response(text):
    """Print the AI response in a styled panel."""
    console.print(Panel(text, title="Tutor Response", border_style="green"))

def stream_response(response_stream):
    """Stream the AI response to the console."""
    console.print(Panel("", title="Tutor Response", border_style="green", title_align="left"), end="")

    # Move cursor to panel content area
    sys.stdout.write("\033[A")  # Move up one line
    sys.stdout.write("\033[3C")  # Move right 3 characters

    full_response = ""
    for chunk in response_stream:
        # Handle different response formats
        if hasattr(chunk, 'text'):
            text = chunk.text
        elif hasattr(chunk, 'parts') and chunk.parts:
            text = chunk.parts[0].text
        else:
            text = str(chunk)

        if text:
            sys.stdout.write(text)
            sys.stdout.flush()
            full_response += text

    # Print newline after response
    print("\n")
    return full_response
