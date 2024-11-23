import os
import joblib
import lightgbm as lgb

class LightGBMModel:
    def __init__(self):
        # Automatically detect the directory of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the relative path to the model file
        model_path = os.path.join(base_dir, 'saved', 'lightgbm_model.pkl')
        self.model = joblib.load(model_path)

    def predict(self, features):
        return self.model.predict_proba([features])