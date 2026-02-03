# NLP Intent Classifier Upgrade Plan

## 1. Objective
Transition from simple keyword matching to a sophisticated **Sentiment + Negation Aware Intent Engine**. Compare the accuracy and lead quality against the current baseline.

## 2. Methodology & Algorithms
- **Baseline (V1)**: Keyword-based lookup (`buy`, `purchase`, `love`). High recall, low precision (captures "didn't buy").
- **NLP Upgrade (V2)**: 
    - **Step A: Text Normalization**: Lowercase, punctuation removal, and tokenization using `NLTK`.
    - **Step B: Negation Handling**: Identifying phrases like "not", "didn't", "never" and neutralizing intent scores within those windows.
    - **Step C: Sentiment Analysis**: Using **VADER (Valence Aware Dictionary and sEntiment Reasoner)** to distinguish between "I love this product" (High Intent) vs "I hate this product" (Churn Risk).
    - **Step D: POS Tagging (Part-of-Speech)**: Focusing on Verb-Noun pairs (e.g., `buy` + `Echo`) to confirm transactional intent.

## 3. Comparative Metrics
| Metric | Keyword Baseline (V1) | NLP Engine (V2) |
| :--- | :--- | :--- |
| **Total Leads** | 1,162 | Expected: ~400-600 |
| **Precision** | Low (includes negations) | High (intent-aware) |
| **Actionability** | General | Specific (Upsell vs Support) |

## 4. Implementation Timeline
1. Install necessary NLP libraries (`nltk`, `vaderSentiment`).
2. Create `scripts/phase3_nlp_intent_audit.py`.
3. Run head-to-head comparison on the 3,150 Alexa records.
4. Export a "Lead Quality Report" to `data/lead_comparison_results.csv`.
