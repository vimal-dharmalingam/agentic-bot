import { useState } from 'react'
import { sendMessage } from '../api/chatClient'
import type { ChatMessage } from '../types/chat'

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function send(text: string) {
    const trimmed = text.trim()
    if (!trimmed || isLoading) return

    setError(null)
    setMessages((prev) => [...prev, { role: 'user', content: trimmed }])   // show instantly
    setIsLoading(true)

    try {
      const response = await sendMessage({ message: trimmed, session_id: sessionId })
      setSessionId(response.session_id)
      setMessages((prev) => [...prev, { role: 'assistant', content: response.reply }])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setIsLoading(false)
    }
  }

  function reset() {
    setMessages([])
    setSessionId(null)
    setError(null)
  }

  return { messages, sessionId, isLoading, error, send, reset }
}