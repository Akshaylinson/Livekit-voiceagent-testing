from typing import Dict, List, Optional
from datetime import datetime, timedelta
import structlog
from backend.config import settings

logger = structlog.get_logger()


class ConversationMessage:
    """Represents a single message in the conversation."""
    
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.role = role  # 'user' or 'assistant'
        self.content = content
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }


class SessionManager:
    """Manages conversation sessions and memory."""
    
    def __init__(self):
        self.sessions: Dict[str, List[ConversationMessage]] = {}
        self.session_metadata: Dict[str, dict] = {}
        self.max_history = settings.MAX_CONVERSATION_HISTORY
    
    def create_session(self, session_id: str, system_prompt: Optional[str] = None):
        """Create a new conversation session."""
        self.sessions[session_id] = []
        self.session_metadata[session_id] = {
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "message_count": 0,
            "system_prompt": system_prompt or "You are a helpful AI voice assistant. Respond conversationally and naturally."
        }
        logger.info("session_created", session_id=session_id)
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to the conversation history."""
        if session_id not in self.sessions:
            self.create_session(session_id)
        
        message = ConversationMessage(role, content)
        self.sessions[session_id].append(message)
        self.session_metadata[session_id]["last_activity"] = datetime.utcnow()
        self.session_metadata[session_id]["message_count"] += 1
        
        # Trim history if it exceeds max
        if len(self.sessions[session_id]) > self.max_history:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history:]
        
        logger.debug("message_added", session_id=session_id, role=role)
    
    def get_conversation_history(self, session_id: str) -> List[dict]:
        """Get the conversation history for a session."""
        if session_id not in self.sessions:
            return []
        
        return [msg.to_dict() for msg in self.sessions[session_id]]
    
    def get_messages_for_llm(self, session_id: str) -> List[dict]:
        """Get formatted messages for LLM API consumption."""
        if session_id not in self.sessions:
            return []
        
        messages = []
        system_prompt = self.session_metadata[session_id].get("system_prompt")
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.extend([msg.to_dict() for msg in self.sessions[session_id]])
        
        return messages
    
    def clear_session(self, session_id: str):
        """Clear a conversation session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.session_metadata:
            del self.session_metadata[session_id]
        logger.info("session_cleared", session_id=session_id)
    
    def cleanup_expired_sessions(self):
        """Remove sessions that have exceeded the timeout."""
        current_time = datetime.utcnow()
        expired_sessions = []
        
        for session_id, metadata in self.session_metadata.items():
            last_activity = metadata["last_activity"]
            if current_time - last_activity > timedelta(seconds=settings.SESSION_TIMEOUT):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.clear_session(session_id)
        
        if expired_sessions:
            logger.info("expired_sessions_cleaned", count=len(expired_sessions))
    
    def get_session_status(self, session_id: str) -> Optional[dict]:
        """Get status information for a session."""
        if session_id not in self.session_metadata:
            return None
        
        metadata = self.session_metadata[session_id]
        return {
            "session_id": session_id,
            "created_at": metadata["created_at"].isoformat(),
            "last_activity": metadata["last_activity"].isoformat(),
            "message_count": metadata["message_count"],
            "is_active": True
        }


# Global session manager instance
session_manager = SessionManager()
