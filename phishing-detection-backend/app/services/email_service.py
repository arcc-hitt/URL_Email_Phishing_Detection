import joblib
import numpy as np
from models.email_autoencoder_model import EmailAutoencoderModel
from models.lightgbm_model import LightGBMModel
from utils.feature_extraction import extract_email_features
from sklearn.preprocessing import MinMaxScaler

class EmailService:
    def __init__(self):
        self.lightgbm_model = LightGBMModel()
        self.autoencoder_model = EmailAutoencoderModel()
        
        # Thresholds for determining phishing
        self.lightgbm_phishing_threshold = 0.005
        self.autoencoder_anomaly_threshold = 485

        # Create a scaler for consistent score range
        self.autoencoder_scaler = MinMaxScaler(feature_range=(0, 1))
        self.autoencoder_scaler.fit([[0], [1000]])  # Assuming typical Autoencoder scores range from 0 to 1000
        self.lightgbm_scaler = MinMaxScaler(feature_range=(0, 1))
        self.lightgbm_scaler.fit([[0], [1]])  # LightGBM output is a probability in [0, 1]

    def analyze_email(self, email):
        # Extract features from email
        features = extract_email_features(email)
        
        # Step 1: LightGBM Model Prediction
        lightgbm_prediction = self.lightgbm_model.predict(features)
        lightgbm_phishing_score = lightgbm_prediction[0][1]
        
        # Normalize LightGBM score
        lightgbm_score_normalized = self.lightgbm_scaler.transform([[lightgbm_phishing_score]])[0][0]

        # Step 2: Autoencoder Model Anomaly Score
        autoencoder_score = self.autoencoder_model.predict(features)
        if isinstance(autoencoder_score, (list, np.ndarray)):
            autoencoder_score = autoencoder_score[0]
        
        # Normalize Autoencoder score
        autoencoder_score_normalized = self.autoencoder_scaler.transform([[autoencoder_score]])[0][0]

        # Step 3: Determine phishing based on original thresholds
        is_phishing = (
            lightgbm_phishing_score >= self.lightgbm_phishing_threshold and 
            autoencoder_score >= self.autoencoder_anomaly_threshold
        )

        # Step 4: Return results with normalized scores
        return {
            "is_phishing": bool(is_phishing),
            "lightgbm_score": float(lightgbm_score_normalized),
            "autoencoder_score": float(autoencoder_score_normalized),
            "original_lightgbm_score": float(lightgbm_phishing_score),
            "original_autoencoder_score": float(autoencoder_score)
        }
