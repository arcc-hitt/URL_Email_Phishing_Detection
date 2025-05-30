import numpy as np
from app.models.xgboost_model import XGBoostModel
from app.models.url_autoencoder_model import URLAutoencoderModel
from app.utils.feature_extraction import extract_url_features
from sklearn.preprocessing import MinMaxScaler

class URLService:
    def __init__(self):
        self.xgboost_model = XGBoostModel()
        self.autoencoder_model = URLAutoencoderModel()
        
        # Thresholds for determining phishing
        self.xgboost_phishing_threshold = 0.9  # XGBoost score threshold for phishing
        self.autoencoder_anomaly_threshold = 50  # Autoencoder anomaly threshold

        # Create scalers for consistent score range
        self.xgboost_scaler = MinMaxScaler(feature_range=(0, 1))
        self.xgboost_scaler.fit([[0], [1]])  # XGBoost output is already in [0, 1]
        self.autoencoder_scaler = MinMaxScaler(feature_range=(0, 1))
        self.autoencoder_scaler.fit([[0], [100]])  # Assuming Autoencoder scores range from 0 to 100

    def analyze_url(self, url):
        # Step 1: Extract features from the URL
        features = extract_url_features(url)
        
        # Step 2: Get XGBoost model prediction (phishing probability)
        xgboost_prediction = self.xgboost_model.predict(features)
        xgboost_phishing_score = xgboost_prediction[0][1]  # Probability that URL is phishing
        
        # Normalize XGBoost score
        xgboost_score_normalized = self.xgboost_scaler.transform([[xgboost_phishing_score]])[0][0]

        # Step 3: Get Autoencoder model anomaly score
        autoencoder_score = self.autoencoder_model.predict(features)
        if isinstance(autoencoder_score, (list, np.ndarray)):
            autoencoder_score = autoencoder_score[0]  # Handle array output
        
        # Normalize Autoencoder score
        autoencoder_score_normalized = self.autoencoder_scaler.transform([[autoencoder_score]])[0][0]

        # Step 4: Determine if phishing based on original thresholds
        is_phishing = (
            xgboost_phishing_score >= self.xgboost_phishing_threshold and 
            autoencoder_score >= self.autoencoder_anomaly_threshold
        )

        # Step 5: Return results with normalized scores
        return {
            "is_phishing": bool(is_phishing),
            "xgboost_score": float(xgboost_score_normalized),
            "autoencoder_score": float(autoencoder_score_normalized),
            "original_xgboost_score": float(xgboost_phishing_score),
            "original_autoencoder_score": float(autoencoder_score)
        }
