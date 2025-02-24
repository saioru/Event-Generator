"""Application"""
import logging
from typing import Union

import openai
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from src.core import GRAPH

# Initialize - FastAPI Application
app = FastAPI()

# Configure - Logger
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Define - Request body model
class RequestModel(BaseModel):
    """Pydantic Class for API request body"""
    request: str

# Define - Response model
class ResponseModel(BaseModel):
    """Pydantic Class for API response body"""
    output: Union[str, list]

# Define - Route to execute module inference
@app.post("/run", response_model=ResponseModel)
async def run(request: RequestModel):
    """_summary_

    Args:
        request (RequestModel): RequestModel request body structure.
    """
    # Validate input
    if not request.request.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request input shan't not be empty"
        )
    try:
        _output = GRAPH.invoke({'request': request})['output']
        return ResponseModel(output=_output)
    except openai.BadRequestError as err:
        LOGGER.error("OpenAI API error: %s", err)
        return ResponseModel(output="This request violates OpenAI content policy")
    except Exception as e:
        LOGGER.error("Unexpected error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) from e

# To run the app, use: uvicorn main:app --reload
