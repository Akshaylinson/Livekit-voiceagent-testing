# API Reference Documentation

Complete API reference for the AI Voice Agent platform.

**Base URL:** `http://localhost:8000/api/v1`

---

## Authentication

Currently, the API does not require authentication for local development. For production, implement:
- API key authentication
- JWT tokens
- OAuth 2.0

---

## Endpoints

### 1. Session Management

#### 1.1 Create Session

Create a new conversation session and LiveKit room.

**Endpoint:** `POST /api/v1/session`

**Request Body:**
```json
{
  "session_id": "optional-custom-uuid",
  "system_prompt": "You are a helpful assistant specializing in customer support."
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | No | Custom session ID (auto-generated if omitted) |
| system_prompt | string | No | Custom system prompt for the AI |

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room_name": "voice-session-550e8400",
  "status": "active"
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| session_id | string | Unique session identifier |
| token | string | LiveKit JWT access token |
| room_name | string | LiveKit room name |
| status | string | Session status (active/inactive) |

**Example (cURL):**
```bash
curl -X POST http://localhost:8000/api/v1/session \
  -H "Content-Type: application/json" \
  -d '{"system_prompt": "You are a friendly voice assistant"}'
```

---

#### 1.2 Get Session

Retrieve session information and status.

**Endpoint:** `GET /api/v1/session/{session_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | Yes | Session identifier |

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-01T00:00:00",
  "last_activity": "2024-01-01T00:05:00",
  "message_count": 10,
  "is_active": true
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Session not found"
}
```

---

#### 1.3 Delete Session

Delete a session and clean up resources.

**Endpoint:** `DELETE /api/v1/session/{session_id}`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | Yes | Session identifier |

**Response (200 OK):**
```json
{
  "status": "deleted",
  "session_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 2. Conversation

#### 2.1 Process Conversation

Send STT transcript and receive AI response.

**Endpoint:** `POST /api/v1/conversation`

**Request Body:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "transcript": "What is the weather today?",
  "is_final": true,
  "is_interim": false
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | Yes | Session identifier |
| transcript | string | Yes | Speech-to-text transcript |
| is_final | boolean | No | Whether this is a final transcript (default: false) |
| is_interim | boolean | No | Whether this is an interim transcript (default: false) |

**Response (200 OK):**
```json
{
  "status": "success",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_transcript": "What is the weather today?",
  "assistant_response": "I don't have access to real-time weather data, but I can help you find weather information online."
}
```

**Interim Response (200 OK):**
```json
{
  "status": "interim",
  "transcript": "What is the..."
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "detail": "Failed to process conversation: Empty LLM response"
}
```

---

#### 2.2 Get Conversation History

Retrieve full conversation history for a session.

**Endpoint:** `GET /api/v1/conversation/{session_id}/history`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | Yes | Session identifier |

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "messages": [
    {
      "role": "user",
      "content": "Hello, how are you?",
      "timestamp": "2024-01-01T00:00:00"
    },
    {
      "role": "assistant",
      "content": "I'm doing well, thank you! How can I help you today?",
      "timestamp": "2024-01-01T00:00:05"
    }
  ],
  "count": 2
}
```

---

### 3. Text-to-Speech

#### 3.1 Generate TTS

Create a TTS job to convert text to speech.

**Endpoint:** `POST /api/v1/tts`

**Request Body:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "Hello, how can I help you today?",
  "voice": "Ryan"
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | Yes | Session identifier |
| text | string | Yes | Text to convert to speech |
| voice | string | No | Voice name (uses default if omitted) |

**Response (200 OK):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "job_id": "tts-job-12345",
  "status": "processing"
}
```

---

#### 3.2 Check TTS Status

Check the status of a TTS job.

**Endpoint:** `GET /api/v1/tts/{job_id}/status`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | TTS job identifier |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | No | Session identifier (for logging) |

**Response (200 OK) - Processing:**
```json
{
  "job_id": "tts-job-12345",
  "status": "processing",
  "progress": 50
}
```

**Response (200 OK) - Completed:**
```json
{
  "job_id": "tts-job-12345",
  "status": "completed",
  "audio_format": "mp3"
}
```

**Response (200 OK) - Failed:**
```json
{
  "job_id": "tts-job-12345",
  "status": "failed",
  "error": "Invalid voice name"
}
```

---

#### 3.3 Download TTS Audio

