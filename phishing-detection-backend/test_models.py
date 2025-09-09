#!/usr/bin/env python3
"""
Simple script to test model loading without starting the full Flask app
"""
import os
import sys

# Set TensorFlow environment variables before importing anything
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def test_xgboost_model():
    try:
        print("Testing XGBoost model loading...")
        from app.models.xgboost_model import XGBoostModel
        model = XGBoostModel()
        print("✓ XGBoost model loaded successfully")
        return True
    except Exception as e:
        print(f"✗ XGBoost model failed: {e}")
        return False

def test_autoencoder_model():
    try:
        print("Testing Autoencoder model loading...")
        # Import TensorFlow config first
        from app.tf_config import tf
        from app.models.url_autoencoder_model import URLAutoencoderModel
        model = URLAutoencoderModel()
        print("✓ Autoencoder model loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Autoencoder model failed: {e}")
        return False

def test_feature_extraction():
    try:
        print("Testing feature extraction...")
        from app.utils.feature_extraction import extract_url_features
        features = extract_url_features("https://example.com")
        print(f"✓ Feature extraction successful, extracted {len(features)} features")
        return True
    except Exception as e:
        print(f"✗ Feature extraction failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting model tests...")
    
    success_count = 0
    total_tests = 3
    
    if test_feature_extraction():
        success_count += 1
    
    if test_xgboost_model():
        success_count += 1
    
    if test_autoencoder_model():
        success_count += 1
    
    print(f"\nTest Results: {success_count}/{total_tests} passed")
    
    if success_count == total_tests:
        print("All tests passed! Models should work in production.")
        sys.exit(0)
    else:
        print("Some tests failed. Check the errors above.")
        sys.exit(1)