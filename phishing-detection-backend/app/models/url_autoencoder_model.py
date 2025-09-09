import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError

# Configure TensorFlow for memory efficiency
tf.config.experimental.enable_memory_growth = True
if tf.config.list_physical_devices('GPU'):
    for gpu in tf.config.list_physical_devices('GPU'):
        tf.config.experimental.set_memory_growth(gpu, True)

class URLAutoencoderModel:
    def __init__(self):
        # Automatically detect the directory of the current script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the relative path to the model file
        model_path = os.path.join(base_dir, 'saved', 'url_autoencoder_model.h5')
        
        # Load model with memory optimization
        with tf.device('/CPU:0'):  # Force CPU usage to avoid GPU memory issues
            self.model = load_model(model_path, custom_objects={'mse': MeanSquaredError()})

    def predict(self, features):
        features = np.array(features, dtype=np.float32)  # Use float32 to save memory
        if features.ndim == 1:
            features = features.reshape(1, -1)
        
        with tf.device('/CPU:0'):  # Force CPU usage
            reconstructed = self.model.predict(features, verbose=0)  # Disable verbose output
        
        error = np.mean(np.power(features - reconstructed, 2), axis=1)
        return error