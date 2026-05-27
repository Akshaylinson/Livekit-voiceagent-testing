import asyncio
import httpx
import structlog
from typing import Optional, Tuple
from backend.config import settings

logger = structlog.get_logger()


class CodeVoiceTTSService:
    """CodeVoice TTS service with async job polling."""
    
    def __init__(self):
        self.api_key = settings.CODEVOICE_API_KEY
        self.base_url = settings.CODEVOICE_BASE_URL
        self.default_voice = settings.CODEVOICE_VOICE
        self.poll_interval = settings.CODEVOICE_POLL_INTERVAL
        self.max_polls = settings.CODEVOICE_MAX_POLLS
        self.client = httpx.AsyncClient(timeout=120.0)
    
    async def close(self):
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
    
    async def create_tts_job(
        self,
        text: str,
        voice: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> str:
        """
        Create a TTS job and return the job_id.
        
        Args:
            text: Text to convert to speech
            voice: Voice name (optional, uses default if not provided)
            session_id: Optional session identifier for logging
            
        Returns:
            job_id for the TTS job
        """
        try:
            voice_name = voice or self.default_voice
            
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            }
            
            payload = {
                "text": text,
                "voice": voice_name
            }
            
            logger.info(
                "tts_job_created",
                session_id=session_id,
                voice=voice_name,
                text_length=len(text)
            )
            
            response = await self.client.post(
                f"{self.base_url}/v1/tts",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            
            job_data = response.json()
            job_id = job_data["job_id"]
            
            logger.info("tts_job_initiated", job_id=job_id, session_id=session_id)
            return job_id
        
        except Exception as e:
            logger.error(
                "tts_job_creation_failed",
                error=str(e),
                session_id=session_id
            )
            raise
    
    async def check_job_status(
        self,
        job_id: str,
        session_id: Optional[str] = None
    ) -> dict:
        """
        Check the status of a TTS job.
        
        Args:
            job_id: The job identifier
            session_id: Optional session identifier
            
        Returns:
            Status data dict
        """
        try:
            headers = {
                "X-API-Key": self.api_key,
            }
            
            response = await self.client.get(
                f"{self.base_url}/tts/status/{job_id}",
                headers=headers
            )
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(
                "tts_status_check_failed",
                job_id=job_id,
                error=str(e),
                session_id=session_id
            )
            raise
    
    async def download_audio(
        self,
        job_id: str,
        session_id: Optional[str] = None
    ) -> Tuple[bytes, str]:
        """
        Download the generated audio file.
        
        Args:
            job_id: The job identifier
            session_id: Optional session identifier
            
        Returns:
            Tuple of (audio_bytes, format)
        """
        try:
            headers = {
                "X-API-Key": self.api_key,
            }
            
            response = await self.client.get(
                f"{self.base_url}/v1/audio/{job_id}",
                headers=headers
            )
            response.raise_for_status()
            
            # Determine format from content-type or default to mp3
            content_type = response.headers.get("content-type", "audio/mpeg")
            audio_format = "wav" if "wav" in content_type else "mp3"
            
            logger.info(
                "tts_audio_downloaded",
                job_id=job_id,
                format=audio_format,
                size=len(response.content),
                session_id=session_id
            )
            
            return response.content, audio_format
        
        except Exception as e:
            logger.error(
                "tts_audio_download_failed",
                job_id=job_id,
                error=str(e),
                session_id=session_id
            )
            raise
    
    async def generate_and_wait(
        self,
        text: str,
        voice: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Tuple[bytes, str]:
        """
        Complete TTS workflow: create job, poll until complete, download audio.
        
        Args:
            text: Text to convert to speech
            voice: Voice name (optional)
            session_id: Optional session identifier
            
        Returns:
            Tuple of (audio_bytes, format)
        """
        # Step 1: Create TTS job
        job_id = await self.create_tts_job(text, voice, session_id)
        
        # Step 2: Poll for completion
        for attempt in range(self.max_polls):
            await asyncio.sleep(self.poll_interval)
            
            status_data = await self.check_job_status(job_id, session_id)
            status = status_data.get("status")
            
            if status == "completed":
                # Step 3: Download audio
                audio_bytes, audio_format = await self.download_audio(job_id, session_id)
                return audio_bytes, audio_format
            
            elif status == "failed":
                error_msg = status_data.get("error", "TTS job failed")
                logger.error(
                    "tts_job_failed",
                    job_id=job_id,
                    error=error_msg,
                    session_id=session_id
                )
                raise Exception(f"TTS job failed: {error_msg}")
            
            else:
                logger.debug(
                    "tts_job_pending",
                    job_id=job_id,
                    status=status,
                    attempt=attempt + 1,
                    session_id=session_id
                )
        
        # If we get here, we've exceeded max polls
        logger.error(
            "tts_job_timeout",
            job_id=job_id,
            max_polls=self.max_polls,
            session_id=session_id
        )
        raise TimeoutError(f"TTS generation timed out after {self.max_polls} attempts")
    
    async def list_voices(self) -> list:
        """List available voices from CodeVoice API."""
        try:
            headers = {
                "X-API-Key": self.api_key,
            }
            
            response = await self.client.get(
                f"{self.base_url}/v1/voices",
                headers=headers
            )
            response.raise_for_status()
            
            voices_data = response.json()
            logger.info("voices_listed", count=len(voices_data))
            
            return voices_data
        
        except Exception as e:
            logger.error("voices_list_failed", error=str(e))
            raise
    
    async def test_connection(self) -> bool:
        """Test the connection to CodeVoice API."""
        try:
            voices = await self.list_voices()
            return len(voices) > 0
        except Exception as e:
            logger.error("codevoice_connection_test_failed", error=str(e))
            return False


# Global TTS service instance
tts_service = CodeVoiceTTSService()
