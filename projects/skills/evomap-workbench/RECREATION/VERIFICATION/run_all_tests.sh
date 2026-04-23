#!/bin/bash
# run_all_tests.sh
# Run all verification tests for EvoMap Workbench

set -e  # Exit on any error

echo "🧪 Starting comprehensive verification suite..."

echo "1️⃣ Testing proxy connectivity"
python3 VERIFICATION/test_proxy_connectivity.py || { echo "❌ Proxy test failed"; exit 1; }

echo "\n2️⃣ Testing node credentials"
python3 VERIFICATION/test_node_credentials.py || { echo "❌ Node credentials test failed"; exit 1; }

echo "\n3️⃣ Testing dependencies"
python3 VERIFICATION/test_dependencies.py || { echo "❌ Dependencies test failed"; exit 1; }

echo "\n🎉 All verification tests PASSED!"