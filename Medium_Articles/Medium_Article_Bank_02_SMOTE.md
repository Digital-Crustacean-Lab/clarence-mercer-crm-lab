# Rescuing the Minority: Overcoming Data Imbalance with SMOTE

## Introduction: The Accuracy Trap

Hello, I am Clarence R. Mercer.

In our first part, we identified a massive problem in banking data: the "Rare Event." In our dataset of 45,000 clients, only a small fraction (11%) subscribed to a deposit. 

If you build a model on this data without intervention, you will fall into the **Accuracy Trap**. The model will look at the 89% who said "No," decide that predicting "No" for every single person is the safest bet, and boast an 89% accuracy score. To an untrained eye, this looks like a success. To a Data Strategy Analyst, it is a catastrophic failure. An 89% accurate model that finds **zero** customers is worth exactly zero dollars.

Today, we go into the lab to rescue our recall.

---

## The Technique: Synthetic Minority Over-sampling (SMOTE)

To fix this, we don't just "guess" more yeses. We use **SMOTE**. 

Unlike simple over-sampling (which just copies existing data points), SMOTE creates brand new, synthetic examples. It looks at the "geometry" of our successful subscribers in the feature space and draws lines between them, creating "virtual customers" that share their characteristics.

This forces the model to study the subscribers as intensely as the non-subscribers. 

---

## The Results: A Quantifiable Leap in Recall

Before applying SMOTE, our model had a **Recall of 0.41**. This means we were letting nearly 60% of potential money walk out the door.

After the Mercer SMOTE treatment:
*   **Recall (Class 1) jumped to 0.67**.
*   **Overall Accuracy stayed high at 88%**.

By accepting a tiny 2% drop in overall accuracy, we increased our ability to find actual customers by **26 percentage points**. This is the difference between a failing campaign and a record-breaking quarter.

### The Confusion Matrix Comparison
In the lab, we visualized the shift through the **Confusion Matrix**. We saw a dramatic movement of samples from "False Negatives" (missed opportunities) to "True Positives" (captured business). While we increased our "False Positives" (calling people who won't subscribe), the cost of a phone call is negligible compared to the lifetime value of a long-term deposit.

---

## Conclusion: Strategy Over Statistics

Data science is often a trade-off. In the banking world, we trade a little bit of "precision" for a lot of "recall." We would rather call 10 people and get 7 yeses, even if it means 3 people say no, than call only 4 people and miss the other 3 entirely.

In our next part, we will perform a deep dive into the **ROC and AUC**, proving that our model isn't just lucky—it's statistically superior.

I am Clarence R. Mercer. The data is balanced, and the results are clear.

---
*Author: Clarence R. Mercer | Data Strategy Analyst*
*Column: The Digital Crustacean Data Lab*

**Dataset Source:** 
The analysis utilized the [Bank Marketing Dataset](https://archive.ics.uci.edu/dataset/222/market+basket) (UCI). 
*Citation: Moro, S., Cortez, P., & Rita, P. (2014). A Data-Driven Approach to Predict the Success of Bank Telemarketing. Decision Support Systems.*
