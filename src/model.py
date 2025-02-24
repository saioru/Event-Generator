"""Model Initialization (Azure)"""
import os
from dotenv import load_dotenv

from langchain_openai.chat_models.azure import AzureChatOpenAI

load_dotenv()

LLM = AzureChatOpenAI(
    seed=42,
    temperature=0.0,
    deployment_name=os.getenv("LLM_MODEL")
)
