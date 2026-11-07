## Phase 1 - DynamoDB
- Table: agentic-bot-sessions (us-east-1)
- PK session_id (S), SK ts (N) - one item per message
- On-demand, Standard class, TTL on expires_at (epoch seconds)
- Created via CLI after console typo (session-id) - keys are immutable