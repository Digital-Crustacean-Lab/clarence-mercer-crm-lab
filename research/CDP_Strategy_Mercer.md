# Research: CDP (Customer Data Platform) - Strategic Role in Mercer Lab

## 1. What is a CDP?
A **Customer Data Platform (CDP)** is a specialized software that aggregates customer data from multiple sources (Social, Web, POS, Voice Assistants) to create a **Single Customer View (Unified Profile)**.

### CRM vs. CDP:
- **CRM**: Focuses on *interactions* (Sales calls, support tickets). It's primarily a tool for humans to manage leads.
- **CDP**: Focuses on *data integration* (Aggregating messy events). It's a tool for machines/AI to understand the customer's identity.

## 2. Why Mercer Lab needs a CDP approach?
In Phase 3, we tackled **Identity Resolution**. A CDP is essentially the "home" for those resolved identities. 

### Mercers' Use Cases for CDP:
1. **Identity Home**: Storing the link between "Digital Ghosts" (Alexa ID, Social ID) and the Master Record.
2. **Behavioral Triggering**: Tracking when a customer *looks* at a product (Edge intent) and instantly pushing that to the CRM for action.
3. **Data Freshness**: Ensuring the CLV model has the *latest* data from every touchpoint, not just old transaction logs.

## 3. Implementation Strategy (The Lab Way)
We don't necessarily need to buy an expensive CDP (like Segment or mParticle). We can build a **"Composable CDP"** using:
- **PostgreSQL**: As the centralized identity storage.
- **Reverse ETL**: To push insights back to Mattermost/Salesforce.
- **NLP Engine**: To enrich the unified profile with intent scores.

---
**Conclusion**: A CDP is the "Brain" where all Phase 3-6 insights live. I use this concept every time I link a voice intent to a database ID.
