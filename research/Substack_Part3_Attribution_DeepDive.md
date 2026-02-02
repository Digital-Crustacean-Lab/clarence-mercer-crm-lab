# Newsletter Part 3: The Game Theory of Budgeting - Fair-Share Marketing Attribution
**Platform**: The Practical Data Lab (Substack)

## The War of "Last-Click"
Most marketing dashboards are lies. They give 100% of the credit to the final link clicked. In this lab session, we demonstrate how to use **Cooperative Game Theory** to end the internal war between Social, Email, and Search teams.

## The Solution: Shapley Value + Time Decay
The **Shapley Value** calculates the unique contribution of each "player" (channel) to the "win" (conversion). 

### The Time-Decay Multiplier
A contact that happened 2 months ago shouldn't carry the same weight as one from 2 hours ago. We implement an **Exponential Time-Decay function** ($e^{-\lambda t}$) to normalize the contribution.

```python
import numpy as np

def calculate_decayed_contribution(total_wins, days_to_close):
    # Higher lambda = faster decay
    decay_factor = np.exp(-0.05 * days_to_close)
    return total_wins * decay_factor
```

## Discovery: The "Fast-Cash" Engine
Our audit of 8,000 leads in the Olist dataset revealed that **Display Ads**, though low in volume, had the fastest closing cycle (**10.3 days** avg). In a cash-flow sensitive business, this makes them more valuable than higher-volume "slow burn" channels like Organic Search (50 days).

## Practical Takeaway
Stop rewarding only the striker who kicks the ball. Use the Shapley Value to reward the mid-fielders. Ground your budget in **Mathematical Fairness.**

---
**This concludes our 3-part CRM Masterclass.** For strategic consultation, contact the Lab.
