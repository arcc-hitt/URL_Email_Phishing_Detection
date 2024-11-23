import lightgbm as lgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import sys
import os
import joblib 

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.utils.feature_extraction import extract_email_features

# Ensure the script detects the project root dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# Dynamically set dataset and model paths relative to the project root
dataset_path = os.path.join(project_root, 'app', 'data', 'CEAS_08.csv')
model_path = os.path.join(project_root, 'app', 'models', 'saved', 'lightgbm_model.pkl')

# Load data
data = pd.read_csv(dataset_path)

# Prepare data
data['features'] = data.apply(extract_email_features, axis=1)
X = list(data['features'])
y = data['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train LightGBM
model = lgb.LGBMClassifier(objective='binary', metric='binary_logloss')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("LightGBM Model Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, model_path)