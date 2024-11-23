import numpy as np
import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.utils.feature_extraction import extract_email_features

# Ensure the script detects the project root dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# Dynamically set dataset and model paths relative to the project root
dataset_path = os.path.join(project_root, 'app', 'data', 'CEAS_08.csv')
model_path = os.path.join(project_root, 'app', 'models', 'saved', 'email_autoencoder_model.h5')

# Load data
data = pd.read_csv(dataset_path)

# Prepare data
data['features'] = data.apply(extract_email_features, axis=1)
X = np.array(list(data['features']))

# Scale data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)

# Define the autoencoder model
input_dim = X.shape[1]
encoding_dim = 10

input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='sigmoid')(encoded)

autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# Train the autoencoder
autoencoder.fit(X_train, X_train, epochs=50, batch_size=32, shuffle=True, validation_data=(X_test, X_test))

# Step 7: Save the trained autoencoder model
autoencoder.save(model_path)
print(f"Autoencoder model saved to {model_path}")
