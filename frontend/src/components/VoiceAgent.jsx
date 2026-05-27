import { useState, useEffect, useRef, useCallback } from 'react'
import axios from 'axios'
import { WaveformVisualizer } from './WaveformVisualizer'
import { TranscriptDisplay } from './TranscriptDisplay'
import { ConversationHistory } from './ConversationHistory'
import { StatusIndicator } from './StatusIndicator'
import { MicIcon, StopIcon, PushToTalkIcon } from './Icons'

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000/api/v1'

export function VoiceAgent() {
  // Session state
  const [sessionId, setSessionId] = useState(null)
  const [status, setStatus] = useState('idle') // idle, connecting, listening, processing, speaking, error
  
  // STT state
  const [isListening, setIsListening] = useState(false)
  const [isContinuousMode, setIsContinuousMode] = useState(true)
  const [isPushToTalk, setIsPushToTalk] = useState(false)
  const [interimTranscript, setInterimTranscript] = useState('')
  const [finalTranscript, setFinalTranscript] = useState('')
  
  // Conversation state
  const [conversationHistory, setConversationHistory] = useState([])
  const [currentResponse, setCurrentResponse] = useState('')
  const [isAISpeaking, setIsAISpeaking] = useState(false)
  
  // Audio state
  const [audioLevel, setAudioLevel] = useState(0)
  
  // Refs
  const recognitionRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const animationFrameRef = useRef(null)
  const audioRef = useRef(null)

  // Initialize session
  const initializeSession = useCallback(async () => {
    try {
      setStatus('connecting')
      
      const response = await axios.post(`${API_BASE_URL}/session`, {
        system_prompt: "You are a helpful AI voice assistant. Respond conversationally and naturally. Keep responses concise and engaging."
      })
      
      setSessionId(response.data.session_id)
      setStatus('idle')
      
      console.log('Session initialized:', response.data.session_id)
    } catch (error) {
      console.error('Failed to initialize session:', error)
      setStatus('error')
    }
  }, [])

  // Setup speech recognition
  const setupSpeechRecognition = useCallback(() => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      console.error('Speech Recognition API not supported in this browser')
      setStatus('error')
      return null
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()
    
    recognition.continuous = isContinuousMode
    recognition.interimResults = true
    recognition.lang = 'en-US'

    recognition.onstart = () => {
      console.log('Speech recognition started')
      setIsListening(true)
      setStatus('listening')
    }

    recognition.onresult = async (event) => {
      let interim = ''
      let final = ''

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript
        if (event.results[i].isFinal) {
          final += transcript
        } else {
          interim += transcript
        }
      }

      setInterimTranscript(interim)
      
      if (final) {
        setFinalTranscript(final)
        console.log('Final transcript:', final)
        
        // Send to backend for processing
        await processTranscript(final)
      }
    }

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error)
      setIsListening(false)
      
      if (event.error === 'not-allowed') {
        setStatus('error')
      } else if (event.error === 'no-speech') {
        // Auto-restart if continuous mode
        if (isContinuousMode && isListening) {
          try {
            recognition.start()
          } catch (e) {
            // Ignore if already started
          }
        }
      }
    }

    recognition.onend = () => {
      console.log('Speech recognition ended')
      setIsListening(false)
      
      // Auto-restart if continuous mode
      if (isContinuousMode && status !== 'processing' && status !== 'speaking') {
        setTimeout(() => {
          try {
            recognition.start()
          } catch (e) {
            // Ignore errors
          }
        }, 100)
      }
    }

    recognitionRef.current = recognition
    return recognition
  }, [isContinuousMode, status])

  // Process transcript through backend
  const processTranscript = async (transcript) => {
    if (!sessionId) return

    try {
      setStatus('processing')
      setIsListening(false)
      
      // Stop listening while processing
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }

      // Send to backend
      const response = await axios.post(`${API_BASE_URL}/conversation`, {
        session_id: sessionId,
        transcript: transcript,
        is_final: true
      })

      const aiResponse = response.data.assistant_response
      setCurrentResponse(aiResponse)
      
      // Add to conversation history
      setConversationHistory(prev => [
        ...prev,
        { role: 'user', content: transcript },
        { role: 'assistant', content: aiResponse }
      ])

      // Synthesize speech
      await synthesizeSpeech(aiResponse)

    } catch (error) {
      console.error('Failed to process transcript:', error)
      setStatus('error')
      
      // Resume listening on error
      if (isContinuousMode) {
        startListening()
      }
    }
  }

  // Synthesize speech using CodeVoice TTS
  const synthesizeSpeech = async (text) => {
    if (!sessionId) return

    try {
      setStatus('speaking')
      setIsAISpeaking(true)

      // Request TTS generation
      const ttsResponse = await axios.post(`${API_BASE_URL}/tts`, {
        session_id: sessionId,
        text: text
      })

      const jobId = ttsResponse.data.job_id

      // Poll for completion
      let audioUrl = null
      let attempts = 0
      const maxAttempts = 60

      while (attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        const statusResponse = await axios.get(`${API_BASE_URL}/tts/${jobId}/status`)
        
        if (statusResponse.data.status === 'completed') {
          audioUrl = `${API_BASE_URL}/tts/${jobId}/audio`
          break
        } else if (statusResponse.data.status === 'failed') {
          throw new Error('TTS generation failed')
        }
        
        attempts++
      }

      if (audioUrl) {
        // Play audio
        const audio = new Audio(audioUrl)
        audioRef.current = audio
        
        audio.onended = () => {
          setIsAISpeaking(false)
          setCurrentResponse('')
          
          // Resume listening after AI finishes speaking
          if (isContinuousMode) {
            startListening()
          } else {
            setStatus('idle')
          }
        }

        audio.onerror = () => {
          console.error('Audio playback error')
          setIsAISpeaking(false)
          setStatus('error')
        }

        await audio.play()
      }

    } catch (error) {
      console.error('Failed to synthesize speech:', error)
      setIsAISpeaking(false)
      setStatus('error')
    }
  }

  // Start listening
  const startListening = useCallback(() => {
    if (!recognitionRef.current) {
      setupSpeechRecognition()
    }

    try {
      setInterimTranscript('')
      setFinalTranscript('')
      recognitionRef.current.start()
    } catch (error) {
      console.error('Failed to start listening:', error)
    }
  }, [setupSpeechRecognition])

  // Stop listening
  const stopListening = useCallback(() => {
    if (recognitionRef.current) {
      recognitionRef.current.stop()
    }
    setIsListening(false)
    setStatus('idle')
  }, [])

  // Push-to-talk handlers
  const handlePushToTalkStart = useCallback(() => {
    setIsPushToTalk(true)
    startListening()
  }, [startListening])

  const handlePushToTalkEnd = useCallback(() => {
    setIsPushToTalk(false)
    stopListening()
  }, [stopListening])

  // Initialize on mount
  useEffect(() => {
    initializeSession()
    
    return () => {
      // Cleanup
      if (recognitionRef.current) {
        recognitionRef.current.stop()
      }
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [initializeSession])

  return (
    <div className="space-y-6">
      {/* Status Bar */}
      <div className="flex items-center justify-between">
        <StatusIndicator status={status} />
        <div className="flex gap-2">
          <button
            onClick={() => setIsContinuousMode(!isContinuousMode)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              isContinuousMode
                ? 'bg-primary-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
          >
            Continuous Mode
          </button>
        </div>
      </div>

      {/* Waveform Visualizer */}
      <div className="card">
        <WaveformVisualizer
          isActive={isListening || isAISpeaking}
          isAISpeaking={isAISpeaking}
          audioLevel={audioLevel}
        />
      </div>

      {/* Controls */}
      <div className="flex justify-center gap-4">
        {isContinuousMode ? (
          <button
            onClick={isListening ? stopListening : startListening}
            className={`btn-primary flex items-center gap-2 ${
              isListening ? 'bg-red-600 hover:bg-red-700' : ''
            }`}
            disabled={status === 'processing' || status === 'speaking'}
          >
            {isListening ? (
              <>
                <StopIcon />
                Stop Listening
              </>
            ) : (
              <>
                <MicIcon />
                Start Listening
              </>
            )}
          </button>
        ) : (
          <button
            onMouseDown={handlePushToTalkStart}
            onMouseUp={handlePushToTalkEnd}
            onTouchStart={handlePushToTalkStart}
            onTouchEnd={handlePushToTalkEnd}
            className="btn-primary flex items-center gap-2"
            disabled={status === 'processing' || status === 'speaking'}
          >
            <PushToTalkIcon />
            {isPushToTalk ? 'Listening...' : 'Push to Talk'}
          </button>
        )}
      </div>

      {/* Live Transcript */}
      {(interimTranscript || finalTranscript || currentResponse) && (
        <div className="card">
          <TranscriptDisplay
            interimTranscript={interimTranscript}
            finalTranscript={finalTranscript}
            aiResponse={currentResponse}
            isAISpeaking={isAISpeaking}
          />
        </div>
      )}

      {/* Conversation History */}
      {conversationHistory.length > 0 && (
        <div className="card">
          <ConversationHistory messages={conversationHistory} />
        </div>
      )}
    </div>
  )
}
