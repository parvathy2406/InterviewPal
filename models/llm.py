from config.config import Config
from models.groq_llm import groq_answer

def generate_answer(system_prompt, user_prompt, mode="concise", temperature=0.2):

    # If Groq key exists, use Groq
    if Config.GROQ_API_KEY:
        return groq_answer(user_prompt)

    # Otherwise fallback
    return (
        "[FALLBACK] No LLM available.\n"
        "Retrieved context:\n\n"
        + user_prompt
    )
