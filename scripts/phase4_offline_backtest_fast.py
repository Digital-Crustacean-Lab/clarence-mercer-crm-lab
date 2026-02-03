import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter
from lifetimes.utils import calibration_and_holdout_data
import os

def run_offline_backtest():
    print("Step 1: Loading small sample... 🦞")
    file_path = 'data/Online Retail.xlsx'
    
    # Load only first 50,000 rows to speed up Excel parsing
    df = pd.read_excel(file_path, nrows=50000)
    df = df[df['CustomerID'].notna()]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']).dt.date
    
    max_date = df['InvoiceDate'].max()
    end_date_train = max_date - pd.Timedelta(days=60) 
    
    print(f"Calibration Period End: {end_date_train} 🦞")

    summary_holdout = calibration_and_holdout_data(
        df, 
        customer_id_col='CustomerID', 
        datetime_col='InvoiceDate',
        calibration_period_end=end_date_train,
        observation_period_end=max_date
    )

    print("Step 2: Training model... 🌲")
    bgf = BetaGeoFitter(penalizer_coef=0.01)
    bgf.fit(summary_holdout['frequency_cal'], summary_holdout['recency_cal'], summary_holdout['T_cal'])

    print("Step 3: Evaluating... 🔮")
    t = 60
    summary_holdout['predicted_purchases'] = bgf.predict(
        t, summary_holdout['frequency_cal'], summary_holdout['recency_cal'], summary_holdout['T_cal']
    )

    actual = summary_holdout['frequency_holdout']
    predicted = summary_holdout['predicted_purchases']
    mae = np.mean(np.abs(actual - predicted))
    correlation = np.corrcoef(actual, predicted)[0, 1]

    print("\n📊 BACKTEST REPORT (Sample):")
    print(f"- MAE: {mae:.4f}")
    print(f"- Correlation: {correlation:.4f} 🦞")
    
    if correlation > 0.4:
        print("\n✅ VERDICT: REAL ENGINE.")
    else:
        print("\n❌ VERDICT: PAPER TIGER.")

if __name__ == "__main__":
    run_offline_backtest()
