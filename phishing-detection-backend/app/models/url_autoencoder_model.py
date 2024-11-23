import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError

class URLAutoencoderModel:
    def __init__(self):
        # Automatically detect the directory of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the relative path to the model file
        model_path = os.path.join(base_dir, 'saved', 'url_autoencoder_model.h5')
        self.model = load_model(model_path, custom_objects={'mse': MeanSquaredError()})

    def predict(self, features):
        features = np.array(features)
        if features.ndim == 1:
            features = features.reshape(1, -1)
        reconstructed = self.model.predict(features)
        error = np.mean(np.power(features - reconstructed, 2), axis=1)
        return error