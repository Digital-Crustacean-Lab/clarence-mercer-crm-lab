# Mattermost Communication Platform - Action Plan

## 1. Authentication & Connection
- **Mattermost URL**: (Provided by user later)
- **Bot Token**: (Generated in Mattermost > Integrations > Bot Accounts)
- **Network**: Since Mattermost is on a separate Zeabur service, we will communicate via the standard HTTPS REST API and WebSocket.

## 2. Database Schema (PostgreSQL)
We need a tracking table in our current `crm_db` to manage ticket states and agent performance.

```sql
CREATE TABLE IF NOT EXISTS mattermost_tickets (
    ticket_id SERIAL PRIMARY KEY,
    store_user_id VARCHAR(50) NOT NULL,
    store_name VARCHAR(100),
    call_center_thread_id VARCHAR(50),
    assigned_agent_id VARCHAR(50),
    status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, PROCESSING, RESOLVED
    intent_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP,
    resolved_at TIMESTAMP,
    last_msg_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agent_performance (
    agent_id VARCHAR(50) PRIMARY KEY,
    agent_name VARCHAR(100),
    total_resolved INTEGER DEFAULT 0,
    avg_response_time_sec FLOAT DEFAULT 0,
    total_points INTEGER DEFAULT 0
);
```

## 3. Bot Logic Implementation (Python)
- **Listener**: A WebSocket client that listens for `posted` events in Direct Messages.
- **Router**: 
    - When a DM arrives from a Store, check if an active ticket exists.
    - If not, create a ticket, calculate intent, and post a "Claim" button to the Call Center channel.
- **Controller**:
    - Handle the `interactive_dialog` or `button_click` event when an Agent clicks "Claim".
    - Update the database and the original message.
- **Relay**:
    - Any subsequent messages in that Thread from the Agent are relayed back to the Store via DM.
    - Any messages from the Store are relayed into the Thread.
