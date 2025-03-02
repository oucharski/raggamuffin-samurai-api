from fastapi import APIRouter, HTTPException
import controllers.ollama_interface as ollama_interface

router = APIRouter()

@router.get("/list-models")
async def list_models():
    """
    Endpoint to list all available models.
    """
    try:
        models = ollama_interface.list_available_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))