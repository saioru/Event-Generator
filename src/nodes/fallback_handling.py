"""Fallback Handling Node Initialization"""
from pydantic import BaseModel, Field
from langchain_core.prompts.chat import ChatPromptTemplate

from src.state import State
from src.model import LLM

class RejectParser(BaseModel):
    """Custom Output Parser for Request Rejection"""
    output: str = Field(description="Short descriptive rejection of request")

def fallback_generation(state: State) -> dict:
    """Rejection Node to reject the processing of the received request.

    Args:
        state (State): Graph State passing between node calls.

    Returns:
        dict: Dictionary key-value update for State `output`.
    """
    _response = (
        ChatPromptTemplate.from_template("Reject request based on intent.\nIntent: {intent}")
        | LLM.with_structured_output(RejectParser)
    ).invoke({'intent': state['intent']})
    return {'output': _response.output}
