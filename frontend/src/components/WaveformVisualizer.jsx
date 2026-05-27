import { useEffect, useRef } from 'react'

export function WaveformVisualizer({ isActive, isAISpeaking, audioLevel }) {
  const canvasRef = useRef(null)
  const animationRef = useRef(null)
  const barsRef = useRef([])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const barCount = 40
    
    // Initialize bars
    barsRef.current = Array.from({ length: barCount }, (_, i) => ({
      x: (canvas.width / barCount) * i,
      height: Math.random() * 20 + 5,
      targetHeight: Math.random() * 20 + 5,
      speed: Math.random() * 0.5 + 0.2
    }))

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      const bars = barsRef.current
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, 0)
      
      if (isAISpeaking) {
        gradient.addColorStop(0, '#8b5cf6')
        gradient.addColorStop(0.5, '#06b6d4')
        gradient.addColorStop(1, '#8b5cf6')
      } else if (isActive) {
        gradient.addColorStop(0, '#0ea5e9')
        gradient.addColorStop(0.5, '#06b6d4')
        gradient.addColorStop(1, '#0ea5e9')
      } else {
        gradient.addColorStop(0, '#6b7280')
        gradient.addColorStop(0.5, '#9ca3af')
        gradient.addColorStop(1, '#6b7280')
      }

      ctx.fillStyle = gradient

      bars.forEach((bar, index) => {
        if (isActive) {
          // Animate bars with wave effect
          bar.height += (bar.targetHeight - bar.height) * bar.speed
          
          // Update target periodically
          if (Math.abs(bar.height - bar.targetHeight) < 1) {
            bar.targetHeight = Math.random() * (isAISpeaking ? 80 : 60) + 20
          }
        } else {
          // Smooth transition to minimal height
          bar.height += (10 - bar.height) * 0.1
        }

        const barWidth = (canvas.width / barCount) * 0.6
        const x = bar.x + (canvas.width / barCount) * 0.2
        const y = (canvas.height - bar.height) / 2

        ctx.fillRect(x, y, barWidth, bar.height)
      })

      animationRef.current = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [isActive, isAISpeaking])

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={800}
        height={120}
        className="w-full h-32 rounded-lg"
      />
      <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
        <div className={`transition-opacity duration-300 ${isActive ? 'opacity-100' : 'opacity-0'}`}>
          {isAISpeaking ? (
            <span className="text-sm font-medium text-purple-600 dark:text-purple-400">
              AI Speaking...
            </span>
          ) : (
            <span className="text-sm font-medium text-primary-600 dark:text-primary-400">
              Listening...
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
