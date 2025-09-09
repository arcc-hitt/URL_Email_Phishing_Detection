"""
TensorFlow configuration module - must be imported before any TensorFlow operations
"""
import os

# Set TensorFlow environment variables before importing TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Disable GPU
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'false'

# Import TensorFlow and configure it
import tensorflow as tf

# Configure TensorFlow for maximum memory efficiency
tf.get_logger().setLevel('ERROR')

# Disable GPU completely
try:
    tf.config.set_visible_devices([], 'GPU')
except RuntimeError:
    pass  # Already configured

# Configure CPU usage - wrap in try/except to handle already initialized case
try:
    tf.config.threading.set_intra_op_parallelism_threads(1)
    tf.config.threading.set_inter_op_parallelism_threads(1)
except RuntimeError:
    pass  # Already configured

print("TensorFlow configured for CPU-only, single-threaded operation")