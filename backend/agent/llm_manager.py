# agent/llm_manager.py

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


def get_llm():
    """
    Initializes and returns the language model.

    Tries to initialize the specified Gemini model using a Google API key.
    If that fails, it falls back to a local Ollama model.
    """
    try:
        # Using the specific model you mentioned
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",  # Updated to the model you are using
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7,
            convert_system_message_to_human=True
        )
        print("[✅] Successfully initialized Gemini-1.5-Flash.")
        return llm
    except Exception as e:
        # Fallback choice: Local Ollama model
        print(f"[⚠️ Gemini initialization failed: {str(e)}]")
        print("[🔄] Switching to Ollama with 'mistral' model.")
        return ChatOllama(model="mistral", temperature=0.7)
