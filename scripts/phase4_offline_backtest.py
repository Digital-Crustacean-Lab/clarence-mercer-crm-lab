import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter
from lifetimes.utils import calibration_and_holdout_data
import os

def run_offline_backtest():
    print("🧪 Supplement 4 Add-on: CLV Offline Backtesting (Hold-out Validation) 🦞")
    print("Testing if our model is a 'Real Engine' or a 'Paper Tiger'...")
    print("-" * 75)

    # 1. Load Data
    # Using the online retail dataset for a rich time-series backtest
    file_path = 'data/Online Retail.xlsx'
    if not os.path.exists(file_path):
        print("⚠️ Retail dataset not found. Please ensure 'Online Retail.xlsx' exists in /data.")
        return

    print("Step 1: Loading and preparing time-series data... 🦞")
    df = pd.read_excel(file_path)
    df = df[df['CustomerID'].notna()]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']).dt.date
    
    # 2. Define Time Windows for Backtesting
    # We will train on the first 9 months and test on the last 3 months
    max_date = df['InvoiceDate'].max()
    end_date_train = max_date - pd.Timedelta(days=90) # Hold out last 90 days
    
    print(f"Calibration Period End: {end_date_train}")
    print(f"Observation (Hold-out) Period End: {max_date} 🦞")

    # 3. Create Calibration and Holdout Summary
    print("\nStep 2: Splitting data into Calibration (Train) and Holdout (Test)... ✂️")
    summary_holdout = calibration_and_holdout_data(
        df, 
        customer_id_col='CustomerID', 
        datetime_col='InvoiceDate',
        calibration_period_end=end_date_train,
        observation_period_end=max_date
    )

    # 4. Fit Model on Calibration Period only
    print("Step 3: Training BG/NBD Model on the Calibration Period... 🌲")
    bgf = BetaGeoFitter(penalizer_coef=0.01)
    bgf.fit(summary_holdout['frequency_cal'], summary_holdout['recency_cal'], summary_holdout['T_cal'])

    # 5. Predict for the Holdout Period
    print("Step 4: Predicting purchases for the hidden Holdout Period... 🔮")
    t = 90 # days
    summary_holdout['predicted_purchases'] = bgf.predict(
        t, 
        summary_holdout['frequency_cal'], 
        summary_holdout['recency_cal'], 
        summary_holdout['T_cal']
    )

    # 6. Evaluation Metrics
    # Comparison: predicted_purchases vs frequency_holdout (actual)
    actual = summary_holdout['frequency_holdout']
    predicted = summary_holdout['predicted_purchases']
    
    mae = np.mean(np.abs(actual - predicted))
    correlation = np.corrcoef(actual, predicted)[0, 1]

    print("\n" + "="*50)
    print("📊 BACKTESTING PERFORMANCE REPORT:")
    print(f"- Mean Absolute Error (MAE): {mae:.4f}")
    print(f"- Prediction Correlation:    {correlation:.4f} 🦞")
    print("="*50)

    # Breakdown by segment
    print("\n🔍 Segmented Audit (Sample Customers):")
    sample = summary_holdout.sample(5, random_state=42)
    for i, row in sample.iterrows():
        print(f"Customer {int(i)}:")
        print(f"   Actual Purchases (Holdout):    {int(row['frequency_holdout'])}")
        print(f"   Predicted Purchases (Holdout): {row['predicted_purchases']:.2f}")
        diff = abs(row['frequency_holdout'] - row['predicted_purchases'])
        print(f"   Accuracy: {'✅ HIGH' if diff < 0.5 else '⚠️ MEDIUM' if diff < 1.5 else '❌ LOW'} 🦞")
        print("-" * 40)

    # 7. Final Verdict
    print("\n🦞 Mercer Forensic Verdict:")
    if correlation > 0.7:
        print("Model is a REAL ENGINE. Strong predictive correlation detected.")
    elif correlation > 0.4:
        print("Model is USABLE but needs refinement. Moderate correlation.")
    else:
        print("Model is a PAPER TIGER. Low predictive power on this dataset.")

    # Save artifact
    summary_holdout.to_csv('data/clv_backtest_results.csv')
    print("\nFull backtest logs saved to data/clv_backtest_results.csv 🦞✅")

if __name__ == "__main__":
    run_offline_backtest()
