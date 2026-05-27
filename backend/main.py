from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
import uuid
from contextlib import asynccontextmanager

from backend.config import settings
from backend.utils import setup_logging
from backend.services import (
    session_manager,
    llm_service,
    tts_service,
    livekit_service
)
from backend.api.routes import router as api_router

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    # Startup
    logger.info("application_starting", version="1.0.0")
    
    # Setup logging
    setup_logging()
    
    # Test connections (non-blocking)
    try:
        livekit_ok = await livekit_service.test_connection()
        logger.info("livekit_status", connected=livekit_ok)
    except Exception as e:
        logger.warning("livekit_connection_failed", error=str(e))
    
    # Run periodic session cleanup
    import asyncio
    async def cleanup_loop():
        while True:
            await asyncio.sleep(300)  # Every 5 minutes
            session_manager.cleanup_expired_sessions()
    
    asyncio.create_task(cleanup_loop())
    
    yield
    
    # Shutdown
    logger.info("application_shutting_down")
    await llm_service.close()
    await tts_service.close()


app = FastAPI(
    title="AI Voice Agent API",
    description="Realtime AI Voice Agent Backend with LiveKit",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


@app.get("/api/status")
async def api_status():
    """Get API status and service health."""
    status = {
        "api": "operational",
        "services": {}
    }
    
    # Check LiveKit
    try:
        livekit_ok = await livekit_service.test_connection()
        status["services"]["livekit"] = "operational" if livekit_ok else "degraded"
    except:
        status["services"]["livekit"] = "down"
    
    # Check LLM
    try:
        llm_ok = await llm_service.test_connection()
        status["services"]["llm"] = "operational" if llm_ok else "degraded"
    except:
        status["services"]["llm"] = "down"
    
    # Check TTS
    try:
        tts_ok = await tts_service.test_connection()
        status["services"]["tts"] = "operational" if tts_ok else "degraded"
    except:
        status["services"]["tts"] = "down"
    
    return status


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error("unhandled_exception", error=str(exc), path=str(request.url))
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.ENVIRONMENT == "development" else None
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower()
    )
