#!/usr/bin/env python3
"""
Startup script for Oracle Cloud deployment
This script can be used to test the application before deployment
"""
import os
import sys
import logging

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        print("Testing imports...")
        
        # Test Flask imports
        from flask import Flask
        from flask_cors import CORS
        print("✓ Flask imports successful")
        
        # Test ML library imports
        import numpy as np
        import pandas as pd
        import sklearn
        import xgboost as xgb
        import tensorflow as tf
        print("✓ ML library imports successful")
        
        # Test MongoDB import
        from pymongo import MongoClient
        print("✓ MongoDB import successful")
        
        # Test application imports
        from app import app
        from app.config import config
        print("✓ Application imports successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during imports: {e}")
        return False

def test_models():
    """Test that ML models can be loaded"""
    try:
        print("\nTesting model loading...")
        
        # Test XGBoost model
        from app.models.xgboost_model import XGBoostModel
        xgb_model = XGBoostModel()
        print("✓ XGBoost model loaded successfully")
        
        # Test Autoencoder model
        from app.models.url_autoencoder_model import URLAutoencoderModel
        ae_model = URLAutoencoderModel()
        print("✓ Autoencoder model loaded successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        return False

def test_feature_extraction():
    """Test feature extraction"""
    try:
        print("\nTesting feature extraction...")
        
        from app.utils.feature_extraction import extract_url_features
        features = extract_url_features("https://example.com")
        print(f"✓ Feature extraction successful, extracted {len(features)} features")
        
        return True
        
    except Exception as e:
        print(f"✗ Feature extraction failed: {e}")
        return False

def test_url_service():
    """Test URL service"""
    try:
        print("\nTesting URL service...")
        
        from app.services.url_service import URLService
        service = URLService()
        
        # Test with a safe URL
        result = service.analyze_url("https://google.com")
        print(f"✓ URL service test successful: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ URL service test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Phishing Detection API Startup Test ===\n")
    
    tests = [
        ("Import Test", test_imports),
        ("Model Loading Test", test_models),
        ("Feature Extraction Test", test_feature_extraction),
        ("URL Service Test", test_url_service)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n=== Test Results: {passed}/{total} passed ===")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())