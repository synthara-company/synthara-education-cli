from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="synthara-education-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai>=0.3.0",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "synthara-education=simple_gemini_cli.gemini_chat:main",
        ],
    },
    author="Synthara Company",
    author_email="info@synthara.company",
    description="An AI-powered command-line tool that generates beautifully formatted, article-style answers using Google's Gemini Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="education, cli, ai, gemini, article, markdown, newspaper",
    python_requires=">=3.7",
    url="https://github.com/synthara-company/synthara-education-cli",
    project_urls={
        "Bug Tracker": "https://github.com/synthara-company/synthara-education-cli/issues",
        "Documentation": "https://github.com/synthara-company/synthara-education-cli#readme",
        "Source Code": "https://github.com/synthara-company/synthara-education-cli",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
)
