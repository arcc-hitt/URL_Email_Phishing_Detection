"""
Simplified URL service that only uses XGBoost model for better reliability
"""
import numpy as np
import gc
import logging
from app.utils.feature_extraction import extract_url_features
from sklearn.preprocessing import MinMaxScaler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleURLService:
    _xgboost_model = None
    _models_loaded = False
    
    def __init__(self):
        # Threshold for determining phishing (adjusted for single model)
        self.xgboost_phishing_threshold = 0.7  # Lower threshold since we only use XGBoost

        # Create scaler for consistent score range
        self.xgboost_scaler = MinMaxScaler(feature_range=(0, 1))
        self.xgboost_scaler.fit([[0], [1]])  # XGBoost output is already in [0, 1]
    
    @classmethod
    def preload_models(cls):
        """Preload XGBoost model only"""
        if not cls._models_loaded:
            try:
                logger.info("Starting XGBoost model preloading...")
                
                # Load XGBoost model
                logger.info("Loading XGBoost model...")
                from app.models.xgboost_model import XGBoostModel
                cls._xgboost_model = XGBoostModel()
                logger.info("XGBoost model loaded successfully")
                
                cls._models_loaded = True
                logger.info("XGBoost model preloading completed")
                
                # Force garbage collection
                gc.collect()
                
            except Exception as e:
                logger.error(f"Error preloading XGBoost model: {e}")
                raise e
    
    @classmethod
    def get_xgboost_model(cls):
        if cls._xgboost_model is None:
            cls.preload_models()
        return cls._xgboost_model
    
    @classmethod
    def models_ready(cls):
        """Check if XGBoost model is loaded and ready"""
        return cls._models_loaded and cls._xgboost_model is not None

    def analyze_url(self, url):
        try:
            # Check if model is ready
            if not self.models_ready():
                raise Exception("XGBoost model is not loaded yet. Please try again in a moment.")
            
            logger.info(f"Analyzing URL with XGBoost only: {url[:50]}...")
            
            # Step 1: Extract features from the URL
            features = extract_url_features(url)
            logger.info("Features extracted successfully")
            
            # Step 2: Get XGBoost model prediction (phishing probability)
            xgboost_model = self.get_xgboost_model()
            xgboost_prediction = xgboost_model.predict(features)
            xgboost_phishing_score = xgboost_prediction[0][1]  # Probability that URL is phishing
            logger.info(f"XGBoost prediction completed: {xgboost_phishing_score}")
            
            # Normalize XGBoost score
            xgboost_score_normalized = self.xgboost_scaler.transform([[xgboost_phishing_score]])[0][0]

            # Step 3: Determine if phishing based on XGBoost only
            is_phishing = xgboost_phishing_score >= self.xgboost_phishing_threshold

            # Step 4: Clean up memory
            gc.collect()

            result = {
                "is_phishing": bool(is_phishing),
                "xgboost_score": float(xgboost_score_normalized),
                "autoencoder_score": 0.0,  # Not used
                "original_xgboost_score": float(xgboost_phishing_score),
                "original_autoencoder_score": 0.0,  # Not used
                "autoencoder_fallback": True,  # Always true for this service
                "model_type": "xgboost_only"
            }
            
            logger.info(f"XGBoost-only analysis completed: is_phishing={is_phishing}")
            return result
            
        except Exception as e:
            logger.error(f"Error in analyze_url: {e}")
            # Clean up memory on error
            gc.collect()
            raise e