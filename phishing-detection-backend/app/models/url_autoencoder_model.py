import os
import logging
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError

# Configure TensorFlow to suppress warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

logger = logging.getLogger(__name__)

class URLAutoencoderModel:
    def __init__(self):
        try:
            # Automatically detect the directory of the current script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the relative path to the model file
            model_path = os.path.join(base_dir, 'saved', 'url_autoencoder_model.h5')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Autoencoder model file not found at: {model_path}")
            
            logger.info(f"Loading Autoencoder model from: {model_path}")
            self.model = load_model(model_path, custom_objects={'mse': MeanSquaredError()})
            logger.info("Autoencoder model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load Autoencoder model: {e}")
            raise e

    def predict(self, features):
        try:
            features = np.array(features, dtype=np.float32)
            if features.ndim == 1:
                features = features.reshape(1, -1)
            
            if features.shape[1] == 0:
                raise ValueError("No features provided for prediction")
            
            # Suppress TensorFlow prediction logs
            reconstructed = self.model.predict(features, verbose=0)
            error = np.mean(np.power(features - reconstructed, 2), axis=1)
            return error
            
        except Exception as e:
            logger.error(f"Autoencoder prediction failed: {e}")
            raise e