from config.config import Config
from groq import Groq  # Make sure 'pip install groq' is done

# Initialize real Groq client
client = Groq(api_key=Config.GROQ_API_KEY)

def query_groq(query: str, model: str = "openai/gpt-oss-20b", max_tokens: int = 512):
    """
    Queries Groq's LLM and returns a list of result strings.
    """
    if not Config.GROQ_API_KEY:
        print("Groq API key not set!")
        return []

    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model=model,
            max_tokens=max_tokens,
        )

        # Extract the text output
        content = response.choices[0].message.content
        return [content]

    except Exception as e:
        print(f"Groq API call failed: {e}")
        return []
