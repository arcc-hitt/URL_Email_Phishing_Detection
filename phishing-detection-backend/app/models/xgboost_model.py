import os
import xgboost as xgb
import numpy as np

class XGBoostModel:
    def __init__(self):
        # Automatically detect the directory of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the relative path to the model file
        model_path = os.path.join(base_dir, 'saved', 'xgboost_model.json')
        self.model = xgb.XGBClassifier()
        self.model.load_model(model_path)

    def predict(self, features):
        features = np.array(features).reshape(1, -1)
        return self.model.predict_proba(features)

