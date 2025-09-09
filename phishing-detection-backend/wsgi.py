import os
import sys

# Set TensorFlow environment variables before importing TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress all TF logs except errors
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Disable GPU
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'false'

# Reduce Python memory usage
os.environ['PYTHONHASHSEED'] = '0'

# Configure TensorFlow before importing app
from app.tf_config import tf

# Import app after TensorFlow configuration
from app import app, config

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT)