from fastapi import APIRouter, HTTPException, BackgroundTasks
from controllers.indexing import index_documents

router = APIRouter()

@router.post("/index-db", tags=["Indexing"])
async def index_db_endpoint(background_tasks: BackgroundTasks):
    """
    Endpoint to start document indexing in the background.
    """
    try:
        # Schedule the indexing task to run in the background.
        background_tasks.add_task(index_documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Immediately return a success message.
    return {"message": "Indexing started successfully."}
