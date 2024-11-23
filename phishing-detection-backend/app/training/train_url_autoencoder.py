import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

# Ensure the script detects the project root dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# Dynamically set dataset and model paths relative to the project root
dataset_path = os.path.join(project_root, 'app', 'data', 'Phishing_URL.csv')
model_path = os.path.join(project_root, 'app', 'models', 'saved', 'url_autoencoder_model.h5')

# Load and prepare the phishing dataset
data = pd.read_csv(dataset_path)

# Extract features, excluding 'class' label column
X = data.drop(columns=['Index', 'class'])

# Normalize the data for autoencoder training
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split into train and test sets
X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)

# Define autoencoder parameters
input_dim = X.shape[1]  # Number of features
encoding_dim = 14       # Size of encoding layer

# Define the autoencoder architecture
input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='sigmoid')(encoded)

# Compile the autoencoder
autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

# Train the autoencoder
autoencoder.fit(X_train, X_train, epochs=50, batch_size=32, shuffle=True, validation_data=(X_test, X_test))

# Save the model to a file
autoencoder.save(model_path)
print(f"Autoencoder model saved to {model_path}")
