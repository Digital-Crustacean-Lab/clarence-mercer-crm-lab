# Direction 2: Identity Resolution (The Customer 360 Puzzle)

## 🎯 Executive Concept
In a world where one person has three emails, two phone numbers, and five social handles, "Identity Resolution" is the process of uniting these "digital ghosts" into a single, high-fidelity customer profile.

## 🔬 Deep Research Findings
- **The Fellegi-Sunter Model**: This is the mathematical bedrock of probabilistic linkage. It uses **Match Weights** to calculate the probability that two records are the same based on the uniqueness of the field (e.g., a match on "Postal Code" is less significant than a match on "Full Name").
- **Probabilistic vs. Deterministic**: Modern systems are moving away from strict "If Email A == Email B" logic towards probabilistic models that handle typos, nicknames, and outdated addresses.
- **High-Performance Tools**:
    - **Splink**: Uses DuckDB/Spark to link millions of records in seconds using probabilistic logic.
    - **Zingg**: An enterprise-grade tool that uses machine learning to "learn" how to link data.

## 🦞 The Mercer Strategic Angle: "The Data Ghost"
*Mercer’s Insight: "A master chef knows that a customer who visits the restaurant and one who orders delivery is the same person. If you treat them as strangers, you lose the opportunity to serve them their favorite vintage."*
- **Strategy**: Creating a "Golden Record"—the single version of truth for every customer.
- **Technical Challenge**: Balancing the "merging" of records with privacy laws like GDPR (The Right to be Forgotten).

## 📂 Suggested Lab Assets
- **The Toolkit**: `Splink` (Python) for fast SQL-based deduplication.
- **Dataset**: **UCI Record Linkage Comparison Patterns** (contains 5 million+ records with synthetic noise).
