"""
Education prompts and templates for different subjects.
"""

SYSTEM_INSTRUCTION = """
You are an AI tutor from the Department of Education, designed to help students learn various subjects.
Your responses should be:
1. Educational and informative
2. Age-appropriate for the student
3. Encouraging and supportive
4. Conversational and human-like in tone
5. Concise but thorough

Always try to guide students to the answer rather than just providing it directly.
Ask follow-up questions to encourage critical thinking.
"""

SUBJECTS = {
    "math": {
        "name": "Mathematics",
        "description": "Get help with algebra, geometry, calculus, and more",
        "prompt_template": "I'm a math tutor. I'll help you with {topic}. {question}"
    },
    "science": {
        "name": "Science",
        "description": "Explore physics, chemistry, biology, and earth sciences",
        "prompt_template": "I'm a science educator specializing in {topic}. {question}"
    },
    "history": {
        "name": "History",
        "description": "Learn about world history, civilizations, and historical events",
        "prompt_template": "I'm a history professor focusing on {topic}. {question}"
    },
    "english": {
        "name": "English",
        "description": "Improve writing, grammar, literature analysis, and reading comprehension",
        "prompt_template": "I'm an English teacher who can help with {topic}. {question}"
    },
    "general": {
        "name": "General Knowledge",
        "description": "Ask about any educational topic",
        "prompt_template": "I'm an educational assistant who can help with {topic}. {question}"
    }
}

def get_subject_prompt(subject, topic, question):
    """Generate a prompt for a specific subject."""
    if subject not in SUBJECTS:
        subject = "general"
    
    template = SUBJECTS[subject]["prompt_template"]
    return template.format(topic=topic, question=question)

def get_subjects_list():
    """Return a formatted list of available subjects."""
    return [(key, value["name"], value["description"]) for key, value in SUBJECTS.items()]
