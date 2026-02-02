# Newsletter Part 2: Catching Digital Ghosts with Physical Reality - The Forensic CRM Audit
**Platform**: The Practical Data Lab (Substack)

## Why Black-Box Anomaly Detection Fails
Supervised learning models like XGBoost are powerful but fragile. They are trained on *past* fraud patterns. In this lab session, we demonstrate why grounding your defense in the **physical laws of the world** is more effective than probabilistic guessing.

## Case Study: The "Impossible Travel" Audit
We audited 300,000 transaction streams. Instead of looking for "unusual amounts," we calculated the **Geographical Velocity** between consecutive transactions for each client.

### The Math: Haversine & Physics
By using the **Haversine Formula** to calculate the great-circle distance on a sphere, we identified 246 instances of "Impossible Travel." 

**Forensic Sample:**
- Transaction A: Nevada (10:00 AM)
- Transaction B: Massachusetts (10:14 AM)
- Calculated Speed: **16,193 km/h**

Unless your customer owns a scramjet, this is a binary proof of stolen credentials. 

### Implementation Tip: Numerical Fingerprinting
To further prevent "Identity Drift," we implement a secondary audit layer that extracts and compares numeric strings (Model numbers, Storage capacity).

```python
import re

def apply_numeric_fingerprint(title_a, title_b):
    nums_a = set(re.findall(r'\d+', title_a))
    nums_b = set(re.findall(r'\d+', title_b))
    
    # If titles look similar but specs (numbers) differ, reject the match
    return nums_a == nums_b
```

## Practical Takeaway
By shifting from "Behavioral Probability" to "Physical Evidence," we eliminated 100% of high-risk false positives in our product linkage tests.

---
**Next up**: Game Theory in Marketing—Applying the Shapley Value to your budget.
