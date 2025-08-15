# src/config.py
import os
from dotenv import load_dotenv

# Call this once at the beginning of your application
# to load variables from the .env file.
def load_env():
    """Loads environment variables from a .env file."""
    load_dotenv()
    print("Environment variables loaded.")

def get_key(key: str, default=None):
    """
    Retrieves an environment variable.
    If the key is not found, it returns None or a specified default value.
    """
    return os.getenv(key, default)