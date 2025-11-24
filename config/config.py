import os

class Config:
    APP_NAME = "InterviewPal"

    # API keys 
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Model settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
