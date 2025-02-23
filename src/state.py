"""State Initialization (Graph)"""
from typing_extensions import TypedDict

class State(TypedDict):
    """Inherited class for LangGraph node states"""
    request: str
    validity: str
    intent: str
    output: dict
