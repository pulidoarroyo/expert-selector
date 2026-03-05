from google import genai

genai_client = None

try:
    from config import GEMINI_API_KEY

    genai_client = genai.Client(api_key=GEMINI_API_KEY)
except ImportError:
    genai_client = None

GENAI_MODEL = "gemini-2.5-flash-lite"
