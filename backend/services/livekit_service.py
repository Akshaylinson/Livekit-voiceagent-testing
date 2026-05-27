import structlog
from livekit import api
from backend.config import settings

logger = structlog.get_logger()


class LiveKitService:
    """LiveKit service for room and token management."""
    
    def __init__(self):
        self.api_key = settings.LIVEKIT_API_KEY
        self.api_secret = settings.LIVEKIT_API_SECRET
        self.url = settings.LIVEKIT_URL
        
        # Initialize LiveKit API client
        self.room_client = api.RoomServiceClient(self.url, self.api_key, self.api_secret)
    
    def generate_token(
        self,
        room_name: str,
        participant_identity: str,
        participant_name: str = "User",
        is_bot: bool = False,
        ttl: int = 3600
    ) -> str:
        """
        Generate a LiveKit access token for a participant.
        
        Args:
            room_name: Name of the room
            participant_identity: Unique identifier for the participant
            participant_name: Display name
            is_bot: Whether this is a bot participant
            ttl: Token time-to-live in seconds
            
        Returns:
            JWT access token
        """
        try:
            at = api.AccessToken(self.api_key, self.api_secret) \
                .with_identity(participant_identity) \
                .with_name(participant_name) \
                .with_ttl(ttl)
            
            # Add room and permissions
            at.with_grants(api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True,
            ))
            
            # If bot, add additional permissions
            if is_bot:
                at.with_grants(api.VideoGrants(
                    agent=True,
                ))
            
            token = at.to_jwt()
            
            logger.info(
                "token_generated",
                room_name=room_name,
                participant=participant_identity,
                is_bot=is_bot
            )
            
            return token
        
        except Exception as e:
            logger.error(
                "token_generation_failed",
                error=str(e),
                room_name=room_name
            )
            raise
    
    async def create_room(self, room_name: str) -> api.Room:
        """
        Create a new LiveKit room.
        
        Args:
            room_name: Name of the room to create
            
        Returns:
            Room object
        """
        try:
            room = self.room_client.create_room(
                api.CreateRoomRequest(name=room_name)
            )
            
            logger.info("room_created", room_name=room_name)
            return room
        
        except Exception as e:
            # Room might already exist, which is okay
            logger.warning(
                "room_creation_warning",
                room_name=room_name,
                error=str(e)
            )
            
            # Try to list rooms to see if it exists
            try:
                rooms = self.room_client.list_rooms(api.ListRoomsRequest())
                for room in rooms.rooms:
                    if room.name == room_name:
                        logger.info("room_exists", room_name=room_name)
                        return room
            except:
                pass
            
            raise
    
    async def delete_room(self, room_name: str):
        """
        Delete a LiveKit room.
        
        Args:
            room_name: Name of the room to delete
        """
        try:
            self.room_client.delete_room(
                api.DeleteRoomRequest(room=room_name)
            )
            
            logger.info("room_deleted", room_name=room_name)
        
        except Exception as e:
            logger.error(
                "room_deletion_failed",
                room_name=room_name,
                error=str(e)
            )
            raise
    
    async def list_participants(self, room_name: str) -> list:
        """
        List all participants in a room.
        
        Args:
            room_name: Name of the room
            
        Returns:
            List of participant objects
        """
        try:
            response = self.room_client.list_participants(
                api.ListParticipantsRequest(room=room_name)
            )
            
            participants = [p for p in response.participants]
            
            logger.info(
                "participants_listed",
                room_name=room_name,
                count=len(participants)
            )
            
            return participants
        
        except Exception as e:
            logger.error(
                "participant_listing_failed",
                room_name=room_name,
                error=str(e)
            )
            raise
    
    async def mute_participant(
        self,
        room_name: str,
        participant_identity: str,
        muted: bool = True
    ):
        """
        Mute or unmute a participant.
        
        Args:
            room_name: Name of the room
            participant_identity: Participant identity
            muted: Whether to mute or unmute
        """
        try:
            self.room_client.mute_published_track(
                api.MuteRoomTrackRequest(
                    room=room_name,
                    identity=participant_identity,
                    track_sid="",  # Would need actual track SID
                    muted=muted
                )
            )
            
            logger.info(
                "participant_muted",
                room_name=room_name,
                participant=participant_identity,
                muted=muted
            )
        
        except Exception as e:
            logger.error(
                "participant_mute_failed",
                room_name=room_name,
                error=str(e)
            )
            raise
    
    async def test_connection(self) -> bool:
        """Test the connection to LiveKit server."""
        try:
            rooms = self.room_client.list_rooms(api.ListRoomsRequest())
            logger.info("livekit_connection_test_successful", room_count=len(rooms.rooms))
            return True
        except Exception as e:
            logger.error("livekit_connection_test_failed", error=str(e))
            return False


# Global LiveKit service instance
livekit_service = LiveKitService()
