"""Core graph module"""
from langgraph.graph import START, StateGraph, END

from src.state import State
from src.nodes.intention_analysis import relevancy_node
from src.nodes.context_generation import context_generation
from src.nodes.fallback_handling import fallback_generation

PIPELINE = StateGraph(State)
PIPELINE.add_node("Intention Analysis", relevancy_node)
PIPELINE.add_node("Context Generation", context_generation)
PIPELINE.add_node("Fallback Generation", fallback_generation)

PIPELINE.add_edge(START, "Intention Analysis")
PIPELINE.add_conditional_edges(
    "Intention Analysis",
    lambda state: state['validity'],
    {'Valid': "Context Generation", 'Invalid': "Fallback Generation"}
)
PIPELINE.add_edge("Context Generation", END)
PIPELINE.add_edge("Fallback Generation", END)

GRAPH = PIPELINE.compile()
