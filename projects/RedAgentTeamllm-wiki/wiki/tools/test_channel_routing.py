#!/usr/bin/env python3
"""
OpenClaw Channel Routing Validation Script
Tests channel isolation and routing separation
"""

import json
import subprocess
import sys
from pathlib import Path

def load_config():
    """Load OpenClaw configuration"""
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    with open(config_path) as f:
        return json.load(f)

def test_channel_status():
    """Test: openclaw channels status"""
    result = subprocess.Popen(
        ["openclaw", "channels", "status"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )
    stdout, stderr = result.communicate()
    print(f"✅ Channel status command executed")
    print(f"   stdout: {stdout[:200] if stdout else 'no output'}")
    return result.returncode == 0

def test_feishu_enabled():
    """Test: Feishu channel is enabled"""
    config = load_config()
    feishu_enabled = config.get("channels", {}).get("feishu", {}).get("enabled", False)
    print(f"✅ Feishu channel: {'enabled' if feishu_enabled else 'disabled'}")
    return feishu_enabled

def test_allowfrom_configured():
    """Test: allowFrom is configured for Feishu"""
    config = load_config()
    allow_from = config.get("channels", {}).get("feishu", {}).get("allowFrom", [])
    print(f"✅ Feishu allowFrom: {allow_from}")
    return len(allow_from) > 0

def test_webchat_not_bound():
    """Test: WebChat is NOT configured as a channel (uses default)"""
    config = load_config()
    webchat_config = config.get("channels", {}).get("webchat", None)
    print(f"✅ WebChat config: {'present (WARNING)' if webchat_config else 'absent (CORRECT)'}")
    return webchat_config is None

def main():
    print("=" * 60)
    print("OpenClaw Channel Routing Validation")
    print("=" * 60)
    
    tests = [
        ("Channel Status Command", test_channel_status),
        ("Feishu Enabled", test_feishu_enabled),
        ("allowFrom Configured", test_allowfrom_configured),
        ("WebChat Not Bound", test_webchat_not_bound),
    ]
    
    results = []
    for name, test_fn in tests:
        try:
            result = test_fn()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("Summary:")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"  Passed: {passed}/{total}")
    
    if passed == total:
        print("  ✅ All tests passed - Channel routing is correctly configured")
        return 0
    else:
        print("  ❌ Some tests failed - Review configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())
