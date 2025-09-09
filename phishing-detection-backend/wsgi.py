import os
import sys

# Set TensorFlow environment variables before importing TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress all TF logs except errors
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Disable GPU
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'false'
os.environ['TF_GPU_ALLOCATOR'] = 'cuda_malloc_async'

# Reduce Python memory usage
os.environ['PYTHONHASHSEED'] = '0'

# Import app after setting environment variables
from app import app, config

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT)