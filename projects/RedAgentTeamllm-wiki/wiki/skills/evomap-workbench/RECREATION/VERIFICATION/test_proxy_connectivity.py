#!/usr/bin/env python3
# test_proxy_connectivity.py
# Verification script to test proxy connectivity

import requests
import sys
from typing import Tuple

def test_proxy_connectivity(proxy_url: str = "http://127.0.0.1:7890") -> Tuple[bool, str]:
    """
    Test if the proxy is working correctly by making a request through it.
    
    Args:
        proxy_url: The URL of the proxy server
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    # Test domains that require proxy access
    test_urls = [
        'https://evomap.ai',
        'https://clawhub.com'
    ]
    
    for url in test_urls:
        try:
            print(f"Testing {url} through proxy...")
            response = requests.get(url, proxies=proxies, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Successfully accessed {url}")
                return True, f"Proxy connectivity verified via {url}"
            else:
                print(f"❌ Failed to access {url}: HTTP {response.status_code}")
                
        except requests.exceptions.ProxyError as e:
            print(f"❌ Proxy error when accessing {url}: {e}")
            return False, f"Proxy error: {e}"
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout when accessing {url}: {e}")
            return False, f"Timeout: {e}"
        except Exception as e:
            print(f"❌ Unexpected error when accessing {url}: {e}")
            return False, f"Unexpected error: {e}"
    
    return False, "All test URLs failed"

if __name__ == "__main__":
    success, message = test_proxy_connectivity()
    
    if success:
        print("\n🎉 All proxy connectivity tests PASSED")
        sys.exit(0)  # Success exit code
    else:
        print(f"\n❌ Proxy connectivity tests FAILED: {message}")
        sys.exit(1)  # Failure exit code)