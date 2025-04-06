from setuptools import setup, find_packages

setup(
    name="edu_cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai>=0.3.0",
        "rich>=10.0.0",
        "prompt-toolkit>=3.0.0",
        "pyfiglet>=0.8.post1",
    ],
    entry_points={
        "console_scripts": [
            "edu-cli=edu_cli.main:main",
        ],
    },
    author="Department of Education",
    author_email="example@education.gov",
    description="A CLI system for students to interact with AI tutors",
    keywords="education, cli, ai, tutor",
    python_requires=">=3.7",
)
