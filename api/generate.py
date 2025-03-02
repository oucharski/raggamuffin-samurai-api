from fastapi import APIRouter, HTTPException
import asyncio

import controllers.ollama_interface as ollama_interface
from controllers.models_enum import ModelEnum
from controllers.generate import generate_response_sync

router = APIRouter()

@router.get("/generate-response", tags=["Generation"])
async def generate_response_endpoint(prompt: str, model: ModelEnum):
    """
    Endpoint to generate a response based on a prompt.
    
    Query Parameters:
      - prompt: The input prompt.
      - model: The model to use (selectable from a dropdown in Swagger).
    
    It:
      1. Checks if the requested model is available.
      2. Delegates the response generation logic to the controller.
      3. Returns the generated response.
    """
    # Check if the requested model is available.
    try:
        ollama_interface.check_model_availability(model.value)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    try:
        # Wrap the synchronous controller function in a thread to avoid blocking.
        result = await asyncio.to_thread(generate_response_sync, prompt, model.value)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
