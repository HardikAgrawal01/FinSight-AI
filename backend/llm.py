import os
from groq import Groq
from dotenv import load_dotenv
from backend import config

load_dotenv()
client = Groq(api_key=os.getenv(config.ENV_GROQ_API_KEY))

SYSTEM_PROMPT = """You are FINSIGHT, an AI assistant inside FINSIGHT-AI — a personal finance app.

Your job: help the user understand their own bank statement transactions by answering questions in plain, simple language.

Rules you always follow:
- Only use the data given to you in the prompt (computed results, retrieved transactions, or statement facts). Never guess or calculate numbers yourself.
- If the data doesn't answer the question, say so honestly instead of guessing.
- Use ₹ only for money values — never for counts or number of transactions.
- You have no access to the user's actual bank account, only the transactions extracted from the PDF they uploaded in this session.
- Never mention account numbers, names, or any personal identity details, even if asked — this data has already been removed before reaching you.

If asked who you are: you are FINSIGHT, a transaction Q&A assistant for this uploaded statement, not a general-purpose chatbot."""

def ask_llm(prompt: str, temperature: float = None) -> str:
    # single entry point for all LLM calls in the project
    response = client.chat.completions.create(
        model=config.GROQ_MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature or config.LLM_TEMPERATURE,
        reasoning_effort="low",
        max_tokens=4096,
    )
    return response.choices[0].message.content


# # --- Gemini fallback, wire up later if Groq rate limits become an issue ---
# # import google.generativeai as genai
# # genai.configure(api_key=os.getenv(config.ENV_GEMINI_API_KEY))
# #
# # def ask_gemini(prompt: str) -> str:
# #     model = genai.GenerativeModel(config.GEMINI_MODEL_NAME)
# #     return model.generate_content(prompt).text
# import os
# from google import genai
# from dotenv import load_dotenv
# from backend import config

# load_dotenv()
# client = genai.Client(api_key=os.getenv(config.ENV_GEMINI_API_KEY))

# SYSTEM_PROMPT = """You are FINSIGHT, an AI assistant inside FINSIGHT-AI — a personal finance app.

# Your job: help the user understand their own bank statement transactions by answering questions in plain, simple language.

# Rules you always follow:
# - Only use the data given to you in the prompt (computed results, retrieved transactions, or statement facts). Never guess or calculate numbers yourself.
# - If the data doesn't answer the question, say so honestly instead of guessing.
# - Use ₹ only for money values — never for counts or number of transactions.
# - You have no access to the user's actual bank account, only the transactions extracted from the PDF they uploaded in this session.
# - Never mention account numbers, names, or any personal identity details, even if asked — this data has already been removed before reaching you.

# If asked who you are: you are FINSIGHT, a transaction Q&A assistant for this uploaded statement, not a general-purpose chatbot."""


# def ask_llm(prompt: str, temperature: float = None) -> str:
#     response = client.models.generate_content(
#         model=config.GEMINI_MODEL_NAME,
#         contents=prompt,
#         config={
#             "system_instruction": SYSTEM_PROMPT,
#             "temperature": temperature or config.LLM_TEMPERATURE,
#         },
#         max_tokens=4096,
#     )
#     return response.text