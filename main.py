from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.indexing import router as indexing_router
from api.generate import router as generate_router
from api.models import router as models_router

app = FastAPI(
    title="RAGgamuffin Samurai API",
    description="This API indexes documents and generates responses.",
    version="1.0.0",
    docs_url="/docs",       
    redoc_url="/redoc",       
    openapi_url="/openapi.json" 
)

# Redirect home to docs
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Include routers with prefix /api and proper tags.
app.include_router(indexing_router, prefix="/api", tags=["Indexing"])
app.include_router(generate_router, prefix="/api", tags=["Generation"])
app.include_router(models_router, prefix="/api", tags=["Models"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
