#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代理按需启动脚本 - 浏览器触发版
原理：浏览器访问外网失败时自动触发启动代理
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class ProxyOnDemand:
    def __init__(self):
        self.clash_path = '/home/admin/bin/clash'
        self.config_dir = Path.home() / '.config' / 'mihomo'
        self.config_file = self.config_dir / 'config.yaml'
        self.pid_file = Path.home() / '.openclaw' / 'proxy.pid'
        self.trigger_log = Path.home() / '.openclaw' / 'logs' / 'proxy-trigger.log'
        
        # 确保日志目录存在
        self.trigger_log.parent.mkdir(parents=True, exist_ok=True)
        
    def log(self, message):
        """记录日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}\n"
        
        with open(self.trigger_log, 'a', encoding='utf-8') as f:
            f.write(log_msg)
        
        print(log_msg, end='')
    
    def is_running(self):
        """检查代理是否运行"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, ValueError):
            self.pid_file.unlink(missing_ok=True)
            return False
    
    def start(self):
        """启动代理"""
        if self.is_running():
            self.log("代理已在运行，无需启动")
            return True
        
        self.log("检测到外网访问需求，自动启动代理...")
        
        try:
            cmd = [self.clash_path, '-d', str(self.config_dir), '-f', str(self.config_file)]
            
            with open('/tmp/clash.log', 'w') as log:
                process = subprocess.Popen(cmd, stdout=log, stderr=log, start_new_session=True)
            
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))
            
            time.sleep(3)
            
            if self.is_running():
                self.log(f"代理已启动 (PID: {process.pid})")
                return True
            else:
                self.log("代理启动失败")
                return False
                
        except Exception as e:
            self.log(f"启动代理失败：{e}")
            return False

if __name__ == '__main__':
    proxy = ProxyOnDemand()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        # 检查模式：检查代理是否运行，不运行则启动
        if not proxy.is_running():
            proxy.start()
        else:
            print("代理运行中")
    else:
        # 启动模式：直接启动代理
        proxy.start()
