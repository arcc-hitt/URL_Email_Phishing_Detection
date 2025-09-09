import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import logging

# Configure TensorFlow for maximum memory efficiency
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs
tf.get_logger().setLevel('ERROR')

# Disable GPU completely
tf.config.set_visible_devices([], 'GPU')

# Configure CPU usage
tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)

logger = logging.getLogger(__name__)

class URLAutoencoderModel:
    def __init__(self):
        try:
            logger.info("Loading URL Autoencoder model...")
            
            # Automatically detect the directory of the current script
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the relative path to the model file
            model_path = os.path.join(base_dir, 'saved', 'url_autoencoder_model.h5')
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            # Load model with maximum memory optimization
            with tf.device('/CPU:0'):  # Force CPU usage
                self.model = load_model(
                    model_path, 
                    custom_objects={'mse': MeanSquaredError()},
                    compile=False  # Don't compile to save memory
                )
            
            logger.info("URL Autoencoder model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading URL Autoencoder model: {e}")
            raise e

    def predict(self, features):
        try:
            features = np.array(features, dtype=np.float32)  # Use float32 to save memory
            if features.ndim == 1:
                features = features.reshape(1, -1)
            
            with tf.device('/CPU:0'):  # Force CPU usage
                # Use batch_size=1 and disable verbose output for memory efficiency
                reconstructed = self.model.predict(
                    features, 
                    verbose=0, 
                    batch_size=1,
                    use_multiprocessing=False
                )
            
            error = np.mean(np.power(features - reconstructed, 2), axis=1)
            return error
            
        except Exception as e:
            logger.error(f"Error in autoencoder prediction: {e}")
            raise e