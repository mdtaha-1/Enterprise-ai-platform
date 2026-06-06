from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, Depends
from app.api.chat import router as chat_router
from app.api.rag import router as rag_router
from app.api.agent import router as agent_router
from app.api.image import router as image_router
from app.core.auth import verify_api_key

app = FastAPI(
    title="EnterpriseAI Platform",
    description="Self-hosted multi-modal AI backend",
    version="1.0.0"
)

# Public route
@app.get("/")
async def root():
    return {"status": "EnterpriseAI Platform is running 🚀"}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ui")
async def serve_ui():
    return FileResponse("static/index.html")
# Protected routes
app.include_router(chat_router, prefix="/api/v1", dependencies=[Depends(verify_api_key)])
app.include_router(rag_router, prefix="/api/v1/rag", dependencies=[Depends(verify_api_key)])
app.include_router(agent_router, prefix="/api/v1/agent", dependencies=[Depends(verify_api_key)])
app.include_router(image_router, prefix="/api/v1/image", dependencies=[Depends(verify_api_key)])