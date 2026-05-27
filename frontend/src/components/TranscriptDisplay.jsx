export function TranscriptDisplay({ interimTranscript, finalTranscript, aiResponse, isAISpeaking }) {
  return (
    <div className="space-y-4">
      {/* User Transcript */}
      {(finalTranscript || interimTranscript) && (
        <div className="space-y-2">
          <div className="text-sm font-medium text-gray-600 dark:text-gray-400">
            You said:
          </div>
          {finalTranscript && (
            <div className="text-lg text-gray-900 dark:text-white font-medium">
              {finalTranscript}
            </div>
          )}
          {interimTranscript && (
            <div className="text-lg text-gray-500 dark:text-gray-400 italic">
              {interimTranscript}
              <span className="animate-pulse">▌</span>
            </div>
          )}
        </div>
      )}

      {/* AI Response */}
      {aiResponse && (
        <div className="space-y-2 pt-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2">
            <div className="text-sm font-medium text-gray-600 dark:text-gray-400">
              AI Response:
            </div>
            {isAISpeaking && (
              <div className="flex gap-1">
                <div className="w-1 h-3 bg-purple-600 rounded animate-pulse"></div>
                <div className="w-1 h-3 bg-purple-600 rounded animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-1 h-3 bg-purple-600 rounded animate-pulse" style={{ animationDelay: '0.4s' }}></div>
              </div>
            )}
          </div>
          <div className="text-lg text-gray-900 dark:text-white">
            {aiResponse}
          </div>
        </div>
      )}
    </div>
  )
}
