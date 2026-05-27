from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import structlog

from backend.services import (
    session_manager,
    llm_service,
    tts_service,
    livekit_service
)

logger = structlog.get_logger()

router = APIRouter()


# Request/Response Models
class CreateSessionRequest(BaseModel):
    """Request model for creating a new session."""
    session_id: Optional[str] = None
    system_prompt: Optional[str] = None


class SessionResponse(BaseModel):
    """Response model for session information."""
    session_id: str
    token: str
    room_name: str
    status: str


class STTTranscriptRequest(BaseModel):
    """Request model for receiving STT transcript from frontend."""
    session_id: str
    transcript: str
    is_final: bool = False
    is_interim: bool = False


class LLMResponse(BaseModel):
    """Response model for LLM response."""
    session_id: str
    response: str
    streaming: bool = False


class TTSRequest(BaseModel):
    """Request model for TTS generation."""
    session_id: str
    text: str
    voice: Optional[str] = None


class TTSResponse(BaseModel):
    """Response model for TTS result."""
    session_id: str
    job_id: Optional[str] = None
    audio_url: Optional[str] = None
    status: str


class TokenRequest(BaseModel):
    """Request model for generating LiveKit token."""
    session_id: str
    participant_name: Optional[str] = "User"


class TokenResponse(BaseModel):
    """Response model for LiveKit token."""
    token: str
    room_name: str
    livekit_url: str


# Session Management Routes
@router.post("/session", response_model=SessionResponse)
async def create_session(request: CreateSessionRequest):
    """Create a new conversation session."""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Create session in session manager
        session_manager.create_session(session_id, request.system_prompt)
        
        # Create LiveKit room
        room_name = f"voice-session-{session_id[:8]}"
        await livekit_service.create_room(room_name)
        
        # Generate token for frontend
        token = livekit_service.generate_token(
            room_name=room_name,
            participant_identity=f"user-{session_id[:8]}",
            participant_name=request.participant_name if hasattr(request, 'participant_name') else "User",
            is_bot=False
        )
        
        logger.info("session_created_successfully", session_id=session_id, room_name=room_name)
        
        return SessionResponse(
            session_id=session_id,
            token=token,
            room_name=room_name,
            status="active"
        )
    
    except Exception as e:
        logger.error("session_creation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session information."""
    session_status = session_manager.get_session_status(session_id)
    
    if not session_status:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session_status


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    try:
        session_manager.clear_session(session_id)
        
        # Clean up LiveKit room
        room_name = f"voice-session-{session_id[:8]}"
        await livekit_service.delete_room(room_name)
        
        return {"status": "deleted", "session_id": session_id}
    
    except Exception as e:
        logger.error("session_deletion_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")


# LiveKit Token Route
@router.post("/token", response_model=TokenResponse)
async def generate_token(request: TokenRequest):
    """Generate a LiveKit access token."""
    try:
        room_name = f"voice-session-{request.session_id[:8]}"
        
        token = livekit_service.generate_token(
            room_name=room_name,
            participant_identity=f"user-{request.session_id[:8]}",
            participant_name=request.participant_name,
            is_bot=False
        )
        
        return TokenResponse(
            token=token,
            room_name=room_name,
            livekit_url=settings.LIVEKIT_URL
        )
    
    except Exception as e:
        logger.error("token_generation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to generate token: {str(e)}")


# Conversation Routes
@router.post("/conversation")
async def process_conversation(request: STTTranscriptRequest):
    """
    Process STT transcript and generate LLM response.
    This is called by the frontend when speech is recognized.
    """
    try:
        session_id = request.session_id
        
        # Only process final transcripts
        if not request.is_final:
            return {"status": "interim", "transcript": request.transcript}
        
        # Add user message to session
        session_manager.add_message(session_id, "user", request.transcript)
        
        # Get conversation history for LLM
        messages = session_manager.get_messages_for_llm(session_id)
        
        # Generate LLM response
        full_response = ""
        async for chunk in llm_service.generate_stream(messages, session_id):
            full_response += chunk
        
        if not full_response:
            raise HTTPException(status_code=500, detail="Empty LLM response")
        
        # Add assistant response to session
        session_manager.add_message(session_id, "assistant", full_response)
        
        logger.info(
            "conversation_processed",
            session_id=session_id,
            user_text=request.transcript[:50],
            response_length=len(full_response)
        )
        
        return {
            "status": "success",
            "session_id": session_id,
            "user_transcript": request.transcript,
            "assistant_response": full_response
        }
    
    except Exception as e:
        logger.error("conversation_processing_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to process conversation: {str(e)}")


# TTS Routes
@router.post("/tts", response_model=TTSResponse)
async def generate_tts(request: TTSRequest, background_tasks: BackgroundTasks):
    """Generate TTS audio from text."""
    try:
        # Start TTS job in background
        job_id = await tts_service.create_tts_job(
            text=request.text,
            voice=request.voice,
            session_id=request.session_id
        )
        
        # Return job ID immediately (frontend will poll or wait)
        return TTSResponse(
            session_id=request.session_id,
            job_id=job_id,
            status="processing"
        )
    
    except Exception as e:
        logger.error("tts_generation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to generate TTS: {str(e)}")


@router.get("/tts/{job_id}/status")
async def get_tts_status(job_id: str, session_id: Optional[str] = None):
    """Check TTS job status."""
    try:
        status_data = await tts_service.check_job_status(job_id, session_id)
        return status_data
    
    except Exception as e:
        logger.error("tts_status_check_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to check TTS status: {str(e)}")


@router.get("/tts/{job_id}/audio")
async def get_tts_audio(job_id: str, session_id: Optional[str] = None):
    """Download TTS audio file."""
    try:
        from fastapi.responses import Response
        
        audio_bytes, audio_format = await tts_service.download_audio(job_id, session_id)
        
        content_type = "audio/wav" if audio_format == "wav" else "audio/mpeg"
        
        return Response(
            content=audio_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename=tts-{job_id}.{audio_format}"
            }
        )
    
    except Exception as e:
        logger.error("tts_audio_download_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to download TTS audio: {str(e)}")


# Conversation History Route
@router.get("/conversation/{session_id}/history")
async def get_conversation_history(session_id: str):
    """Get conversation history for a session."""
    history = session_manager.get_conversation_history(session_id)
    
    return {
        "session_id": session_id,
        "messages": history,
        "count": len(history)
    }


# Voices Route
@router.get("/voices")
async def list_voices():
    """List available TTS voices."""
    try:
        voices = await tts_service.list_voices()
        return {"voices": voices}
    
    except Exception as e:
        logger.error("voices_listing_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to list voices: {str(e)}")


# Import settings for LIVEKIT_URL
from backend.config import settings