Download the generated TTS audio file.

**Endpoint:** `GET /api/v1/tts/{job_id}/audio`

**Path Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| job_id | string | Yes | TTS job identifier |

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | No | Session identifier (for logging) |

**Response (200 OK):**
- Content-Type: `audio/mpeg` (MP3) or `audio/wav` (WAV)
- Binary audio data

**Headers:**
```
Content-Disposition: attachment; filename=tts-tts-job-12345.mp3
Content-Type: audio/mpeg
```

**Error Response (500):**
```json
{
  "detail": "Failed to download TTS audio: Job not found"
}
```

---

### 4. LiveKit Token

#### 4.1 Generate Token

Generate a LiveKit access token for a participant.

**Endpoint:** `POST /api/v1/token`

**Request Body:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "participant_name": "John Doe"
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| session_id | string | Yes | Session identifier |
| participant_name | string | No | Display name (default: "User") |

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room_name": "voice-session-550e8400",
  "livekit_url": "ws://localhost:7880"
}
```

---

### 5. Utility Endpoints

#### 5.1 Health Check

Check if the backend service is healthy.

**Endpoint:** `GET /health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

---

#### 5.2 API Status

Get status of all backend services.

**Endpoint:** `GET /api/status`

**Response (200 OK):**
```json
{
  "api": "operational",
  "services": {
    "livekit": "operational",
    "llm": "operational",
    "tts": "degraded"
  }
}
```

**Service Status Values:**
- `operational`: Service is working normally
- `degraded`: Service is working with issues
- `down`: Service is not accessible

---

#### 5.3 List Voices

List available TTS voices from CodeVoice.

**Endpoint:** `GET /api/v1/voices`

**Response (200 OK):**
```json
{
  "voices": [
    {
      "name": "Ryan",
      "language": "en-US",
      "gender": "male"
    },
    {
      "name": "Emma",
      "language": "en-GB",
      "gender": "female"
    }
  ]
}
```

---

## Error Responses

### Standard Error Format

All error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Invalid request body or parameters |
| 404 | Not Found | Session or resource not found |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | External service (LLM/TTS) down |

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider:
- 100 requests/minute per session
- 10 concurrent TTS jobs per session
- 1000 messages per session per hour

---

## WebSocket Support (Future)

Future versions will support WebSocket for:
- Real-time transcript streaming
- Live LLM response streaming
- Real-time audio streaming
- Bidirectional communication

---

## SDK Examples

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Create session
response = requests.post(f"{BASE_URL}/session", json={
    "system_prompt": "You are a helpful assistant"
})
session_data = response.json()
session_id = session_data["session_id"]

# Process conversation
response = requests.post(f"{BASE_URL}/conversation", json={
    "session_id": session_id,
    "transcript": "Hello, how are you?",
    "is_final": True
})
conversation_data = response.json()
print(conversation_data["assistant_response"])

# Generate TTS
response = requests.post(f"{BASE_URL}/tts", json={
    "session_id": session_id,
    "text": conversation_data["assistant_response"]
})
tts_data = response.json()
job_id = tts_data["job_id"]

# Wait and download audio
import time
while True:
    status_response = requests.get(f"{BASE_URL}/tts/{job_id}/status")
    if status_response.json()["status"] == "completed":
        audio_response = requests.get(f"{BASE_URL}/tts/{job_id}/audio")
        with open("response.mp3", "wb") as f:
            f.write(audio_response.content)
        break
    time.sleep(2)
```

### JavaScript Example

```javascript
const BASE_URL = 'http://localhost:8000/api/v1';

// Create session
const sessionResponse = await fetch(`${BASE_URL}/session`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    system_prompt: 'You are a helpful assistant'
  })
});
const sessionData = await sessionResponse.json();
const sessionId = sessionData.session_id;

// Process conversation
const conversationResponse = await fetch(`${BASE_URL}/conversation`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: sessionId,
    transcript: 'Hello, how are you?',
    is_final: true
  })
});
const conversationData = await conversationResponse.json();
console.log(conversationData.assistant_response);
```

---

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

These interfaces allow you to:
- Browse all endpoints
- View request/response schemas
- Test endpoints directly
- Download OpenAPI specification

---

## OpenAPI Specification

Download the complete OpenAPI spec:

```
GET /openapi.json
```

This can be used with:
- API gateways
- Code generation tools
- Testing frameworks
- Documentation generators
