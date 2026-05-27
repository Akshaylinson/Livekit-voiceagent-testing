# Architecture Documentation

## System Overview

The AI Voice Agent platform is a modular, scalable realtime conversational system built on LiveKit infrastructure. This document provides detailed architecture information for developers and system architects.

---

## High-Level Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                               │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │  React SPA (Vite + Tailwind CSS)                         │       │
│  │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────┐  │       │
│  │  │ Web Speech  │ │  Waveform    │ │  LiveKit Client  │  │       │
│  │  │ API (STT)   │ │  Visualizer  │ │  SDK (WebRTC)    │  │       │
│  │  └─────────────┘ └──────────────┘ └──────────────────┘  │       │
│  └──────────────────────────────────────────────────────────┘       │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                    REST API / WebSockets
                              │
┌─────────────────────────────▼───────────────────────────────────────┐
│                        APPLICATION LAYER                            │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │  FastAPI Backend (Python 3.11)                           │       │
│  │                                                          │       │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │       │
│  │  │ API Routes   │  │  Session     │  │  Audio        │  │       │
│  │  │ (REST)       │  │  Manager     │  │  Orchestrator │  │       │
│  │  └──────────────┘  └──────────────┘  └───────────────┘  │       │
│  │                                                          │       │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │       │
│  │  │ LLM Service  │  │  TTS Service │  │  LiveKit      │  │       │
│  │  │ (Gemini)     │  │  (CodeVoice) │  │  Service      │  │       │
│  │  └──────────────┘  └──────────────┘  └───────────────┘  │       │
│  └──────────────────────────────────────────────────────────┘       │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                    API Calls (HTTPS)
                              │
┌─────────────────────────────▼───────────────────────────────────────┐
│                       INFRASTRUCTURE LAYER                          │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │  LiveKit     │  │  Gemini API  │  │  CodeVoice TTS Platform  │  │
│  │  Server      │  │  (Google)    │  │  (voices.codelessai.in)  │  │
│  │  (WebRTC)    │  │              │  │                          │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Service Architecture

### 1. Frontend Service (React + Vite)

**Technology Stack:**
- React 18
- Vite 6
- Tailwind CSS
- LiveKit Client SDK
- Web Speech API (Browser-native)

**Responsibilities:**
- User interface and interaction
- Browser speech recognition (STT)
- Audio waveform visualization
- LiveKit WebRTC connection
- Transcript display
- Conversation history rendering
- Dark mode theming

**Key Components:**
- `VoiceAgent.jsx`: Main orchestrator component
- `WaveformVisualizer.jsx`: Canvas-based audio visualization
- `TranscriptDisplay.jsx`: Real-time transcript rendering
- `ConversationHistory.jsx`: Message history with auto-scroll

**Speech Recognition Flow:**
```
User speaks 
  → Microphone captures audio
  → Web Speech API processes
  → Interim transcripts (real-time)
  → Final transcript detected
  → Sent to backend API
  → Processed by LLM
  → Response received
  → TTS requested
  → Audio played
  → Resume listening
```

---

### 2. Backend Service (FastAPI)

**Technology Stack:**
- Python 3.11
- FastAPI
- Uvicorn (ASGI server)
- httpx (async HTTP client)
- structlog (structured logging)
- LiveKit Python SDK

**Service Modules:**

#### A. API Routes (`backend/api/routes.py`)

**Endpoints:**
- Session management (CRUD)
- Conversation processing
- TTS generation and retrieval
- LiveKit token generation
- Health checks and status

**Design Pattern:**
- RESTful API design
- Request/response validation with Pydantic
- Async route handlers
- Background task support

#### B. Session Manager (`backend/services/session_manager.py`)

**Responsibilities:**
- Session lifecycle management
- Conversation history storage
- Message trimming and pagination
- Session timeout handling
- Context management for LLM

**Data Structures:**
```python
Session {
    session_id: str
    created_at: datetime
    last_activity: datetime
    message_count: int
    system_prompt: str
    messages: List[ConversationMessage]
}

ConversationMessage {
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
}
```

**Memory Management:**
- In-memory storage (can be replaced with Redis/PostgreSQL)
- Automatic session cleanup (every 5 minutes)
- Configurable max history (default: 50 messages)
- Configurable session timeout (default: 30 minutes)

#### C. LLM Service (`backend/services/llm_service.py`)

**Current Provider:** Google Gemini

**Features:**
- Streaming response support
- Message format conversion
- Async HTTP requests
- Error handling and retries
- Connection testing

**Streaming Implementation:**
```python
async def generate_stream(messages):
    async with client.stream("POST", url, json=payload) as response:
        async for line in response.aiter_lines():
            data = json.loads(line)
            yield text_chunk
```

