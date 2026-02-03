import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter, GammaGammaFitter
import os

def run_clv_monetary_module():
    print("💰 Phase 4: CLV Mastery - Implementing the Gamma-Gamma Monetary Submodel 🦞")
    print("-" * 75)

    # 1. Load the summary results from the previous BG/NBD step
    # We need: frequency, monetary_value (average order value)
    # Note: Gamma-Gamma model requires frequency > 0 (returning customers only)
    
    # Using the synthetic dataset for consistency in the masterclass
    data = {
        'customer_id': [1, 2, 3, 4, 5],
        'frequency': [10, 1, 5, 0, 20],
        'recency': [200, 10, 150, 0, 350],
        'T': [250, 300, 300, 400, 400],
        'monetary_value': [120.5, 45.0, 85.2, 0, 155.8] # Average profit/value per transaction
    }
    rfm = pd.DataFrame(data)
    
    # Filter for customers with at least one repeat purchase (frequency > 0)
    returning_customers = rfm[rfm['frequency'] > 0].copy()
    
    print(f"Step 1: Identifying {len(returning_customers)} returning customers for value estimation... 🦞")

    # 2. Fit Gamma-Gamma Model
    # Use a larger sample or add penalizer to help convergence
    print("Step 2: Fitting Gamma-Gamma Submodel... 📈")
    ggf = GammaGammaFitter(penalizer_coef=0.01) # Added penalizer to ensure convergence
    ggf.fit(returning_customers['frequency'], returning_customers['monetary_value'])

    # 3. Predict Conditional Expected Average Profit
    # This calculates the expected average value of transactions in the future.
    returning_customers['expected_avg_profit'] = ggf.conditional_expected_average_profit(
        returning_customers['frequency'],
        returning_customers['monetary_value']
    )

    # 4. Calculate Final CLV (Combined BG/NBD + Gamma-Gamma)
    # We re-fit BG/NBD to get the frequency component
    bgf = BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(rfm['frequency'], rfm['recency'], rfm['T'])
    
    # Predict CLV for the next 12 months (discount_rate handles the time-value of money)
    returning_customers['clv_12m'] = ggf.customer_lifetime_value(
        bgf,
        returning_customers['frequency'],
        returning_customers['recency'],
        returning_customers['T'],
        returning_customers['monetary_value'],
        time=12, # 12 months
        discount_rate=0.01 # monthly discount rate
    )

    print("\n✓ Final CLV Prediction Results (12-Month Forecast):")
    for i, row in returning_customers.sort_values('clv_12m', ascending=False).iterrows():
        print(f"Customer {int(row['customer_id'])}:")
        print(f"   Historical Avg Value: ${row['monetary_value']:.2f}")
        print(f"   Expected Future Avg: ${row['expected_avg_profit']:.2f}")
        print(f"   Total Predicted 12M Value: ${row['clv_12m']:.2f} 💰 🦞")
        print("-" * 45)

    # 5. Strategic Conclusion
    print("\n🦞 Mercer Wealth Insight:")
    print("We have now moved from predicting 'Rhythms' to predicting 'Revenue'.")
    print("A customer with high frequency but low monetary value might be less valuable than")
    print("a low-frequency customer with massive average order value. CLV balances both.")

    # Save to lab artifacts
    returning_customers.to_csv('data/clv_final_monetary_results.csv', index=False)
    print("\nFinal results exported to data/clv_final_monetary_results.csv 🦞✅")

if __name__ == "__main__":
    run_clv_monetary_module()
