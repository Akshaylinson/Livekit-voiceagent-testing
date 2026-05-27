import { useState, useEffect, useCallback } from 'react'
import { VoiceAgent } from './components/VoiceAgent'
import { ThemeToggle } from './components/ThemeToggle'

function App() {
  const [darkMode, setDarkMode] = useState(true)

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  const toggleTheme = useCallback(() => {
    setDarkMode(prev => !prev)
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle darkMode={darkMode} onToggle={toggleTheme} />
      </div>
      
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <header className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-3">
            AI Voice Agent
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Realtime Conversational Assistant powered by LiveKit
          </p>
        </header>

        <VoiceAgent />
      </div>
    </div>
  )
}

export default App
