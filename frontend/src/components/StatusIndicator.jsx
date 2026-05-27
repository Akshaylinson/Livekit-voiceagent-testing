const statusConfig = {
  idle: {
    label: 'Ready',
    color: 'bg-gray-500',
    textColor: 'text-gray-600 dark:text-gray-400'
  },
  connecting: {
    label: 'Connecting...',
    color: 'bg-yellow-500',
    textColor: 'text-yellow-600 dark:text-yellow-400'
  },
  listening: {
    label: 'Listening',
    color: 'bg-green-500',
    textColor: 'text-green-600 dark:text-green-400'
  },
  processing: {
    label: 'Processing...',
    color: 'bg-blue-500 animate-pulse',
    textColor: 'text-blue-600 dark:text-blue-400'
  },
  speaking: {
    label: 'AI Speaking',
    color: 'bg-purple-500 animate-pulse',
    textColor: 'text-purple-600 dark:text-purple-400'
  },
  error: {
    label: 'Error',
    color: 'bg-red-500',
    textColor: 'text-red-600 dark:text-red-400'
  }
}

export function StatusIndicator({ status }) {
  const config = statusConfig[status] || statusConfig.idle

  return (
    <div className="flex items-center gap-2">
      <div className={`w-3 h-3 rounded-full ${config.color}`}></div>
      <span className={`text-sm font-medium ${config.textColor}`}>
        {config.label}
      </span>
    </div>
  )
}
