import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter
from lifetimes.utils import calibration_and_holdout_data
import os

def run_offline_backtest():
    print("Step 1: Loading all data... 🦞")
    file_path = 'data/Online Retail.xlsx'
    
    # Load all data but minimize columns to speed up
    df = pd.read_excel(file_path, usecols=['CustomerID', 'InvoiceDate'])
    df = df[df['CustomerID'].notna()]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']).dt.date
    
    max_date = df['InvoiceDate'].max()
    end_date_train = max_date - pd.Timedelta(days=90) 
    
    print(f"Total rows: {len(df)}")
    print(f"Calibration Period End: {end_date_train} 🦞")

    summary_holdout = calibration_and_holdout_data(
        df, 
        customer_id_col='CustomerID', 
        datetime_col='InvoiceDate',
        calibration_period_end=end_date_train,
        observation_period_end=max_date
    )
    
    # Remove zero vectors if any
    summary_holdout = summary_holdout[summary_holdout['T_cal'] > 0]

    print("Step 2: Training model (BG/NBD)... 🌲")
    bgf = BetaGeoFitter(penalizer_coef=0.05)
    bgf.fit(summary_holdout['frequency_cal'], summary_holdout['recency_cal'], summary_holdout['T_cal'])

    print("Step 3: Prediction & Audit... 🔮")
    t = 90
    summary_holdout['predicted'] = bgf.predict(
        t, summary_holdout['frequency_cal'], summary_holdout['recency_cal'], summary_holdout['T_cal']
    )

    actual = summary_holdout['frequency_holdout']
    predicted = summary_holdout['predicted']
    mae = np.mean(np.abs(actual - predicted))
    correlation = np.corrcoef(actual, predicted)[0, 1]

    print("\n" + "="*40)
    print("📊 BACKTESTING PERFORMANCE REPORT:")
    print(f"- MAE: {mae:.4f}")
    print(f"- Correlation: {correlation:.4f} 🦞")
    print("="*40)
    
    if correlation > 0.6:
        print("\n✅ FINAL VERDICT: REAL ENGINE.")
    else:
        print("\n❌ FINAL VERDICT: PAPER TIGER (Needs more features).")

if __name__ == "__main__":
    run_offline_backtest()
