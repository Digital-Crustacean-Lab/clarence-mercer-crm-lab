# Direction 2: Identity Resolution (The Customer 360 Puzzle)

## Concept
The average customer interacts with a brand across 15+ data sources. Identity Resolution (or Entity Resolution) is the process of linking these disparate records into a single "Customer 360" profile.

## Research Findings
- **Probabilistic Linkage**: Using algorithms like Fellegi-Sunter to determine the likelihood that two records refer to the same person.
- **Python Tools**:
    - `Dedupe`: Uses machine learning for record linkage.
    - `Splink`: High-performance probabilistic linkage at scale.

## Strategic Strategy for Mercer
- **The "Data Ghost"**: Dealing with partial data (e.g., a phone number without an email).
- **GDPR & Privacy**: Balancing identity resolution with the "Right to be Forgotten."

## Suggested Dataset
- **UCI Record Linkage Comparison Patterns**: Real-world data with noise for testing linkage algorithms.
