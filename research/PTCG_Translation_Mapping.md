# PTCG Translation & Mapping Layer: Japanese to Traditional Chinese (Standard Format)

## 1. Core Rule & Objective
All data ingested from Japanese sources (PokecaBook) must be passed through this mapping layer before being stored in PostgreSQL or displayed to the user. This ensures consistent use of Official Traditional Chinese (Taiwan) card names.

## 2. Master Mapping Table (Sample)

### 🏷️ Deck Types (牌組類型)
- **メガルカリオ ex** -> 超級路卡利歐 ex
- **ドラパルト ex** -> 多龍梅西亞 ex
- **マリィのオーロンゲ ex** -> 瑪俐的長毛巨魔 ex
- **レジギガス** -> 雷吉奇卡斯
- **リザードン ex** -> 噴火龍 ex
- **サーナイト ex** -> 沙奈朵 ex
- **コレクレー / サーフゴー ex** -> 索財靈 / 賽富豪 ex

### 🃏 Key Support Cards (關鍵支援卡)
- **ヒーローマント** -> 英雄斗篷
- **ミツル** -> 赤日 (Birch / Collector logic depending on context)
- **ドロンチ** -> 多龍奇
- **ヨノワール** -> 夜黑魔靈
- **ナンジャモ** -> 奇樹
- **ボスの指令** -> 老大的指令
- **マシマシラ** -> 願增猿

## 3. Implementation Mechanism
The automated scraper (`scripts/fetch_pokecabook_automated.py`) will integrate a `translate_card_names()` function using a local dictionary lookup. If a new card is detected, the system will flag it for translation verification.
