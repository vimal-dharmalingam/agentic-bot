import { useState } from 'react'

interface MessageInputProps {
  onSend: (text: string) => void
  disabled: boolean
}

export function MessageInput({ onSend, disabled }: MessageInputProps) {
  const [text, setText] = useState('')

  return (
    <form
      className="message-input"
      onSubmit={(event) => {
        event.preventDefault()          // stop the browser reloading the page
        if (!text.trim()) return
        onSend(text)
        setText('')
      }}
    >
      <input
        value={text}
        onChange={(event) => setText(event.target.value)}
        placeholder="Type a message…"
        disabled={disabled}
        autoFocus
      />
      <button type="submit" disabled={disabled || !text.trim()}>
        Send
      </button>
    </form>
  )
}