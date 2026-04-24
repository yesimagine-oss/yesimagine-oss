#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代理自动管理脚本
功能：按需启动代理，闲置自动关闭

配置：
- 闲置超时：10 分钟（无请求自动关闭）
- 检查间隔：1 分钟
- 自动启动：检测到外网请求时自动启动
"""

import os
import sys
import time
import subprocess
import signal
from datetime import datetime, timedelta
from pathlib import Path

class ProxyManager:
    def __init__(self):
        self.clash_path = '/home/admin/bin/clash'
        self.config_dir = Path.home() / '.config' / 'mihomo'
        self.config_file = self.config_dir / 'config.yaml'
        self.pid_file = Path.home() / '.openclaw' / 'proxy.pid'
        self.log_file = Path.home() / '.openclaw' / 'logs' / 'proxy-manager.log'
        
        # 配置
        self.idle_timeout = 10 * 60  # 10 分钟闲置超时
        self.check_interval = 60  # 1 分钟检查间隔
        
        # 确保日志目录存在
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}\n"
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg)
        
        # 打印到控制台
        print(log_msg, end='')
        
    def is_running(self):
        """检查代理是否运行"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # 检查进程是否存在
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, ValueError):
            # 进程不存在或 PID 文件损坏
            try:
                self.pid_file.unlink()
            except FileNotFoundError:
                pass
            return False
    
    def start(self):
        """启动代理"""
        if self.is_running():
            self.log("代理已在运行中")
            return True
        
        try:
            # 启动 Clash
            cmd = [
                self.clash_path,
                '-d', str(self.config_dir),
                '-f', str(self.config_file)
            ]
            
            # 后台启动
            with open('/tmp/clash.log', 'w') as log:
                process = subprocess.Popen(
                    cmd,
                    stdout=log,
                    stderr=log,
                    start_new_session=True
                )
            
            # 保存 PID
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))
            
            # 等待启动
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
    
    def stop(self):
        """停止代理"""
        if not self.is_running():
            self.log("代理未运行")
            return True
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # 发送 SIGTERM
            os.kill(pid, signal.SIGTERM)
            
            # 等待进程结束
            for _ in range(10):
                time.sleep(1)
                if not self.is_running():
                    self.log("代理已停止")
                    self.pid_file.unlink(missing_ok=True)
                    return True
            
            # 如果还没停止，强制停止
            os.kill(pid, signal.SIGKILL)
            self.log("代理已强制停止")
            try:
                self.pid_file.unlink()
            except FileNotFoundError:
                pass
            return True
            
        except Exception as e:
            self.log(f"停止代理失败：{e}")
            return False
    
    def check_activity(self):
        """检查是否有代理活动"""
        # 检查 7890 端口的连接
        try:
            result = subprocess.run(
                ['netstat', '-an'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # 检查是否有 ESTABLISHED 连接
            for line in result.stdout.split('\n'):
                if ':7890' in line and 'ESTABLISHED' in line:
                    return True
            
            return False
        except:
            return False
    
    def monitor(self):
        """监控循环"""
        self.log("=" * 50)
        self.log("代理管理器启动")
        self.log(f"闲置超时：{self.idle_timeout // 60} 分钟")
        self.log(f"检查间隔：{self.check_interval} 秒")
        self.log("=" * 50)
        
        last_activity = datetime.now()
        
        while True:
            try:
                # 检查是否有活动
                has_activity = self.check_activity()
                
                if has_activity:
                    last_activity = datetime.now()
                
                # 检查是否超时
                if self.is_running():
                    idle_time = (datetime.now() - last_activity).total_seconds()
                    
                    if idle_time > self.idle_timeout:
                        self.log(f"代理闲置 {idle_time // 60:.0f} 分钟，自动关闭")
                        self.stop()
                    else:
                        self.log(f"代理运行中，已闲置 {idle_time // 60:.0f} 分钟")
                else:
                    self.log("代理未运行")
                
                # 等待下次检查
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                self.log("收到中断信号，停止监控")
                self.stop()
                break
            except Exception as e:
                self.log(f"监控错误：{e}")
                time.sleep(self.check_interval)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='代理自动管理器')
    parser.add_argument('action', choices=['start', 'stop', 'status', 'monitor'],
                       help='操作类型')
    
    args = parser.parse_args()
    
    manager = ProxyManager()
    
    if args.action == 'start':
        manager.start()
    elif args.action == 'stop':
        manager.stop()
    elif args.action == 'status':
        if manager.is_running():
            print("代理运行中")
            if manager.pid_file.exists():
                with open(manager.pid_file, 'r') as f:
                    print(f"PID: {f.read().strip()}")
        else:
            print("代理未运行")
    elif args.action == 'monitor':
        manager.monitor()
