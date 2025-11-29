import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Define column names for NSL-KDD
COL_NAMES = ["duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label", "difficulty"]

def load_and_preprocess(file_path, train=True):
    # 1. Load Data
    df = pd.read_csv(file_path, header=None, names=COL_NAMES)
    
    # 2. Map 'normal' -> 0, everything else -> 1
    df['label'] = df['label'].apply(lambda x: 0 if x == 'normal' else 1)
    
    # Separate features and target
    X = df.drop(['label', 'difficulty'], axis=1)
    y = df['label']

    # 3. Encoding
    cols_to_encode = ['protocol_type', 'service', 'flag']
    
    # Create models folder if it doesn't exist
    # We need to find the project root to save models in the right place
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '../../'))
    model_dir = os.path.join(project_root, "models")
    os.makedirs(model_dir, exist_ok=True)
    
    if train:
        for col in cols_to_encode:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            joblib.dump(le, os.path.join(model_dir, f"{col}_encoder.pkl"))
    else:
        for col in cols_to_encode:
            encoder_path = os.path.join(model_dir, f"{col}_encoder.pkl")
            if os.path.exists(encoder_path):
                le = joblib.load(encoder_path)
                # Handle unknown labels
                X[col] = X[col].apply(lambda x: x if x in le.classes_ else -1)
                mask = X[col] != -1
                X.loc[mask, col] = le.transform(X.loc[mask, col])
            else:
                 # Fallback if encoder missing (shouldn't happen in training)
                 X[col] = 0

    return X, y