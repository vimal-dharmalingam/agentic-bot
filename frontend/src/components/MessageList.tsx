import { useEffect, useRef } from 'react'
import type { ChatMessage } from '../types/chat'

interface MessageListProps {
  messages: ChatMessage[]
  isLoading: boolean
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  // after every new message, scroll to the bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  if (messages.length === 0) {
    return <p className="empty">Say hello to start the conversation.</p>
  }

  return (
    <div className="message-list">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.role}`}>
          {message.content}
        </div>
      ))}
      {isLoading && <div className="message assistant typing">Thinking…</div>}
      <div ref={bottomRef} />
    </div>
  )
}