**Provider Abstraction:**
The LLM service is designed to be provider-agnostic. To switch providers:
1. Create new service class (e.g., `GrokLLMService`)
2. Implement same interface methods
3. Update factory/initialization

#### D. TTS Service (`backend/services/tts_service.py`)

**Current Provider:** CodeVoice (Internal Platform)

**Architecture:**
Asynchronous job-based system:
1. Create TTS job → receive job_id
2. Poll status endpoint until completion
3. Download audio file
4. Stream to client

**Polling Strategy:**
```python
for attempt in range(max_polls):
    await asyncio.sleep(poll_interval)
    status = check_job_status(job_id)
    
    if status == "completed":
        return download_audio(job_id)
    elif status == "failed":
        raise Exception
```

**Provider Abstraction:**
TTS adapter pattern allows easy switching:
- ElevenLabs
- Sarvam AI
- Piper
- VibeVoice
- Local TTS models

#### E. LiveKit Service (`backend/services/livekit_service.py`)

**Responsibilities:**
- Room creation and management
- JWT token generation
- Participant management
- Track publishing control

**Token Generation:**
```python
token = AccessToken(api_key, api_secret) \
    .with_identity(participant_id) \
    .with_name(participant_name) \
    .with_grants(VideoGrants(
        room_join=True,
        room=room_name,
        can_publish=True,
        can_subscribe=True
    )) \
    .to_jwt()
```

---

## Data Flow Architecture

### Complete Conversation Flow

```
1. INITIALIZATION
   Frontend → POST /api/v1/session → Backend
   Backend → Create LiveKit Room → LiveKit Server
   Backend → Generate JWT Token
   Backend → Return {session_id, token, room_name}
   Frontend → Connect to LiveKit Room with Token

2. VOICE INPUT
   User speaks → Microphone
   Browser → Web Speech API → Interim Transcripts
   Browser → Web Speech API → Final Transcript
   Frontend → POST /api/v1/conversation → Backend

3. LLM PROCESSING
   Backend → Get conversation history → Session Manager
   Backend → Format messages for LLM
   Backend → Stream request → Gemini API
   Gemini → Stream response chunks → Backend
   Backend → Accumulate full response

4. TTS GENERATION
   Backend → POST /v1/tts → CodeVoice API
   CodeVoice → Return job_id
   Backend → Poll /tts/status/{job_id} (every 2s)
   CodeVoice → Status: "completed"
   Backend → GET /v1/audio/{job_id} → CodeVoice
   CodeVoice → Return audio bytes (MP3/WAV)

5. AUDIO OUTPUT
   Backend → Audio URL → Frontend
   Frontend → Play audio → Audio API
   User hears AI response

6. CONTINUATION
   After audio ends → Resume listening
   Continuous mode → Auto-restart STT
   Push-to-talk mode → Wait for button press
```

---

## Concurrency Model

### Async Architecture

**Backend:**
- Fully async using asyncio
- Async HTTP clients (httpx)
- Non-blocking I/O operations
- Concurrent request handling

**Frontend:**
- Async/await for API calls
- Non-blocking UI updates
- Web Audio API for visualization
- Event-driven STT handling

### Threading Considerations

**Current Design:**
- Single-threaded async event loop
- No explicit thread management
- Suitable for I/O-bound workloads

**Future Scaling:**
- Use Celery for background TTS jobs
- Implement Redis task queue
- Add worker processes for CPU-bound tasks

---

## State Management

### Frontend State

**React State (useState):**
- Session ID
- Listening status
- Transcripts (interim/final)
- Conversation history
- UI state (dark mode, etc.)

**Refs (useRef):**
- Speech recognition instance
- Audio context
- Animation frames
- Audio elements

### Backend State

**In-Memory Storage:**
- Session data (dict)
- Conversation history (list)
- Session metadata (dict)

**Future Persistence:**
```
Session Store: Redis/PostgreSQL
Message Store: PostgreSQL
Cache: Redis
File Storage: S3/MinIO (for TTS audio)
```

---

## Error Handling Strategy

### Backend Error Handling

**Global Exception Handler:**
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error("unhandled_exception", error=str(exc))
    return JSONResponse(status_code=500, content={...})
