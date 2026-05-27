# Quick Start Guide

Get the AI Voice Agent platform running in under 5 minutes.

---

## Prerequisites

Before you begin, ensure you have:

- ✅ **Docker Desktop** installed ([Download](https://www.docker.com/products/docker-desktop))
- ✅ **Modern browser** (Chrome recommended for best Web Speech API support)
- ✅ **API Keys** (Gemini, CodeVoice, LiveKit)

---

## Step-by-Step Setup

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd Livekit-voice-agent-testing1
```

---

### Step 2: Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys:

```env
# LiveKit Configuration
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_URL=ws://localhost:7880

# LLM Configuration (Gemini)
GEMINI_API_KEY=AIzaSy...your-gemini-api-key

# CodeVoice TTS Configuration
CODEVOICE_API_KEY=your-codevoice-api-key
CODEVOICE_VOICE=Ryan
```

**Getting API Keys:**

1. **LiveKit**: Use the included LiveKit server (default keys work) or get from [LiveKit Cloud](https://livekit.io)
2. **Gemini**: Get from [Google AI Studio](https://makersuite.google.com)
3. **CodeVoice**: Contact your internal team for access

---

### Step 3: Start Services

Run Docker Compose:

```bash
docker compose up --build
```

**What this does:**
- Builds backend and frontend containers
- Starts LiveKit server
- Starts Redis cache
- Starts FastAPI backend
- Starts Nginx frontend server

**Wait for all services to be healthy** (about 30-60 seconds).

You should see:
```
voice-agent-backend    | INFO: Application startup complete.
voice-agent-frontend   | nginx started
voice-agent-livekit    | server started
```

---

### Step 4: Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

You should see the AI Voice Agent interface with:
- Waveform visualizer
- Start/Stop listening button
- Status indicator
- Conversation history panel

---

### Step 5: Start Talking!

1. **Click "Start Listening"** button
2. **Allow microphone access** when prompted
3. **Speak naturally** - "Hello, how are you?"
4. **Wait for AI response** - The AI will speak back
5. **Continue conversation** - Just keep talking!

---

## Verification Checklist

✅ Backend API is running:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

✅ API documentation is accessible:
```
http://localhost:8000/docs
```

✅ Frontend is serving:
```
http://localhost:3000
```

✅ LiveKit is running:
```bash
curl http://localhost:7880
# Should return: HTTP 200
```

---

## Common Issues

### Issue: "Speech Recognition not working"

**Solution:**
- Use Chrome browser (best support)
- Ensure HTTPS or localhost
- Check microphone permissions
- Speak clearly and at normal pace

### Issue: "Microphone permission denied"

**Solution:**
- Click the lock icon in browser URL bar
- Enable microphone permissions
- Refresh the page
- Try again

### Issue: "Backend connection failed"

**Solution:**
```bash
# Check if backend is running
docker compose ps

# View backend logs
docker compose logs backend

# Restart backend
docker compose restart backend
```

### Issue: "TTS generation timeout"

**Solution:**
- Verify CodeVoice API key is correct
- Check internet connectivity
- Increase `CODEVOICE_MAX_POLLS` in `.env`
- View backend logs for details

### Issue: "Gemini API error"

**Solution:**
- Verify Gemini API key is valid
- Check API quota at Google AI Studio
- Ensure `GEMINI_MODEL` is correct
- Test API key with curl:
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY"
```

---

## Development Mode

For active development with hot-reload:

```bash
# Start in development mode
docker compose -f docker-compose.yml -f docker-compose.override.yml up
```

This enables:
- Backend auto-reload on code changes
- Frontend HMR (Hot Module Replacement)
- Volume mounts for live editing

---

## Stop Services

When you're done:

```bash
# Stop all services
docker compose down

# Stop and remove volumes (clean slate)
docker compose down -v
```

---

## Next Steps

### Explore the API

Visit the interactive API documentation:
```
http://localhost:8000/docs
```

Try out endpoints directly in your browser!

### Customize the System Prompt

Edit the default system prompt in `frontend/src/components/VoiceAgent.jsx`:

```javascript
const response = await axios.post(`${API_BASE_URL}/session`, {
  system_prompt: "Your custom prompt here"
});
```

### Change the Voice

Available voices (check CodeVoice documentation):

```env
# In .env
CODEVOICE_VOICE=Emma
```

### Adjust LLM Behavior

```env
# More creative responses
GEMINI_TEMPERATURE=0.9

# More focused responses
GEMINI_TEMPERATURE=0.3

# Longer responses
GEMINI_MAX_TOKENS=4096
```

---

## Monitoring

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f livekit
```

### Check Service Health

```bash
# Backend health
curl http://localhost:8000/health

# API status (includes all services)
curl http://localhost:8000/api/status
```

---

## Performance Tips

### For Best Experience:

1. **Use Chrome** - Best Web Speech API support
2. **Quiet environment** - Better speech recognition
3. **Clear speech** - Speak naturally but clearly
4. **Good microphone** - External mic improves accuracy
5. **Stable internet** - Required for LLM and TTS APIs

### Reduce Latency:

1. **Closer to API regions** - Deploy near API endpoints
2. **Faster TTS polling** - Reduce `CODEVOICE_POLL_INTERVAL` (but respect rate limits)
3. **Shorter responses** - Adjust LLM max tokens
4. **Optimize network** - Use wired connection

---

## Getting Help

### Documentation

- **README.md** - Complete overview
- **ARCHITECTURE.md** - System architecture details
- **API_REFERENCE.md** - Complete API documentation

### Logs

Check logs for error messages:
```bash
docker compose logs --tail=100 backend
```

### Support

- Create an issue in the repository
- Contact the development team
- Check existing documentation

---

## What's Next?

Now that you have the platform running:

1. ✅ **Test the voice conversation** - Try different queries
2. ✅ **Explore the API** - Use the interactive docs
3. ✅ **Read the architecture** - Understand how it works
4. ✅ **Customize** - Modify prompts, voices, settings
5. ✅ **Contribute** - Add features or improvements

---

## Quick Commands Reference

```bash
# Start services
docker compose up --build

# Start in background
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Restart a service
docker compose restart backend

# Rebuild a service
docker compose build backend

# View running containers
docker compose ps

# Access backend shell
docker compose exec backend bash

# Access frontend shell
docker compose exec frontend sh
```

---

**Happy Voice Conversing! 🎙️🤖**
