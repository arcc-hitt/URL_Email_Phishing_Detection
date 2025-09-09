#!/usr/bin/env python3
"""
Health check script for Oracle Cloud monitoring
This script can be used by Oracle Cloud monitoring services
"""
import sys
import requests
import json
import time
from urllib.parse import urljoin

def check_endpoint(base_url, endpoint, timeout=30):
    """Check if an endpoint is healthy"""
    try:
        url = urljoin(base_url, endpoint)
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            return True, data
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
            
    except requests.exceptions.RequestException as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e}"

def main():
    """Main health check function"""
    base_url = "http://localhost:8000"
    
    # Override with environment variable if provided
    import os
    base_url = os.environ.get("HEALTH_CHECK_URL", base_url)
    
    print(f"🏥 Health Check for {base_url}")
    print("=" * 50)
    
    endpoints = [
        ("/health", "General Health"),
        ("/api/url/health", "URL Analysis Service")
    ]
    
    all_healthy = True
    
    for endpoint, description in endpoints:
        print(f"\n🔍 Checking {description}...")
        
        healthy, result = check_endpoint(base_url, endpoint)
        
        if healthy:
            print(f"✅ {description}: HEALTHY")
            if isinstance(result, dict):
                status = result.get('status', 'unknown')
                print(f"   Status: {status}")
        else:
            print(f"❌ {description}: UNHEALTHY")
            print(f"   Error: {result}")
            all_healthy = False
    
    print("\n" + "=" * 50)
    
    if all_healthy:
        print("🎉 All health checks passed!")
        return 0
    else:
        print("❌ Some health checks failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())