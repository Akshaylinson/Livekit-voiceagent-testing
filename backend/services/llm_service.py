import httpx
import structlog
from typing import AsyncGenerator, List, Optional
from backend.config import settings

logger = structlog.get_logger()


class GeminiLLMService:
    """Gemini LLM service with streaming support."""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
        self.max_tokens = settings.GEMINI_MAX_TOKENS
        self.temperature = settings.GEMINI_TEMPERATURE
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def close(self):
        """Close the HTTP client."""
        if self.client:
            await self.client.aclose()
    
    async def generate_stream(
        self,
        messages: List[dict],
        session_id: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming response from Gemini.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            session_id: Optional session identifier for logging
            
        Yields:
            Chunks of text from the LLM response
        """
        try:
            # Convert messages to Gemini format
            gemini_contents = self._convert_messages_to_gemini(messages)
            
            url = f"{self.base_url}/models/{self.model}:streamGenerateContent"
            
            payload = {
                "contents": gemini_contents,
                "generationConfig": {
                    "temperature": self.temperature,
                    "maxOutputTokens": self.max_tokens,
                }
            }
            
            params = {"key": self.api_key}
            
            logger.info(
                "llm_request_started",
                session_id=session_id,
                model=self.model,
                message_count=len(messages)
            )
            
            async with self.client.stream(
                "POST",
                url,
                json=payload,
                params=params,
                timeout=60.0
            ) as response:
                if response.status_code != 200:
                    error_body = await response.aread()
                    logger.error(
                        "llm_request_failed",
                        status_code=response.status_code,
                        error=error_body.decode()
                    )
                    raise Exception(f"Gemini API error: {response.status_code}")
                
                # Process streaming response
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    
                    # Parse the JSON response
                    try:
                        import json
                        # Gemini streaming response format
                        data = json.loads(line)
                        
                        if "candidates" in data:
                            for candidate in data["candidates"]:
                                if "content" in candidate:
                                    for part in candidate["content"]["parts"]:
                                        if "text" in part:
                                            yield part["text"]
                    
                    except json.JSONDecodeError:
                        continue
            
            logger.info("llm_stream_completed", session_id=session_id)
        
        except Exception as e:
            logger.error("llm_generation_error", error=str(e), session_id=session_id)
            raise
    
    async def generate(
        self,
        messages: List[dict],
        session_id: Optional[str] = None
    ) -> str:
        """
        Generate a complete response (non-streaming).
        
        Args:
            messages: List of message dicts
            session_id: Optional session identifier
            
        Returns:
            Complete response text
        """
        full_response = ""
        async for chunk in self.generate_stream(messages, session_id):
            full_response += chunk
        
        return full_response
    
    def _convert_messages_to_gemini(self, messages: List[dict]) -> List[dict]:
        """
        Convert standard chat messages to Gemini format.
        
        Gemini expects:
        - role: 'user' or 'model' (not 'assistant')
        - parts: array with {'text': content}
        """
        gemini_contents = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            # Skip system messages (Gemini doesn't support system role directly)
            if role == "system":
                # We can prepend system prompt to first user message
                continue
            
            # Convert 'assistant' to 'model' for Gemini
            gemini_role = "model" if role == "assistant" else "user"
            
            gemini_contents.append({
                "role": gemini_role,
                "parts": [{"text": content}]
            })
        
        return gemini_contents
    
    async def test_connection(self) -> bool:
        """Test the connection to Gemini API."""
        try:
            url = f"{self.base_url}/models/{self.model}"
            params = {"key": self.api_key}
            
            response = await self.client.get(url, params=params)
            
            if response.status_code == 200:
                logger.info("gemini_connection_test_successful")
                return True
            else:
                logger.error(
                    "gemini_connection_test_failed",
                    status_code=response.status_code
                )
                return False
        
        except Exception as e:
            logger.error("gemini_connection_test_error", error=str(e))
            return False


# Global LLM service instance
llm_service = GeminiLLMService()
