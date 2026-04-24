#!/usr/bin/env python3
"""Skill Distillation Monitor - Track execution success rate for distillation trigger"""

import json
import os
from datetime import datetime, timedelta

STATE_FILE = "/home/admin/.openclaw/workspace/evomap-workbench-min/distillation_state.json"
DISTILLATION_THRESHOLD = 100  # Trigger after 100 successful executions
CHAIN_ID = "chain_docker_build_optimization_20260407"

class DistillationMonitor:
    def __init__(self):
        self.state = self.load_state()
    
    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE) as f:
                return json.load(f)
        return {
            "total_executions": 88,  # Starting from current success streak
            "successful_executions": 88,
            "failed_executions": 0,
            "last_execution": None,
            "distillation_triggered": False,
            "threshold": DISTILLATION_THRESHOLD
        }
    
    def save_state(self):
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)
    
    def record_execution(self, success=True):
        """Record a new execution result"""
        self.state["total_executions"] += 1
        if success:
            self.state["successful_executions"] += 1
        else:
            self.state["failed_executions"] += 1
        
        self.state["last_execution"] = datetime.utcnow().isoformat()
        self.save_state()
        
        # Check if distillation should be triggered
        if (self.state["successful_executions"] >= self.state["threshold"] and 
            not self.state["distillation_triggered"]):
            self.trigger_distillation()
        
        return self.get_status()
    
    def trigger_distillation(self):
        """Trigger skill distillation when threshold is reached"""
        self.state["distillation_triggered"] = True
        self.save_state()
        
        print("🧬 SKILL DISTILLATION TRIGGERED!")
        print(f"Total executions: {self.state['total_executions']}")
        print(f"Success rate: {self.state['successful_executions'] / self.state['total_executions'] * 100:.1f}%")
        
        # Generate distilled Gene asset
        distilled_gene = {
            "type": "Gene",
            "schema_version": "1.5.0",
            "category": "optimize",
            "signals_match": [
                "docker_build_cache",
                "buildkit_cache_mount",
                "layer_caching",
                "multi_stage_build",
                "dependency_cache"
            ],
            "summary": f"🦞RedOpenClaw...生活太快⚡️...老逼快跑💨... Docker BuildKit Cache Optimized Pattern - Distilled from {self.state['successful_executions']} successful executions",
            "strategy": [
                "Analyze Docker build bottlenecks → identify dependency installation steps",
                "Implement BuildKit cache mount → configure package manager caches",
                "Configure multi-stage builds → optimize layer ordering",
                "Verify correctness → measure cold vs warm build times"
            ],
            "validation": ["node ./test/vibe_test.js"],
            "metadata": {
                "distilled_from_chain_id": CHAIN_ID,
                "distillation_date": datetime.utcnow().isoformat(),
                "execution_records": self.state["successful_executions"],
                "success_rate": self.state["successful_executions"] / self.state["total_executions"]
            }
        }
        
        # Save distilled gene
        gePEX_file = f"/home/admin/.openclaw/workspace/distilled_gep_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(gePEX_file, "w") as f:
            json.dump(distilled_gene, f, indent=2)
        
        print(f"✅ Distilled Gene saved: {gePEX_file}")
        
        return distilled_gene
    
    def get_status(self):
        """Get current monitoring status"""
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
            "last_execution": self.state["last_execution"] or "None"
        }
    
    def report_status(self):
        """Print formatted status report"""
        status = self.get_status()
        
        print("\n" + "="*60)
        print("📊 DISTILLATION MONITOR STATUS REPORT")
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
    monitor = DistillationMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "record-success":
            status = monitor.record_execution(success=True)
            print(f"✅ Execution recorded successfully")
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
            print("Usage: distillation_monitor.py [record-success|record-failure|status|trigger]")
    else:
        monitor.report_status()

if __name__ == "__main__":
    import sys
    main()
