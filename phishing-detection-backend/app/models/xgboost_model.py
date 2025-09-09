import os
import logging
import xgboost as xgb
import numpy as np

logger = logging.getLogger(__name__)

class XGBoostModel:
    def __init__(self):
        try:
            # Automatically detect the directory of the current script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the relative path to the model file
            model_path = os.path.join(base_dir, 'saved', 'xgboost_model.json')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"XGBoost model file not found at: {model_path}")
            
            logger.info(f"Loading XGBoost model from: {model_path}")
            self.model = xgb.XGBClassifier()
            self.model.load_model(model_path)
            logger.info("XGBoost model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load XGBoost model: {e}")
            raise e

    def predict(self, features):
        try:
            features = np.array(features, dtype=np.float32).reshape(1, -1)
            
            if features.shape[1] == 0:
                raise ValueError("No features provided for prediction")
            
            prediction = self.model.predict_proba(features)
            return prediction
            
        except Exception as e:
            logger.error(f"XGBoost prediction failed: {e}")
            raise e

