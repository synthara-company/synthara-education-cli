# Synthara | The Education Times CLI

An AI-powered command-line interface that generates article-style responses using Google's Gemini model.

## Features

- Article-style AI responses with proper formatting and markdown
- Support for multiple Gemini models (flash, pro, preview)
- Newspaper-like presentation with headers and footers
- Easy-to-use command-line interface
- Simple one-command installation

## Quick Installation

Install and run with a single command:

```bash
curl -s https://raw.githubusercontent.com/bniladridas/gemini_cli/main/setup.sh | bash
```

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/bniladridas/gemini_cli.git
   cd gemini_cli
   ```

2. Install dependencies:
   ```bash
   pip install google-generativeai rich
   ```

3. Run the application:
   ```bash
   python simple_gemini_cli/gemini_chat.py
   ```

4. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Usage

- Type your questions or topics after the "READER INQUIRY" prompt
- The AI will generate article-style responses formatted like a newspaper

### Commands

- Type `exit` or `quit` to end the session
- Type `key` to update your API key
- Type `model` to switch between different Gemini models:
  - `flash`: Gemini-1.5-flash (fastest, recommended)
  - `pro`: Gemini-1.5-pro (more capable)
  - `preview`: Gemini-2.5-pro-preview (experimental)

## Workflow

1. Enter your Gemini API key when prompted (only needed once)
2. Type your question or topic of interest
3. Receive a professionally formatted article-style response
4. Continue with more questions or type `exit` when done

## Requirements

- Python 3.7 or higher
- Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Internet connection

## Screenshots

[Add screenshots here]

## License

MIT License
