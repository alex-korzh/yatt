import os


CHUNK_SIZE = 128
LINE_LIMIT = 45
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_PROMPT = (
    "Generate a creative and engaging text on a random topic. "
    "The text should be between 1500 and 2000 characters long and "
    "cover the topic in enough detail to be interesting and informative. "
    "Use a neutral tone, and avoid any controversial or sensitive topics. "
    "Make sure the content is suitable for all ages and can be used as a typing exercise."
)
