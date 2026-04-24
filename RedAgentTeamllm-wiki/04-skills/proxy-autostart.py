#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代理自动启动服务 - 端口监听触发版
原理：监听 7890 端口，当有连接请求但代理未运行时自动启动
"""

import socket
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime

class ProxyAutoStart:
    def __init__(self):
        self.clash_path = '/home/admin/bin/clash'
        self.config_dir = Path.home() / '.config' / 'mihomo'
        self.config_file = self.config_dir / 'config.yaml'
        self.pid_file = Path.home() / '.openclaw' / 'proxy.pid'
        self.log_file = Path.home() / '.openclaw' / 'logs' / 'proxy-autostart.log'
        
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg)
        
        print(log_msg, end='')
    
    def is_running(self):
        """检查代理是否运行"""
        if not self.pid_file.exists():
            return False
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            import os
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, ValueError):
            self.pid_file.unlink(missing_ok=True)
            return False
    
    def start_proxy(self):
        """启动代理"""
        if self.is_running():
            return True
        
        self.log("检测到代理端口连接请求，自动启动 Clash...")
        
        try:
            cmd = [self.clash_path, '-d', str(self.config_dir), '-f', str(self.config_file)]
            
            with open('/tmp/clash.log', 'w') as log:
                process = subprocess.Popen(cmd, stdout=log, stderr=log, start_new_session=True)
            
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))
            
            time.sleep(3)
            
            if self.is_running():
                self.log(f"Clash 已启动 (PID: {process.pid})")
                return True
            else:
                self.log("Clash 启动失败")
                return False
                
        except Exception as e:
            self.log(f"启动失败：{e}")
            return False
    
    def check_port(self, port=7890, timeout=2):
        """检查端口是否有连接请求"""
        try:
            # 如果端口被占用，说明 Clash 已在运行
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            try:
                sock.bind(('127.0.0.1', port))
                # 绑定成功，说明端口空闲
                sock.listen(1)
                sock.settimeout(timeout)
                
                try:
                    conn, addr = sock.accept()
                    conn.close()
                    return True  # 有连接请求
                except socket.timeout:
                    return False  # 无连接请求
                finally:
                    sock.close()
            except OSError as e:
                if e.errno == 98:  # Address already in use
                    # Clash 已在运行，无需启动
                    return None
                raise
                
        except Exception as e:
            self.log(f"端口检查失败：{e}")
            return False
    
    def run(self):
        """运行自动启动服务"""
        self.log("=" * 50)
        self.log("代理自动启动服务运行")
        self.log("监听端口：7890")
        self.log("检查间隔：5 秒")
        self.log("=" * 50)
        
        check_interval = 5  # 5 秒检查一次
        last_trigger = 0
        clash_running = False
        
        while True:
            try:
                import time
                current_time = time.time()
                
                # 检查端口状态
                port_status = self.check_port()
                
                if port_status is None:
                    # Clash 已在运行
                    if not clash_running:
                        self.log("Clash 已在运行，进入监控模式")
                        clash_running = True
                elif port_status:
                    # 有连接请求
                    clash_running = False
                    if current_time - last_trigger > 60:  # 避免频繁触发
                        if not self.is_running():
                            self.start_proxy()
                        last_trigger = current_time
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                self.log("收到中断信号，停止服务")
                break
            except Exception as e:
                self.log(f"服务错误：{e}")
                time.sleep(check_interval)

if __name__ == '__main__':
    service = ProxyAutoStart()
    service.run()
