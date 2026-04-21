#!/usr/bin/env python3
# test_node_credentials.py
# Verification script to test node credentials

import os
import sys
from typing import Tuple

def validate_node_credentials() -> Tuple[bool, str]:
    """
    Validate that node_id and node_secret files exist and contain valid content.
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    node_id_path = os.path.expanduser("~/.evomap/node_id")
    node_secret_path = os.path.expanduser("~/.evomap/node_secret")
    
    # Check if files exist
    if not os.path.exists(node_id_path):
        return False, f"node_id file not found at {node_id_path}"
    
    if not os.path.exists(node_secret_path):
        return False, f"node_secret file not found at {node_secret_path}"
    
    # Read and validate content
    try:
        with open(node_id_path, 'r') as f:
            node_id = f.read().strip()
            
        if not node_id or len(node_id) < 32:
            return False, f"Invalid node_id format: '{node_id[:50]}...'", length={len(node_id)}"
            
        with open(node_secret_path, 'r') as f:
            node_secret = f.read().strip()
            
        if not node_secret or len(node_secret) < 64:
            return False, f"Invalid node_secret format: '{node_secret[:50]}...'", length={len(node_secret)}"
            
        return True, "Node credentials are valid and properly formatted"
        
    except Exception as e:
        return False, f"Error reading credential files: {e}"

if __name__ == "__main__":
    success, message = validate_node_credentials()
    
    if success:
        print("\n✅ Node credentials validation PASSED")
        print(f"{message}")
        sys.exit(0)  # Success exit code
    else:
        print("\n❌ Node credentials validation FAILED")
        print(f"{message}")
        sys.exit(1)  # Failure exit code)