# Quick Reference Card

Your at-a-glance guide for the AI Voice Agent Platform.

---

## 🚀 Quick Start

```bash
# Setup
cp .env.example .env
# Edit .env with API keys

# Start
docker compose up --build

# Access
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# Backend: http://localhost:8000
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.env.example` | Environment template |
| `docker-compose.yml` | Service orchestration |
| `backend/main.py` | Backend entry point |
| `frontend/src/App.jsx` | Frontend entry point |
| `README.md` | Main documentation |
| `QUICKSTART.md` | Setup guide |
| `API_REFERENCE.md` | API docs |

---

## 🔑 Environment Variables

```env
# Required
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
GEMINI_API_KEY=your_key
CODEVOICE_API_KEY=your_key

# Optional (with defaults)
LIVEKIT_URL=ws://localhost:7880
GEMINI_MODEL=gemini-pro
CODEVOICE_VOICE=Ryan
BACKEND_PORT=8000
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/session` | POST | Create session |
| `/api/v1/conversation` | POST | Process voice input |
| `/api/v1/tts` | POST | Generate speech |
| `/api/v1/token` | POST | Get LiveKit token |
| `/health` | GET | Health check |
| `/api/status` | GET | Service status |

**Test API:** http://localhost:8000/docs

---

## 🛠️ Common Commands

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f backend

# Restart service
docker compose restart backend

# Stop all
docker compose down

# Rebuild
docker compose up --build

# Check status
docker compose ps
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Mic not working | Use Chrome, check permissions |
| STT fails | Speak clearly, quiet environment |
| TTS timeout | Check API key, internet connection |
| Backend error | View logs: `docker compose logs backend` |
| Frontend not loading | Check if container is running |

---

## 📊 Service Ports

| Service | Port | Protocol |
|---------|------|----------|
| Frontend | 3000 | HTTP |
| Backend API | 8000 | HTTP |
| LiveKit | 7880 | WebSocket |
| Redis | 6379 | TCP |

---

## 🎯 Feature Flags

```javascript
// Frontend: Continuous vs Push-to-Talk
isContinuousMode = true  // Always listening
isContinuousMode = false // Push-to-talk
```

```env
# Backend: LLM Behavior
GEMINI_TEMPERATURE=0.7    # Creativity (0-1)
GEMINI_MAX_TOKENS=2048    # Response length
```

---

## 📚 Documentation

| Document | When to Use |
|----------|-------------|
| QUICKSTART.md | First time setup |
| README.md | Complete overview |
| ARCHITECTURE.md | System design |
| API_REFERENCE.md | API details |
| DEPLOYMENT_CHECKLIST.md | Production deploy |

---

## 🔧 Development

```bash
# Dev mode with hot-reload
docker compose -f docker-compose.yml -f docker-compose.override.yml up

# Backend only
cd backend
uvicorn backend.main:app --reload

# Frontend only
cd frontend
npm install
npm run dev
```

---

## 🎨 Customization

```javascript
// Change system prompt
// frontend/src/components/VoiceAgent.jsx
system_prompt: "Your custom prompt"

// Change voice
// .env
CODEVOICE_VOICE=Emma

// Change LLM behavior
// .env
GEMINI_TEMPERATURE=0.9
```

---

## 📞 Quick Help

- **API Docs:** http://localhost:8000/docs
- **Logs:** `docker compose logs -f`
- **Health:** http://localhost:8000/health
- **Status:** http://localhost:8000/api/status

---

## ⚡ Performance Tips

1. Use Chrome browser
2. Good microphone
3. Quiet environment
4. Stable internet
5. Clear speech

---

## 🔐 Security Checklist

- [ ] Set strong API keys
- [ ] Configure CORS
- [ ] Enable HTTPS (production)
- [ ] Add rate limiting
- [ ] Implement auth
- [ ] Regular updates

---

## 🎉 Success Indicators

✅ Frontend loads at :3000
✅ Backend healthy at :8000/health
✅ API docs accessible
✅ LiveKit connected
✅ STT recognizes speech
✅ LLM generates responses
✅ TTS creates audio
✅ Audio plays successfully

---

**Print this page for quick reference!**
