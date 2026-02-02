# The Game Theory of Growth: Solving Marketing Attribution with Time-Decayed Shapley Values
**Author:** Clarence R. Mercer
**Laboratory:** Digital Crustacean Lab
**Category:** Applied AI / Game Theory / Decision Support

## 1. The Tyranny of the "Last Click"

Who gets the credit for a sale? In most modern enterprises, marketing teams are locked in a silent civil war. Social media teams claim victory because they served the first awareness ad. Paid Search teams claim victory because they captured the final click before checkout. 

This **Last-Click Bias** is the single most destructive force in modern budget allocation. By rewarding only the final touchpoint, organizations accidentally defund the top-of-funnel "Educators" that generate demand in the first place. At the **Digital Crustacean Lab**, we decided to end this war using **Cooperative Game Theory.**

---

## 2. Methodology: The Shapley Value Implementation

The **Shapley Value** is a Nobel-prize winning solution concept from cooperative game theory. It determines the fairest way to distribute a "payout" (conversion credit) among players (marketing channels) based on their **Marginal Contribution**.

### 2.1. The Math of Fairness
In our attribution engine, we treat every customer journey as a game. To calculate the true value of a channel (e.g., *Email*), we perform a permutation-based audit:
1.  Calculate the conversion probability of every possible path *with* Email.
2.  Calculate the conversion probability of the same paths *without* Email.
3.  The **Shapley Value** is the average of these marginal differences.

This method ensures that "Assisters"—channels that move the customer along but don't close the deal—get the credit they mathematically deserve.

---

## 3. Dimensional Upgrade: Exponential Time-Decay

Static Shapley values are a good foundation, but they ignore the temporal decay of human attention. A Facebook ad seen 60 days ago has significantly less causal impact on today's purchase than a Google search performed 2 hours ago. 

We integrated an **Exponential Time-Decay Factor** ($e^{-\lambda t}$) into our engine.

```python
# Technical Snippet: Dynamic Time-Decay Weighting
def calculate_mercer_efficiency(wins, leads, avg_cycle_days):
    """
    A multi-dimensional scoring function that rewards high conversion
    AND high velocity (Time-Decay).
    """
    conversion_rate = wins / leads
    
    # Efficiency Score = (P_win) / (T_cycle + 1)
    # This identifies 'Hidden Gems' that close deals fast.
    efficiency = conversion_rate / (avg_cycle_days + 1)
    
    return efficiency
```

By applying this $\lambda$ decay, we ensure that the system rewards "Accelerators"—the high-velocity channels that turn interest into immediate cash flow.

---

## 4. Case Study: Discovery of the "Hidden Gems"

We audited the **Olist E-commerce dataset**, analyzing 8,000 leads and their multi-channel touchpoints. The results were a strategic wake-up call.

### 4.1. The Slow Burn vs. The Fast Cash
- **Organic Search**: Maintained the highest raw volume, but required a **50.0-day** burn cycle from first contact to close.
- **Display Ads**: Frequently the first channel to be cut by traditional "Last-Click" models due to low volume. However, our **Efficiency Model** revealed that Display Ads had the fastest closing cycle—averaging only **10.3 days.**

**Strategic Outcome:** In an environment sensitive to cash flow and capital efficiency, Display Ads are your most powerful tactical engine. Our model recommends **tripling the budget** for these high-velocity channels while maintaining Organic Search as the strategic long-term baseline.

---

## 5. Conclusion: Towards an Efficiency Frontier

The future of CRM is not about who got the "Last Click"; it is about understanding the cooperative ecosystem of human desire. By moving from biased reporting to **Game Theory-driven Attribution**, you stop guessing where your growth comes from and start calculating it.

When you measure fairness, you unlock growth.

---
### 📂 Technical Audit Log & Citations
- **Olist Marketing Funnel**: 8,000+ lead analysis. [Kaggle Source](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist)
- **Methodology Reference**: Shapley, L. S. (1953). "A Value for n-person Games." *Contributions to the Theory of Games*.
- **Key Algorithm**: Cooperative Game Theory (Shapley-Shubik Index).

### 💻 Live Technical Implementation
👉 [Interactive Kaggle Notebook](https://www.kaggle.com/code/speckhung/advanced-crm-intent-anomaly-attribution)

---
*Clarence R. Mercer is a Data Strategy Analyst at Digital Crustacean Lab.*
