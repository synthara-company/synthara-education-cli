# Contributing to Synthara | The Education Times CLI

Thank you for considering contributing to Synthara! This document outlines the process for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

- Check if the bug has already been reported in the [Issues](https://github.com/bniladridas/gemini_cli/issues)
- If not, create a new issue with a descriptive title and clear steps to reproduce
- Include as much relevant information as possible (OS, Python version, etc.)

### Suggesting Features

- Check if the feature has already been suggested in the [Issues](https://github.com/bniladridas/gemini_cli/issues)
- If not, create a new issue with a descriptive title and detailed description of the feature
- Explain why this feature would be useful to most users

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Development Setup

1. Clone your fork of the repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install google-generativeai rich
   ```

## Style Guidelines

- Follow PEP 8 style guidelines for Python code
- Use descriptive variable names
- Add comments for complex logic
- Write docstrings for functions and classes

## Testing

- Test your changes thoroughly before submitting a pull request
- Ensure your changes don't break existing functionality

## License

By contributing to Synthara, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

Thank you for your contributions!
