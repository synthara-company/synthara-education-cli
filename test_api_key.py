#!/usr/bin/env python3
"""
Simple script to test a Gemini API key
"""
import sys
import google.generativeai as genai

def test_key(api_key):
    """Test if the API key works."""
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Try with a simpler model first
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Make a simple request
        response = model.generate_content("Hello, this is a test.")
        
        print("✅ API key is valid!")
        print("Response:", response.text)
        return True
    except Exception as e:
        print("❌ API key test failed!")
        print("Error:", str(e))
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use API key from command line
        api_key = sys.argv[1]
    else:
        # Ask for API key
        print("Please enter your Gemini API key:")
        api_key = input("> ")
    
    if not api_key:
        print("No API key provided. Exiting...")
        sys.exit(1)
    
    # Test the key
    if test_key(api_key):
        print("\nYour API key is working correctly!")
    else:
        print("\nYour API key is not working. Please check it and try again.")
        print("You can get a new API key from: https://aistudio.google.com/app/apikey")
