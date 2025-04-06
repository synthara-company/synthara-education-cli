#!/usr/bin/env python3
"""
Main entry point for the Department of Education CLI System.
"""
import sys
import os
import argparse
from .cli import EducationCLI
from .utils.terminal import print_header, print_message, print_error

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Department of Education CLI System")
    parser.add_argument("--api-key", help="Gemini API key (overrides saved key)")
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    # Set API key from command line if provided
    if args.api_key:
        os.environ["GEMINI_API_KEY"] = args.api_key
    
    try:
        cli = EducationCLI()
        cli.run()
    except KeyboardInterrupt:
        print_message("\nExiting Education CLI. Goodbye!", style="bold blue")
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
