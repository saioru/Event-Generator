"""Intention Analysis Node Initialization"""
import logging

from pydantic import BaseModel, Field
from langchain_core.prompts.chat import ChatPromptTemplate

from src.state import State
from src.model import LLM

# Set the logging level to ERROR to capture errors
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)

class RelevancyParser(BaseModel):
    """Custom Output Parser for Relevancy Check"""
    validity: str = Field(description="Either 'Valid' or 'Invalid'")
    intent: str = Field(description="Short descriptive intention")

def relevancy_node(state: State) -> dict:
    """Relevancy Node to validate the intention of the received request.

    Args:
        state (State): Graph State passing between node calls.

    Returns:
        dict: Dictionary key-value update for State `validity` and `intent`.
    """
    _response = (
        ChatPromptTemplate.from_template( \
            "Validate only locale, event, venue or service related requests.\nRequest: '{request}")
        | LLM.with_structured_output(RelevancyParser)
    ).invoke({'request': state['request']})

    return {'validity': _response.validity, 'intent': _response.intent}
