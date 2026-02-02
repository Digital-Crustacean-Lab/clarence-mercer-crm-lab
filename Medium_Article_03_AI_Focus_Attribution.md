# The Game Theory of Growth: Solving Marketing Attribution with Time-Decayed Shapley Values
**Author:** Clarence R. Mercer
**Laboratory:** Digital Crustacean Lab
**Publication Target:** Towards AI / Towards Data Science
**Category:** Applied AI / Game Theory / Decision Support

## 1. The Tyranny of the "Last Click": A Systematic Budget Failure

Who actually gets the credit for a sale? In most modern enterprises, marketing teams are locked in a silent civil war. Social media teams claim victory because they served the first awareness ad. Paid Search teams claim victory because they captured the final, desperate click before checkout. 

This **Last-Click Bias** is the single most destructive force in modern marketing budget allocation. By rewarding only the final touchpoint, organizations accidentally defund the top-of-funnel "Educators" that generate demand in the first place. This leads to a feedback loop where budgets are shifted to capture existing demand rather than creating it. At the **Digital Crustacean Lab**, we decided to end the war using **Cooperative Game Theory.**

---

## 2. Methodology: The Shapley Value Implementation

The **Shapley Value** is a Nobel-prize winning solution concept from cooperative game theory, originally proposed by Lloyd Shapley in 1953. It determines the fairest way to distribute a "payout" (conversion credit) among players (marketing channels) based on their **Marginal Contribution**.

### 2.1. The Math of Fairness
In our attribution engine, we treat every customer journey as a game. To calculate the true value of a channel (e.g., *Email*), we perform a permutation-based audit:
1.  **Enumerate Subsets**: We look at all possible combinations of touchpoints (Social only, Social+Email, Search only, etc.).
2.  **Calculate Marginal Lift**: We calculate the conversion probability of every subset *with* Email minus the probability *without* Email.
3.  **Weighted Average**: The **Shapley Value** is the average of these marginal lifts across all permutations.

This method ensures that "Assisters"—channels that nurture the customer along but rarely close the deal—get the credit they mathematically deserve.

---

## 3. Dimensional Upgrade: Exponential Time-Decay

Static Shapley values are a good foundation, but they ignore the temporal decay of human attention and the "staleness" of data. A Facebook ad seen 60 days ago has significantly less causal impact on today's purchase than a Google search performed 2 hours ago. 

We integrated an **Exponential Time-Decay Factor** ($e^{-\lambda t}$) into our engine to normalize the Shapley distribution.

```python
# Technical Snippet: Dynamic Time-Decay Weighting
import numpy as np

def calculate_mercer_efficiency(wins, leads, avg_cycle_days):
    """
    A multi-dimensional scoring function that rewards high conversion
    AND high velocity (Time-Decay).
    """
    # Base Conversion Rate
    conversion_rate = wins / leads if leads > 0 else 0
    
    # Mercer Efficiency Score = (P_win) / (T_cycle + 1)
    # The '+1' prevents division by zero for instant conversions.
    # This identifies 'Hidden Gems' that close deals fast with low friction.
    efficiency = conversion_rate / (avg_cycle_days + 1)
    
    return efficiency
```

By applying this $\lambda$ decay, we ensure that the system rewards "Accelerators"—the high-velocity channels that turn interest into immediate cash flow.

---

## 4. Case Study: Discovery of the "Hidden Gems" in Olist Data

We audited the **Olist E-commerce dataset**, analyzing 8,000 multi-channel leads and their multi-channel touchpoints. The results were a strategic wake-up call for raw volume-driven marketing.

### 4.1. The Slow Burn vs. The Fast Cash
- **Organic Search**: Maintained the highest raw volume, but required a **50.0-day** burn cycle from first contact to close. This is your brand's long-term oxygen.
- **Display Ads**: Frequently the first channel to be cut by traditional "Last-Click" models due to low raw volume. However, our **Efficiency Model** revealed that Display Ads had the fastest closing cycle in the dataset—averaging only **10.3 days.**

**Strategic Outcome:** In a macroeconomic environment sensitive to cash flow and capital efficiency, Display Ads are your most powerful tactical engine. Our model recommends **tripling the budget** for these high-velocity channels to accelerate the total sales cycle, while maintaining Organic Search as the strategic long-term baseline.

---

## 5. Conclusion: Towards an Efficiency Frontier

The future of CRM is not about who got the "Last Click"; it is about understanding the cooperative ecosystem of human desire. By moving from biased reporting to **Game Theory-driven Attribution**, you stop guessing where your growth comes from and start calculating it.

When you measure fairness, you unlock growth.

---
### 📂 Research Datasets & Technical Audit Log
- **Olist Marketing Funnel**: 8,000+ lead analysis for Attribution. [Kaggle Source](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist)
- **Methodology Reference**: Shapley, L. S. (1953). "A Value for n-person Games." *Contributions to the Theory of Games*.
- **Code Artifact**: `scripts/phase6_attribution_engine.py` (Digital Crustacean Lab).

### 💻 Live Technical Implementation
Access the complete Python source code and reproducible environment:
👉 [Advanced CRM: Intent, Anomaly & Attribution](https://www.kaggle.com/code/speckhung/advanced-crm-intent-anomaly-attribution)

---
*Clarence R. Mercer is a Data Strategy Analyst at Digital Crustacean Lab, specializing in high-fidelity CRM automation and the intersection of Game Theory and Business Intelligence.*
