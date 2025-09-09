import numpy as np
import gc
import logging
from app.utils.feature_extraction import extract_url_features
from sklearn.preprocessing import MinMaxScaler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLService:
    _xgboost_model = None
    _autoencoder_model = None
    _models_loaded = False
    
    def __init__(self):
        # Thresholds for determining phishing
        self.xgboost_phishing_threshold = 0.9  # XGBoost score threshold for phishing
        self.autoencoder_anomaly_threshold = 50  # Autoencoder anomaly threshold

        # Create scalers for consistent score range
        self.xgboost_scaler = MinMaxScaler(feature_range=(0, 1))
        self.xgboost_scaler.fit([[0], [1]])  # XGBoost output is already in [0, 1]
        self.autoencoder_scaler = MinMaxScaler(feature_range=(0, 1))
        self.autoencoder_scaler.fit([[0], [100]])  # Assuming Autoencoder scores range from 0 to 100
    
    @classmethod
    def preload_models(cls):
        """Preload models during app startup"""
        if not cls._models_loaded:
            try:
                logger.info("Starting model preloading...")
                
                # Load XGBoost model
                logger.info("Loading XGBoost model...")
                from app.models.xgboost_model import XGBoostModel
                cls._xgboost_model = XGBoostModel()
                logger.info("XGBoost model loaded successfully")
                
                # Try to load Autoencoder model, but don't fail if it doesn't work
                try:
                    logger.info("Loading Autoencoder model...")
                    # Import TensorFlow config first to ensure proper configuration
                    from app.tf_config import tf
                    from app.models.url_autoencoder_model import URLAutoencoderModel
                    cls._autoencoder_model = URLAutoencoderModel()
                    logger.info("Autoencoder model loaded successfully")
                except Exception as ae_error:
                    logger.warning(f"Autoencoder model loading failed, will use fallback: {ae_error}")
                    cls._autoencoder_model = None
                
                cls._models_loaded = True
                logger.info("Model preloading completed")
                
                # Force garbage collection
                gc.collect()
                
            except Exception as e:
                logger.error(f"Error preloading models: {e}")
                # Don't raise the error - allow the service to start with partial functionality
                cls._models_loaded = True  # Mark as loaded even if some models failed
    
    @classmethod
    def get_xgboost_model(cls):
        if cls._xgboost_model is None:
            cls.preload_models()
        return cls._xgboost_model
    
    @classmethod
    def get_autoencoder_model(cls):
        if cls._autoencoder_model is None:
            cls.preload_models()
        return cls._autoencoder_model
    
    @classmethod
    def models_ready(cls):
        """Check if models are loaded and ready"""
        return cls._models_loaded and cls._xgboost_model is not None

    def analyze_url(self, url):
        try:
            # Check if models are ready
            if not self.models_ready():
                raise Exception("Models are not loaded yet. Please try again in a moment.")
            
            logger.info(f"Analyzing URL: {url[:50]}...")  # Log first 50 chars for privacy
            
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

            # Step 3: Get Autoencoder model anomaly score with fallback
            autoencoder_score = 25.0  # Default fallback score
            autoencoder_score_normalized = 0.25
            autoencoder_fallback = True
            
            # Try to use autoencoder if available
            if self._autoencoder_model is not None:
                try:
                    autoencoder_model = self.get_autoencoder_model()
                    autoencoder_score = autoencoder_model.predict(features)
                    if isinstance(autoencoder_score, (list, np.ndarray)):
                        autoencoder_score = autoencoder_score[0]  # Handle array output
                    logger.info(f"Autoencoder prediction completed: {autoencoder_score}")
                    
                    # Normalize Autoencoder score
                    autoencoder_score_normalized = self.autoencoder_scaler.transform([[autoencoder_score]])[0][0]
                    autoencoder_fallback = False
                    
                except Exception as ae_error:
                    logger.warning(f"Autoencoder prediction failed, using fallback: {ae_error}")
                    # Keep fallback values
            else:
                logger.info("Autoencoder model not available, using fallback")

            # Step 4: Determine if phishing based on available models
            if autoencoder_fallback:
                # Use only XGBoost with adjusted threshold
                is_phishing = xgboost_phishing_score >= 0.7  # Lower threshold when autoencoder not available
            else:
                # Use both models with original thresholds
                is_phishing = (
                    xgboost_phishing_score >= self.xgboost_phishing_threshold and 
                    autoencoder_score >= self.autoencoder_anomaly_threshold
                )

            # Step 5: Clean up memory
            gc.collect()

            result = {
                "is_phishing": bool(is_phishing),
                "xgboost_score": float(xgboost_score_normalized),
                "autoencoder_score": float(autoencoder_score_normalized),
                "original_xgboost_score": float(xgboost_phishing_score),
                "original_autoencoder_score": float(autoencoder_score),
                "autoencoder_fallback": autoencoder_fallback
            }
            
            logger.info(f"Analysis completed: is_phishing={is_phishing}")
            return result
            
        except Exception as e:
            logger.error(f"Error in analyze_url: {e}")
            # Clean up memory on error
            gc.collect()
            raise e