```

**Service-Level Errors:**
- Try-except blocks in service methods
- Structured logging with context
- Custom exception classes (future)
- Retry mechanisms for external APIs

### Frontend Error Handling

**API Call Errors:**
```javascript
try {
  const response = await axios.post(url, data)
} catch (error) {
  console.error('Failed:', error)
  setStatus('error')
}
```

**STT Errors:**
- Permission denied handling
- No speech detection auto-restart
- Network error recovery

---

## Security Architecture

### Current Security Measures

1. **Environment Variables:**
   - API keys in `.env` (not committed)
   - Docker secrets support

2. **CORS Configuration:**
   - Configurable allowed origins
   - Credentials support

3. **JWT Tokens:**
   - LiveKit access tokens with TTL
   - Scoped permissions

4. **Input Validation:**
   - Pydantic models for request validation
   - Type safety throughout

### Recommended Production Enhancements

1. **Authentication:**
   - User login system
   - OAuth/SAML integration
   - API key management

2. **Rate Limiting:**
   - Per-user rate limits
   - Per-IP rate limits
   - Token bucket algorithm

3. **HTTPS:**
   - TLS termination (nginx/LiveKit)
   - Certificate management (Let's Encrypt)

4. **Input Sanitization:**
   - XSS protection
   - SQL injection prevention
   - Prompt injection mitigation

---

## Performance Considerations

### Latency Optimization

**Current Performance Targets:**
- STT recognition: < 500ms
- LLM response: 1-3s (streaming)
- TTS generation: 2-10s (async)
- Total round-trip: 3-15s

**Optimization Strategies:**
1. **Streaming:** LLM and TTS stream responses
2. **Async I/O:** Non-blocking operations
3. **Connection pooling:** HTTP client reuse
4. **Caching:** Frequent responses (future)

### Resource Management

**Memory:**
- Conversation history trimming
- Session cleanup
- Audio buffer management

**CPU:**
- Offload TTS to external service
- LLM API-based (no local compute)
- Frontend canvas optimization

---

## Scalability Roadmap

### Phase 1: Current (Single Instance)
- In-memory session storage
- Single backend instance
- Direct API calls

### Phase 2: Horizontal Scaling
- Redis session store
- Load balancer
- Multiple backend instances
- Database persistence

### Phase 3: Microservices
```
┌──────────────┐
│  API Gateway │
└──────┬───────┘
       │
   ┌───┴───┬───────────┬──────────┐
   │       │           │          │
┌──────┐┌──────┐┌─────────┐┌──────┐
│Session││ LLM  ││   TTS   ││LiveKit│
│Service││Service││ Service ││Service│
└──────┘└──────┘└─────────┘└──────┘
```

### Phase 4: Multi-Tenant SaaS
- Tenant isolation
- Custom domains
- Billing integration
- Analytics dashboard

---

## Monitoring & Observability

### Logging

**Structured Logging (structlog):**
```json
{
  "event": "conversation_processed",
  "session_id": "uuid",
  "level": "info",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

**Log Levels:**
- DEBUG: Detailed debugging
- INFO: General operational info
- WARNING: Warning conditions
- ERROR: Error conditions

### Metrics (Future)

**Key Metrics to Track:**
- Request latency (p50, p95, p99)
- Error rates
- Active sessions
- API response times
- TTS job completion times
- LLM token usage

### Health Checks

**Docker Health Checks:**
- Backend: `/health` endpoint
- Frontend: HTTP check
- LiveKit: WebSocket check
- Redis: PING command

---

## Deployment Architecture

### Development Environment
```
Developer Machine
├── Docker Compose
│   ├── LiveKit Server
│   ├── Redis
│   ├── Backend (hot reload)
│   └── Frontend (HMR)
```

### Staging Environment
```
Cloud VM / Kubernetes
├── LiveKit (self-hosted)
├── Redis
├── Backend (2+ replicas)
└── Frontend (CDN)
```

### Production Environment
```
Kubernetes Cluster
├── Ingress Controller
├── LiveKit Cloud / Self-hosted
├── Redis Cluster
├── Backend (auto-scaling)
├── Frontend (CDN)
├── PostgreSQL
└── Monitoring Stack
    ├── Prometheus
    ├── Grafana
    └── ELK Stack
```

---

## Technology Decisions

### Why FastAPI?
- Async-first design
- Automatic API documentation
- Type safety with Pydantic
- High performance
- Easy to learn

### Why React + Vite?
- Component-based architecture
- Fast hot module replacement
- Large ecosystem
- Good TypeScript support

### Why LiveKit?
- Production-ready WebRTC
- Excellent SDKs
- Scalable architecture
- Active development
- SIP support (future)

### Why Web Speech API?
- Zero cost
- Browser-native
- No external dependencies
- Good accuracy
- Can be replaced later

---

## Future Integration Points

### SIP/Telephony
- LiveKit SIP URI support
- Twilio integration
- PSTN connectivity
- IVR systems

### CRM Integration
- Salesforce
- HubSpot
- Custom webhooks
- Contact management

### Analytics
- Conversation analytics
- Sentiment analysis
- User behavior tracking
- Performance dashboards

### Voice Enhancements
- Emotional voice modulation
- Voice cloning
- Multi-language support
- Custom voice training

---

**This architecture is designed for evolution, not revolution. Each component can be upgraded independently without affecting the entire system.**
