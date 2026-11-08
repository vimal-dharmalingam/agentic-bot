export type Role = 'user' | 'assistant'

export interface ChatMessage {
  role: Role
  content: string
}

// mirrors backend ChatRequest / ChatResponse (Pydantic schemas)
export interface ChatRequest {
  message: string
  session_id?: string | null
}

export interface ChatResponse {
  session_id: string
  reply: string
}