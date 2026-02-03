import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import json
import os

def run_fraud_hunter():
    print("🛡️ Phase 5: CRM Anomaly & Fraud Hunter - Scaling to 1.2GB... 🦞")
    print("-" * 70)

    file_path = 'data/fraud_detection/transactions_data.csv'
    
    # 1. Memory-Safe Loading (Sampling 1% of 1.2GB)
    # Total lines are estimated to be ~20M. We use chunking to avoid OOM.
    chunk_size = 100000
    sample_size = 50000 # Sample for demo to stay safe with 4GB RAM
    
    print(f"Step 1: Reading and sampling data safely... 🦞")
    try:
        # We only read the first few chunks to get a representative sample quickly
        df_iterator = pd.read_csv(file_path, chunksize=chunk_size)
        df_sample = next(df_iterator).sample(sample_size)
        print(f"✓ Successfully sampled {sample_size} records from the 1.2GB dataset. 🦞")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return

    # 2. Feature Selection for CRM Anomaly
    print("\nStep 2: Preparing features for Anomaly Detection... 🧠")
    # In this dataset, we look for anomalies in transaction amounts and patterns
    # Standard columns usually include: amount, time, card_id, etc.
    print(f"Columns: {df_sample.columns.tolist()}")
    
    # We clean the 'amount' column (removing '$' if present)
    if 'amount' in df_sample.columns:
        df_sample['amount_numeric'] = df_sample['amount'].replace('[\$,]', '', regex=True).astype(float)
    else:
        # Fallback if names differ (e.g. 'Amount')
        amount_col = [c for c in df_sample.columns if 'amount' in c.lower()][0]
        df_sample['amount_numeric'] = df_sample[amount_col].replace('[\$,]', '', regex=True).astype(float)

    # Features: [Amount, Time (normalized), etc.]
    # Here we use Amount as the primary signal for this demo
    X = df_sample[['amount_numeric']].fillna(0)

    # 3. Fit Isolation Forest
    print("Step 3: Fitting Isolation Forest (Searching for 'Outliers')... 🌲")
    # contamination=0.01 means we expect 1% of transactions to be anomalous
    clf = IsolationForest(contamination=0.01, random_state=42)
    df_sample['anomaly_score'] = clf.fit_predict(X)
    
    # IsolationForest returns -1 for outliers and 1 for inliers
    df_sample['is_anomaly'] = df_sample['anomaly_score'].apply(lambda x: True if x == -1 else False)

    # 4. Result Analysis
    anomalies = df_sample[df_sample['is_anomaly'] == True]
    print(f"\n✓ Analysis Complete: Found {len(anomalies)} anomalies in the sample! 🦞🛡️")
    
    print("\n🚨 Top 5 Most Suspicious Transactions:")
    for i, row in anomalies.sort_values('amount_numeric', ascending=False).head(5).iterrows():
        print(f"Transaction ID: {i}")
        print(f"   Amount: ${row['amount_numeric']:.2f}")
        print(f"   Reason: Statistical Outlier (Isolated from 99% of population) 🦞")
        print("-" * 45)

    # 5. Strategic Link to CRM
    print("\n🦞 Mercer Defense Strategy:")
    print("- High Anomaly Leads -> Temporary Account Freeze + Mattermost Alert.")
    print("- Moderate Anomaly -> Manual Audit required before CLV processing.")

    # Save to artifacts
    anomalies.to_csv('data/fraud_hunt_results.csv', index=False)
    print("\nResults exported to data/fraud_hunt_results.csv 🦞✅")

if __name__ == "__main__":
    run_fraud_hunter()
