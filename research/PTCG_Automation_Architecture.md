# PTCG Intelligence System: Automated Ingestion & Analytics Architecture

## 1. Objective
Establish a persistent, structured pipeline to track the "Munix Zero (M3)" meta from PokecaBook (Japan) and store it in PostgreSQL for deep card-level analysis.

## 2. Architecture Design

### A. The Scraper (Listener)
- **Target**: `https://pokecabook.com/archives/category/tournament-results/city-league`
- **Mechanism**: Python script using `BeautifulSoup` or `Selenium` (if JS rendering is needed).
- **Frequency**: Every 24 hours (aligned with Japanese City League daily updates).

### B. The Parser (Processor)
- **Task**: Extract "Deck Name", "Placement (Winner/Top 4)", and "Deck List (60 cards)".
- **Challenge**: PokecaBook lists often use images or specific deck IDs. We will focus on extracting the **Official Deck ID** (e.g., `ppUyyM-SjC4X6-URy2Rp`) to fetch the raw card data.

### C. Database Schema (PostgreSQL)
We will initialize a new database/schema `ptcg_analytics`.

```sql
CREATE TABLE IF NOT EXISTS ptcg_tournaments (
    tournament_id SERIAL PRIMARY KEY,
    event_date DATE,
    event_name TEXT,
    region VARCHAR(50) DEFAULT 'Japan'
);

CREATE TABLE IF NOT EXISTS ptcg_decklists (
    deck_id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES ptcg_tournaments(tournament_id),
    deck_type VARCHAR(100), -- e.g., Mega Lucario ex, Dragapult ex
    placement VARCHAR(20), -- Winner, Top 4, Top 8
    official_deck_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ptcg_deck_contents (
    deck_id INTEGER REFERENCES ptcg_decklists(deck_id),
    card_name_zh TEXT,
    card_quantity INTEGER
);
```

## 3. Implementation Plan
1. **Script Development**: Write `scripts/fetch_pokecabook_data.py`.
2. **PostgreSQL Setup**: Execute schema creation.
3. **Cron Job**: Set up a daily task in OpenClaw to run the ingestion.
4. **Analysis View**: Create SQL views to calculate "Card Inclusion Rate" and "Regional Win Rate Deltas".

---
*Status: Initial design complete. Ready to implement schema and scraper. 🦞🃏💻*
