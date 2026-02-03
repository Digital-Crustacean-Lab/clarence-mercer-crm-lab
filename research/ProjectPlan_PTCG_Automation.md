# Project Plan: PTCG Intelligence Automation (M3 Meta)

## 1. Objective
Build a robust, fully automated pipeline to ingest Japanese City League results from PokecaBook, resolve official card data, and maintain a high-fidelity analytics database in PostgreSQL.

## 2. Technical Stack
- **Languages**: Python 3.11
- **Libraries**: 
    - `BeautifulSoup4`: Primary web parsing.
    - `Playwright` or `Selenium`: (Fallback) For JS-heavy card deck renders.
    - `psycopg2`: Database orchestration.
    - `thefuzz`: To handle translation edge cases.
- **Database**: PostgreSQL (hosted on Zeabur).
- **Automation**: OpenClaw Cron Scheduler.

## 3. Execution Phases

### Phase A: The Discovery Scraper (High Efficiency)
- **Task**: Daily scan of `pokecabook.com/archives/category/tournament-results/city-league`.
- **Output**: Extraction of **Tournament ID** and **Official Deck ID** (e.g., `ppUyyM-SjC4X6-URy2Rp`).
- **Goal**: Identify *what* happened without downloading duplicate data.

### Phase B: The Card-Level Ingestor (Precision)
- **Task**: Use the Official Deck ID to fetch the 60-card list from the official Pokemon-Card.com source.
- **Processing**: Apply the **Official Chinese Translation Layer** to every card name.
- **Goal**: Populate `ptcg_deck_contents` with 100% accurate quantities.

### Phase C: The Analytical Reporting Engine (Insight)
- **Task**: Daily execution of `analyze_ptcg_daily.py`.
- **Output**: 
    - Inclusion rates of key 2026 cards (e.g., Birch, Hero's Cape).
    - Matchup win-rate estimates based on placement frequency.
- **Goal**: Generate the daily strategic report for the user.

## 4. Adversarial Audit (Failure Points)
- **Risk**: PokecaBook changes their HTML class names (again).
    - *Mitigation*: Implementation of a "Structure Monitor" that alerts the user if zero records are found during a run.
- **Risk**: New cards released without official Chinese names.
    - *Mitigation*: Fallback to JP name with a [PENDING_TRANSLATION] flag in the database.

## 5. Success Metrics
- **Data Fidelity**: 0% hard-coded simulation data in reports.
- **Automation**: Zero manual intervention required for daily updates.
- **Coverage**: At least 95% of top 16 decklists from major City Leagues captured.

---
*Generated via Mercer Intelligence Lab / Project Planner v1.0 🦞*
