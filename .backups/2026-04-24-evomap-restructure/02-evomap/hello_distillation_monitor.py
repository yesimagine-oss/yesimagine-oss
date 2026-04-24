#!/usr/bin/env python3
"""
Distillation Monitor for A2A Hello Protocol Assets
"""

import json
import os
from datetime import datetime

STATE_FILE = "/home/admin/.openclaw/workspace/evomap-workbench-min/hello_distillation_state.json"
DISTILLATION_THRESHOLD = 25  # Lower threshold for protocol assets
CHAIN_ID = "chain_a2a_hello_protocol_20260407"

class HelloDistillationMonitor:
    def __init__(self):
        self.state = self.load_state()
    
    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE) as f:
                return json.load(f)
        return {
            "total_executions": 1,
            "successful_executions": 1,
            "failed_executions": 0,
            "last_execution": datetime.utcnow().isoformat(),
            "distillation_triggered": False,
            "threshold": DISTILLATION_THRESHOLD,
            "chain_id": CHAIN_ID,
            "asset_type": "protocol_implementation"
        }
    
    def save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)
    
    def record_execution(self, success=True):
        self.state["total_executions"] += 1
        if success:
            self.state["successful_executions"] += 1
        else:
            self.state["failed_executions"] += 1
        
        self.state["last_execution"] = datetime.utcnow().isoformat()
        self.save_state()
        
        if (self.state["successful_executions"] >= self.state["threshold"] and 
            not self.state["distillation_triggered"]):
            return self.trigger_distillation()
        
        return self.get_status()
    
    def trigger_distillation(self):
        self.state["distillation_triggered"] = True
        self.save_state()
        
        print("🧬 A2A HELLO PROTOCOL DISTILLATION TRIGGERED!")
        print(f"Total executions: {self.state['total_executions']}")
        print(f"Success rate: {self.state['successful_executions'] / self.state['total_executions'] * 100:.1f}%")
        
        distilled_gene = {
            "type": "Gene",
            "schema_version": "1.5.0",
            "category": "repair",
            "signals_match": [
                "a2a_protocol",
                "hello_endpoint",
                "node_registration",
                "agent_handshake"
            ],
            "summary": f"🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... A2A Hello Protocol Implementation - Distilled from {self.state['successful_executions']} successful registrations",
            "strategy": [
                "Construct GEP-A2A envelope → include all required fields",
                "Generate unique message_id → timestamp + random suffix",
                "Set environment fingerprint → node_version, platform, arch",
                "Validate payload structure → check required fields presence",
                "Handle referrer parameter → enable network propagation",
                "Ensure sender_id uniqueness → prevent collisions"
            ],
            "validation": ["python3 validate_hello_payload.py"],
            "metadata": {
                "distilled_from_chain_id": CHAIN_ID,
                "distillation_date": datetime.utcnow().isoformat(),
                "execution_records": self.state["successful_executions"],
                "success_rate": self.state["successful_executions"] / self.state["total_executions"],
                "protocol_version": "1.0.0"
            }
        }
        
        gePEX_file = f"/home/admin/.openclaw/workspace/distilled_hello_gep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(gePEX_file, "w", encoding='utf-8') as f:
            json.dump(distilled_gene, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Distilled Gene saved: {gePEX_file}")
        return distilled_gene
    
    def get_status(self):
        success_rate = (self.state["successful_executions"] / self.state["total_executions"] * 100) if self.state["total_executions"] > 0 else 0
        remaining = max(0, self.state["threshold"] - self.state["successful_executions"])
        
        return {
            "chain_id": CHAIN_ID,
            "total_executions": self.state["total_executions"],
            "successful_executions": self.state["successful_executions"],
            "failed_executions": self.state["failed_executions"],
            "success_rate": f"{success_rate:.1f}%",
            "remaining_for_distillation": remaining,
            "distillation_triggered": self.state["distillation_triggered"],
            "last_execution": self.state["last_execution"]
        }
    
    def report_status(self):
        status = self.get_status()
        
        print("\n" + "="*60)
        print("📡 A2A HELLO PROTOCOL DISTILLATION MONITOR")
        print("="*60)
        print(f"Chain ID: {status['chain_id']}")
        print(f"Total Executions: {status['total_executions']}")
        print(f"Successful: {status['successful_executions']} ✓")
        print(f"Failed: {status['failed_executions']} ✗")
        print(f"Success Rate: {status['success_rate']}")
        print(f"Remaining for Distillation: {status['remaining_for_distillation']}")
        print(f"Distillation Triggered: {'✅ YES' if status['distillation_triggered'] else '⏳ NO'}")
        print(f"Last Execution: {status['last_execution']}")
        print("="*60 + "\n")

def main():
    import sys
    monitor = HelloDistillationMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "record-success":
            status = monitor.record_execution(success=True)
            print(f"✅ Execution recorded")
            monitor.report_status()
        elif command == "record-failure":
            status = monitor.record_execution(success=False)
            print(f"❌ Execution failed recorded")
            monitor.report_status()
        elif command == "status":
            monitor.report_status()
        elif command == "trigger":
            if monitor.state["successful_executions"] >= monitor.state["threshold"]:
                monitor.trigger_distillation()
            else:
                print(f"⚠️ Threshold not reached ({monitor.state['successful_executions']}/{monitor.state['threshold']})")
        else:
            print("Usage: hello_distillation_monitor.py [record-success|record-failure|status|trigger]")
    else:
        monitor.report_status()

if __name__ == "__main__":
    main()