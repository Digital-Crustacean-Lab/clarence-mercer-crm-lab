# Mattermost Store-to-Center Bridge Bot (Design Document)

## 1. 核心流程 (Core Workflow)
- **入口**: 每個店鋪使用獨立帳號登入 Mattermost。
- **發起**: 店鋪員工對 Bot 發送私訊 (Direct Message) 提出需求。
- **分派**: Bot 接收訊息後，將其轉發至 Call Center 的專屬頻道 (Channel)。
- **搶單/佔位機制**:
    - Bot 發送訊息時會附帶一個「領取任務」的按鈕 (Interactive Button) 或要求 Agent 使用特定的 Emoji 反應（如 :raised_hand:）。
    - **第一個**點擊按鈕或反應的 Agent 會被系統鎖定為「承辦人」。
    - Bot 會更新該則訊息，標註：`[已由 Agent A 領取]`，並阻擋其他人重複領取。
    - **解決搶單爭議**: 系統以 Bot 接收到 API 請求的時間戳 (Timestamp) 為準，毫秒級判定誰是第一人。
- **隔離**: 由於店鋪是透過私訊與 Bot 溝通，不同店鋪帳號之間完全無法看到彼此的對話內容。
- **回覆**: 只有被鎖定的 Agent 可以回覆該 Thread，Bot 自動將回覆內容私訊給對應的店鋪。

## 2. 關鍵組件 (Components)

### A. 訊息分派器 (Dispatcher)
- **邏輯**: 
    - 建立一個 `StoreRequest` 映射表（Store ID <-> Ticket ID）。
    - 當新訊息進來，若該店鋪已有開啟中的任務，則追加訊息；若無，則建立新任務。
    - 轉發至 Call Center 頻道，格式化為：`[店鋪 A] 需求描述`。

### B. 狀態追蹤器 (State Tracker)
- **欄位**:
    - `store_user_id`: 發起人的 Mattermost ID。
    - `agent_id`: 承辦人的 Mattermost ID（分派後填入）。
    - `status`: [Pending, Processing, Resolved]。
    - `thread_id`: 在 Call Center 頻道的訊息 Thread ID。

### C. 隱私層 (Privacy Layer)
- **機制**: 
    - 利用 Mattermost 的 **Personal Access Tokens** 或 **Bot Accounts**。
    - 店鋪端只會看到與 Bot 的對話視窗。

## 3. 推薦實作技術 (Stack)
- **語言**: Python。
- **函式庫**: `mattermostdriver` (官方推薦的 Python Driver)。
- **觸發機制**: 使用 **Outgoing Webhooks** 或 **WebSocket Client** 監聽訊息。

## 4. 進階整合 (Clarence Mercer Style)
- **CRM 連結**: 將店鋪的需求與我們的 `crm_db` 同步，自動帶出該店鋪的過往紀錄給 Agent 參考。
- **意圖偵測**: 如果店鋪傳送「緊急」、「火災」或「VIP」字眼，Bot 自動跳過分派邏輯，改為全頻道 @all 廣播。

---
**龍蝦建議**: 
我們先從「私訊轉發到 Call Center 頻道」這個最核心的邏輯開始寫起嗎？我可以幫你寫一個初步的 Python 腳本。
