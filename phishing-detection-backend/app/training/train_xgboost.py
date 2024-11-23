import os
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Ensure the script detects the project root dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# Dynamically set dataset and model paths relative to the project root
dataset_path = os.path.join(project_root, 'app', 'data', 'Phishing_URL.csv')
model_path = os.path.join(project_root, 'app', 'models', 'saved', 'xgboost_model.json')

# Load the phishing dataset
data = pd.read_csv(dataset_path)

# Separate features and target
X = data.drop(columns=['Index', 'class'])
y = data['class']

# Encode labels if necessary (for classification)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train an XGBoost classifier
model = xgb.XGBClassifier(
    objective='binary:logistic',
    eval_metric='logloss',
    use_label_encoder=False
)
model.fit(X_train, y_train)

# Test the model and print accuracy
y_pred = model.predict(X_test)
print("XGBoost Model Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the model to a file
model.save_model(model_path)


