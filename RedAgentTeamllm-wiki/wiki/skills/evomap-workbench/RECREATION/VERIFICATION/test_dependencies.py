#!/usr/bin/env python3
# test_dependencies.py
# Verification script to test required dependencies

import subprocess
import sys
import os
from typing import Tuple, List

def check_dependency_versions() -> Tuple[bool, str]:
    """
    Check that all required dependencies are installed and have correct versions.
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    issues = []  # type: List[str]
    
    # Check Node.js version
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            issues.append(f"Node.js check failed: {result.stderr}")
        else:
            version = result.stdout.strip().replace('v', '')
            major = int(version.split('.')[0])
            if major < 18:
                issues.append(f"Node.js {version} too old, need >=18.0.0")
    except Exception as e:
        issues.append(f"Node.js not accessible: {e}")
    
    # Check Python version
    try:
        if sys.version_info.major < 3 or (sys.version_info.major == 3 and sys.version_info.minor < 9):
            issues.append(f"Python {'.'.join(map(str, sys.version_info[:2]))} too old, need >=3.9")
    except Exception as e:
        issues.append(f"Python version check failed: {e}")
    
    # Check Clash version
    try:
        result = subprocess.run(['clash', '-v'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            issues.append(f"Clash check failed: {result.stderr}")
        else:
            output = result.stdout.strip()
            # Extract version from output like "Mihomo v1.8.4-1-gf7d6b5a linux/amd64"
            if 'v' in output:
                version_part = output.split('v')[1].split()[0]  # Get first part after 'v'
                version = version_part.split('-')[0]  # Remove git hash if present
                major = int(version.split('.')[0])
                minor = int(version.split('.')[1])
                if major < 1 or (major == 1 and minor < 8):
                    issues.append(f"Clash {output} too old, need >=1.8.0")
    except Exception as e:
        issues.append(f"Clash not found: {e}")
    
    # Check npm is available
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            issues.append(f"npm not working: {result.stderr}")
    except Exception as e:
        issues.append(f"npm not found: {e}")
    
    # Check git is available
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            issues.append(f"git not working: {result.stderr}")
    except Exception as e:
        issues.append(f"git not found: {e}")
    
    # Check curl is available
    try:
        result = subprocess.run(['curl', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            issues.append(f"curl not working: {result.stderr}")
    except Exception as e:
        issues.append(f"curl not found: {e}")
    
    if len(issues) > 0:
        return False, "; ".join(issues)
    else:
        return True, "All dependencies satisfied"

if __name__ == "__main__":
    success, message = check_dependency_versions()
    
    if success:
        print("\n✅ All dependency checks PASSED")
        print(f"{message}")
        sys.exit(0)  # Success exit code
    else:
        print("\n❌ Dependency checks FAILED")
        print(f"{message}")
        sys.exit(1)  # Failure exit code)