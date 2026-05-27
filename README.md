# AI Voice Agent Platform - Realtime Conversational Assistant

A production-ready realtime AI Voice Agent platform built with LiveKit, enabling natural browser-based voice conversations with AI. Users can speak naturally with the AI instead of typing prompts.

## 🎯 Features

### Core Capabilities
- **Realtime Voice Communication**: Powered by LiveKit WebRTC infrastructure
- **Browser-Based STT**: Web Speech API for continuous speech recognition
- **LLM Integration**: Gemini API with streaming responses
- **CodeVoice TTS**: High-quality text-to-speech synthesis
- **Natural Conversation Flow**: Supports interruptions, barge-in, and simultaneous listening/speaking
- **Live Transcript Display**: Real-time interim and final transcript visualization
- **Conversation Memory**: Session-based context management

### UI/UX Features
- Modern, minimal design with Tailwind CSS
- Realtime waveform visualization
- Push-to-talk and continuous listening modes
- AI speaking indicators
- Conversation history panel
- Dark mode support
- Responsive design

### Architecture Features
- Fully Dockerized setup
- Modular service-oriented design
- Async-first Python backend (FastAPI)
- React/Vite frontend
- Production-ready organization
- Future-ready for SIP/telephony integration

---

## 📁 Project Structure

```
Livekit-voice agent-testing1/
├── backend/                      # Python FastAPI backend
│   ├── api/                      # API routes
│   │   ├── __init__.py
│   │   └── routes.py             # REST API endpoints
│   ├── config/                   # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py           # Environment-based settings
│   ├── services/                 # Core business logic
│   │   ├── __init__.py
│   │   ├── livekit_service.py    # LiveKit room & token management
│   │   ├── llm_service.py        # Gemini LLM integration
│   │   ├── session_manager.py    # Conversation session & memory
│   │   └── tts_service.py        # CodeVoice TTS integration
│   ├── utils/                    # Utilities
│   │   ├── __init__.py
│   │   └── logging.py            # Structured logging setup
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   └── requirements.txt          # Python dependencies
│
├── frontend/                     # React/Vite frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── ConversationHistory.jsx
│   │   │   ├── Icons.jsx
│   │   │   ├── StatusIndicator.jsx
│   │   │   ├── ThemeToggle.jsx
│   │   │   ├── TranscriptDisplay.jsx
│   │   │   ├── VoiceAgent.jsx    # Main voice agent component
│   │   │   ├── WaveformVisualizer.jsx
│   │   │   └── index.js
│   │   ├── App.jsx               # Main application component
│   │   ├── index.css             # Global styles & Tailwind
│   │   └── main.jsx              # React entry point
│   ├── index.html
│   ├── nginx.conf                # Nginx configuration for production
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── docker-compose.yml            # Docker orchestration
├── Dockerfile.backend            # Backend container
├── Dockerfile.frontend           # Frontend container
├── livekit-config.yaml           # LiveKit server configuration
├── .env.example                  # Environment variables template
├── .gitignore
└── README.md                     # This file
```

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      User Browser                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React Frontend (Vite)                               │   │
│  │  ┌────────────┐  ┌──────────┐  ┌─────────────────┐  │   │
│  │  │  Web Speech│  │Waveform  │  │  LiveKit Client │  │   │
│  │  │  API (STT) │  │Visualizer│  │  (WebRTC)       │  │   │
│  │  └────────────┘  └──────────┘  └─────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
              WebSockets / HTTP API
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                     Backend Services                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  FastAPI (Python)                                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐  │   │
│  │  │  Session │ │   LLM    │ │   TTS    │ │LiveKit │  │   │
│  │  │ Manager  │ │ Service  │ │ Service  │ │Service │  │   │
│  │  │          │ │ (Gemini) │ │(CodeVoice│ │        │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   External Services                         │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │  LiveKit     │  │  Gemini API │  │  CodeVoice TTS   │   │
│  │  Server      │  │  (LLM)      │  │  Platform        │   │
│  └──────────────┘  └─────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Service Interaction Flow

1. **Session Initialization**:
   - Frontend requests new session from Backend API
   - Backend creates LiveKit room and generates access token
   - Frontend connects to LiveKit room using token

2. **Voice Conversation Flow**:
   - User speaks → Browser STT (Web Speech API) captures audio
   - STT generates interim/final transcripts
   - Final transcript sent to Backend via REST API
   - Backend forwards to Gemini LLM with conversation context
   - LLM streams response back to Backend
   - Backend sends text to CodeVoice TTS
   - TTS generates audio file (async job polling)
   - Audio streamed back to frontend and played through LiveKit

3. **Realtime Behavior**:
   - Continuous listening mode with auto-restart
   - Interruption handling (barge-in support)
   - Simultaneous listening/speaking management
   - Low-latency streaming throughout the pipeline

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- LiveKit API credentials (or use included LiveKit server)
- Gemini API key
- CodeVoice API key
- Modern web browser with Web Speech API support (Chrome recommended)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Livekit-voice-agent-testing1
```

### Step 2: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# LiveKit Configuration
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=ws://localhost:7880

# LLM Configuration (Gemini)
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-pro
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.7

# CodeVoice TTS Configuration
CODEVOICE_API_KEY=your_codevoice_api_key
CODEVOICE_BASE_URL=https://voices.codelessai.in
CODEVOICE_VOICE=Ryan
CODEVOICE_POLL_INTERVAL=2
CODEVOICE_MAX_POLLS=60

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Step 3: Start with Docker Compose

```bash
docker compose up --build
```

This will start:
- LiveKit Server (port 7880)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)

### Step 4: Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

### Step 5: Grant Microphone Permission

When prompted, allow microphone access to start voice conversations.

---

## 🔧 Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API documentation available at: `http://localhost:8000/docs`

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

---

## 📡 API Documentation

### Session Management

#### Create Session
```http
POST /api/v1/session
Content-Type: application/json

{
  "session_id": "optional-custom-id",
  "system_prompt": "Custom system prompt (optional)"
}
```

Response:
```json
{
  "session_id": "uuid-here",
  "token": "livekit-jwt-token",
  "room_name": "voice-session-uuid",
  "status": "active"
}
```

#### Get Session Status
```http
GET /api/v1/session/{session_id}
```

#### Delete Session
```http
DELETE /api/v1/session/{session_id}
```

### Conversation

#### Process Transcript
```http
POST /api/v1/conversation
Content-Type: application/json

{
  "session_id": "uuid",
  "transcript": "What is the weather today?",
  "is_final": true
}
```

Response:
```json
{
  "status": "success",
  "session_id": "uuid",
  "user_transcript": "What is the weather today?",
  "assistant_response": "Let me check the weather for you..."
}
```

#### Get Conversation History
```http
GET /api/v1/conversation/{session_id}/history
```

### Text-to-Speech

#### Generate TTS
```http
POST /api/v1/tts
Content-Type: application/json

{
  "session_id": "uuid",
  "text": "Hello, how can I help you?",
  "voice": "Ryan"
}
```

Response:
```json
{
  "session_id": "uuid",
  "job_id": "tts-job-id",
  "status": "processing"
}
```

#### Check TTS Status
```http
GET /api/v1/tts/{job_id}/status
```

#### Download TTS Audio
```http
GET /api/v1/tts/{job_id}/audio
```

### LiveKit Token

#### Generate Token
```http
POST /api/v1/token
Content-Type: application/json

{
  "session_id": "uuid",
  "participant_name": "User"
}
```

### Utility Endpoints

#### Health Check
```http
GET /health
```

#### API Status
```http
GET /api/status
```

#### List Available Voices
```http
GET /api/v1/voices
```

---

## 🎛️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LIVEKIT_API_KEY` | LiveKit server API key | Required |
| `LIVEKIT_API_SECRET` | LiveKit server API secret | Required |
| `LIVEKIT_URL` | LiveKit WebSocket URL | `ws://localhost:7880` |
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `GEMINI_MODEL` | Gemini model to use | `gemini-pro` |
| `GEMINI_MAX_TOKENS` | Maximum response tokens | `2048` |
| `GEMINI_TEMPERATURE` | Response creativity (0-1) | `0.7` |
| `CODEVOICE_API_KEY` | CodeVoice TTS API key | Required |
| `CODEVOICE_BASE_URL` | CodeVoice API base URL | `https://voices.codelessai.in` |
| `CODEVOICE_VOICE` | Default voice name | `Ryan` |
| `CODEVOICE_POLL_INTERVAL` | TTS job poll interval (seconds) | `2` |
| `CODEVOICE_MAX_POLLS` | Maximum poll attempts | `60` |
| `BACKEND_HOST` | Backend bind address | `0.0.0.0` |
| `BACKEND_PORT` | Backend port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENVIRONMENT` | Environment name | `development` |
| `SESSION_TIMEOUT` | Session timeout (seconds) | `1800` |
| `MAX_CONVERSATION_HISTORY` | Max messages per session | `50` |

---

## 🔐 Security Considerations

- **API Keys**: Never commit `.env` files. Use secrets management in production.
- **CORS**: Configure `allow_origins` appropriately for production.
- **HTTPS**: Use HTTPS in production (configure in nginx/LiveKit).
- **Rate Limiting**: Implement rate limiting for production deployments.
- **Authentication**: Add user authentication for multi-tenant setups.

---

## 📊 Monitoring & Logging

### Structured Logging

The backend uses `structlog` for structured JSON logging in production:

```json
{
  "event": "conversation_processed",
  "session_id": "uuid",
  "user_text": "Hello",
  "response_length": 150,
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Health Checks

All services include Docker health checks:
- Backend: `/health` endpoint
- LiveKit: HTTP check on port 7880
- Redis: `redis-cli ping`
- Frontend: HTTP check on port 80

---

## 🚀 Deployment

### Production Deployment

1. **Set environment variables** with production values
2. **Configure HTTPS** in nginx and LiveKit
3. **Use external LiveKit** (LiveKit Cloud or self-hosted)
4. **Configure CORS** for your domain
5. **Set up monitoring** (Prometheus, Grafana, etc.)
6. **Enable HTTPS** for all external API calls

### Scaling Considerations

- **Horizontal Scaling**: Backend is stateless, can be scaled behind a load balancer
- **Session Management**: Move to Redis for distributed session storage
- **LiveKit**: Use LiveKit Cloud or scale self-hosted with Kubernetes
- **Database**: Add PostgreSQL for persistent conversation history
- **Caching**: Implement Redis caching for frequent TTS requests

---

## 🔮 Future Enhancements

### Planned Features

1. **AI Receptionist System**
   - Inbound calling support
   - Outbound calling capabilities
   - SIP trunk integration
   - Call routing and queuing

2. **Multi-Agent Architecture**
   - Agent specialization
   - Intelligent routing
   - Agent handoff protocols

3. **Voice Enhancements**
   - Emotional voice modulation
   - Voice cloning support
   - Multiple language support
   - Custom voice training

4. **Integration Capabilities**
   - CRM integration (Salesforce, HubSpot)
   - Calendar integration
   - Database connectivity
   - Webhook support

5. **Analytics & Monitoring**
   - Conversation analytics dashboard
   - Sentiment analysis
   - Performance metrics
   - User behavior tracking

6. **Multi-Tenant SaaS**
   - Tenant isolation
   - Custom branding
   - Billing integration
   - Usage quotas

---

## 🛠️ Troubleshooting

### Common Issues

**Microphone not working:**
- Ensure browser has microphone permissions
- Use HTTPS or localhost
- Try Chrome browser (best Web Speech API support)

**STT not recognizing speech:**
- Check microphone input levels
- Speak clearly and at normal pace
- Ensure quiet environment

**TTS generation timeout:**
- Check CodeVoice API key is valid
- Verify network connectivity to `voices.codelessai.in`
- Increase `CODEVOICE_MAX_POLLS` if needed

**LiveKit connection failed:**
- Verify LiveKit server is running
- Check API key and secret match
- Ensure WebSocket port (7880) is accessible

**Gemini API errors:**
- Verify API key is valid
- Check quota and billing status
- Review model name configuration

### Logs

View service logs:

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f livekit
```

---

## 📝 License

This project is proprietary and confidential.

---

## 🤝 Support

For issues, questions, or contributions:
- Create an issue in the repository
- Contact the development team

---

## 🙏 Acknowledgments

- **LiveKit**: Realtime communication infrastructure
- **Google Gemini**: Large language model
- **CodeVoice**: Text-to-speech synthesis platform
- **FastAPI**: Modern Python web framework
- **React**: UI library
- **Tailwind CSS**: Utility-first CSS framework

---

## 📄 Architecture Decision Records

### Why LiveKit?
- Production-ready WebRTC infrastructure
- Built-in room and participant management
- Excellent SDK support
- Scalable architecture
- Future SIP/telephony support

### Why Web Speech API?
- No additional STT service costs
- Browser-native, low latency
- Continuous listening support
- Good accuracy for common use cases
- Can be replaced with Whisper/DeepSpeech later

### Why Gemini?
- Strong conversational abilities
- Streaming support
- Competitive pricing
- Easy API integration
- Provider abstraction allows easy switching

### Why CodeVoice?
- Internal platform integration
- High-quality voice synthesis
- Async job architecture
- Modular design allows easy TTS provider switching

---

**Built with ❤️ for production-ready AI voice interactions**
#   L i v e k i t - v o i c e a g e n t - t e s t i n g  
 