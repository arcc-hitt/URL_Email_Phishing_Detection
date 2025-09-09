#!/usr/bin/env python3
"""
Comprehensive test script for model loading and functionality
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_environment():
    """Test environment and dependencies"""
    try:
        print("=== Testing Environment ===")
        
        # Test Python version
        python_version = sys.version_info
        print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 8):
            print("⚠️  Warning: Python 3.8+ recommended")
        
        # Test required packages
        packages = ['numpy', 'pandas', 'sklearn', 'xgboost', 'tensorflow', 'flask', 'pymongo']
        for package in packages:
            try:
                __import__(package)
                print(f"✓ {package} available")
            except ImportError:
                print(f"✗ {package} not available")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Environment test failed: {e}")
        return False

def test_model_files():
    """Test that model files exist"""
    try:
        print("\n=== Testing Model Files ===")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(base_dir, 'app', 'models', 'saved')
        
        required_files = [
            'xgboost_model.json',
            'url_autoencoder_model.h5'
        ]
        
        for file_name in required_files:
            file_path = os.path.join(models_dir, file_name)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"✓ {file_name} exists ({file_size:,} bytes)")
            else:
                print(f"✗ {file_name} not found at {file_path}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Model file test failed: {e}")
        return False

def test_xgboost_model():
    """Test XGBoost model loading and prediction"""
    try:
        print("\n=== Testing XGBoost Model ===")
        
        from app.models.xgboost_model import XGBoostModel
        model = XGBoostModel()
        print("✓ XGBoost model loaded successfully")
        
        # Test prediction with dummy features
        import numpy as np
        dummy_features = np.random.rand(30)  # Assuming 30 features
        prediction = model.predict(dummy_features)
        print(f"✓ XGBoost prediction successful: shape {prediction.shape}")
        
        return True
        
    except Exception as e:
        print(f"✗ XGBoost model test failed: {e}")
        return False

def test_autoencoder_model():
    """Test Autoencoder model loading and prediction"""
    try:
        print("\n=== Testing Autoencoder Model ===")
        
        from app.models.url_autoencoder_model import URLAutoencoderModel
        model = URLAutoencoderModel()
        print("✓ Autoencoder model loaded successfully")
        
        # Test prediction with dummy features
        import numpy as np
        dummy_features = np.random.rand(30)  # Assuming 30 features
        prediction = model.predict(dummy_features)
        print(f"✓ Autoencoder prediction successful: {prediction}")
        
        return True
        
    except Exception as e:
        print(f"✗ Autoencoder model test failed: {e}")
        return False

def test_feature_extraction():
    """Test feature extraction functionality"""
    try:
        print("\n=== Testing Feature Extraction ===")
        
        from app.utils.feature_extraction import extract_url_features
        
        test_urls = [
            "https://example.com",
            "https://google.com/search?q=test",
            "http://suspicious-site.com/login.php"
        ]
        
        for url in test_urls:
            features = extract_url_features(url)
            print(f"✓ {url}: {len(features)} features extracted")
        
        return True
        
    except Exception as e:
        print(f"✗ Feature extraction test failed: {e}")
        return False

def test_url_service():
    """Test complete URL service functionality"""
    try:
        print("\n=== Testing URL Service ===")
        
        from app.services.url_service import URLService
        service = URLService()
        print("✓ URL service initialized successfully")
        
        # Test with safe URLs
        test_urls = ["https://google.com", "https://github.com"]
        
        for url in test_urls:
            result = service.analyze_url(url)
            print(f"✓ Analysis for {url}: phishing={result['is_phishing']}")
        
        return True
        
    except Exception as e:
        print(f"✗ URL service test failed: {e}")
        return False

def test_flask_app():
    """Test Flask app creation"""
    try:
        print("\n=== Testing Flask App ===")
        
        from app import app
        print("✓ Flask app created successfully")
        
        # Test app configuration
        print(f"✓ Debug mode: {app.debug}")
        print(f"✓ Secret key configured: {'SECRET_KEY' in app.config}")
        
        return True
        
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Comprehensive Model Tests\n")
    
    tests = [
        ("Environment", test_environment),
        ("Model Files", test_model_files),
        ("Feature Extraction", test_feature_extraction),
        ("XGBoost Model", test_xgboost_model),
        ("Autoencoder Model", test_autoencoder_model),
        ("URL Service", test_url_service),
        ("Flask App", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())