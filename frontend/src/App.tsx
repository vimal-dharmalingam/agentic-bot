import { MessageInput } from './components/MessageInput'
import { MessageList } from './components/MessageList'
import { useChat } from './hooks/useChat'
import './App.css'

function App() {
  const { messages, sessionId, isLoading, error, send, reset } = useChat()

  return (
    <div className="app">
      <header className="app-header">
        <h1>Agentic Bot</h1>
        <button className="secondary" onClick={reset} disabled={isLoading}>
          New chat
        </button>
      </header>

      <main className="chat">
        <MessageList messages={messages} isLoading={isLoading} />
        {error && <div className="error">{error}</div>}
      </main>

      <MessageInput onSend={send} disabled={isLoading} />
      <footer className="session">Session: {sessionId ?? 'new'}</footer>
    </div>
  )
}

export default App