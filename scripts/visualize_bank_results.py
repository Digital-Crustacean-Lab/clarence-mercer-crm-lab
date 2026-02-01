import pandas as pd
import psycopg2
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# Load DB config
CONFIG_PATH = os.path.expanduser("~/.config/clawdbot/db-config.json")
with open(CONFIG_PATH, 'r') as f:
    db_config = json.load(f)["databases"][0]

def visualize_confusion_matrix():
    print("Fetching data for visualization... 🦞")
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        database=db_config["database"],
        user=db_config["user"],
        password=db_config["password"]
    )
    
    query = "SELECT * FROM bank_marketing"
    df = pd.read_sql(query, conn)
    conn.close()
    
    if 'id' in df.columns:
        df = df.drop('id', axis=1)
    
    # Preprocessing
    categorical_cols = df.select_dtypes(include=['object']).columns
    le = LabelEncoder()
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col])
    
    X = df.drop('y', axis=1)
    y = df['y']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Apply SMOTE
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_train, y_train)
    
    # Train Optimized Model
    print("Training model for matrix generation... 🦞")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_res, y_res)
    
    y_pred = model.predict(X_test)
    
    # Generate Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Plotting
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['No', 'Yes'], yticklabels=['No', 'Yes'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix: Bank Term Deposit Prediction (Optimized)')
    
    # Save the plot
    output_path = 'data/bank_confusion_matrix.png'
    plt.savefig(output_path)
    print(f"✓ Confusion Matrix saved to {output_path} 🦞")

if __name__ == "__main__":
    visualize_confusion_matrix()
