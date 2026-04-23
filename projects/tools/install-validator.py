#!/usr/bin/env python3
"""
软件安装验证工具
用于验证软件是否正确安装，避免"报喜不报忧"
"""

import subprocess
import sys
import json

class InstallValidator:
    def __init__(self, software_name):
        self.software_name = software_name
        self.results = {
            'name': software_name,
            'steps': [],
            'success': False,
            'errors': []
        }
    
    def log_step(self, step_name, success, details=None, error=None):
        """记录步骤结果"""
        step = {
            'name': step_name,
            'success': success,
            'details': details,
            'error': error
        }
        self.results['steps'].append(step)
        
        if success:
            print(f"✅ {step_name}")
            if details:
                print(f"   {details}")
        else:
            print(f"❌ {step_name}")
            if error:
                print(f"   错误：{error}")
    
    def check_command_exists(self, command):
        """检查命令是否存在"""
        try:
            result = subprocess.run(
                ['which', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=10
            )
            if result.returncode == 0:
                self.log_step(
                    f"命令检查：{command}",
                    True,
                    f"路径：{result.stdout.strip()}"
                )
                return result.stdout.strip()
            else:
                self.log_step(
                    f"命令检查：{command}",
                    False,
                    error="命令未找到"
                )
                return None
        except Exception as e:
            self.log_step(
                f"命令检查：{command}",
                False,
                error=str(e)
            )
            return None
    
    def check_version(self, command, version_args=['--version']):
        """检查版本信息"""
        try:
            result = subprocess.run(
                [command] + version_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=10
            )
            if result.returncode == 0:
                version_info = result.stdout.strip().split('\n')[0][:100]
                self.log_step(
                    f"版本检查",
                    True,
                    f"{version_info}"
                )
                return True
            else:
                self.log_step(
                    f"版本检查",
                    False,
                    error=result.stderr.strip()[:100]
                )
                return False
        except Exception as e:
            self.log_step(
                f"版本检查",
                False,
                error=str(e)[:100]
            )
            return False
    
    def check_process(self, process_name):
        """检查进程是否运行"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', process_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=10
            )
            if result.returncode == 0:
                pids = result.stdout.strip().split('\n')
                self.log_step(
                    f"进程检查：{process_name}",
                    True,
                    f"PID: {', '.join(pids)}"
                )
                return True
            else:
                self.log_step(
                    f"进程检查：{process_name}",
                    False,
                    error="进程未运行"
                )
                return False
        except Exception as e:
            self.log_step(
                f"进程检查：{process_name}",
                False,
                error=str(e)
            )
            return False
    
    def check_port(self, port, use_netstat=False):
        """检查端口是否监听"""
        try:
            if use_netstat:
                result = subprocess.run(
                    ['netstat', '-tlnp'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=10
                )
            else:
                result = subprocess.run(
                    ['ss', '-tlnp'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    timeout=10
                )
            if f':{port}' in result.stdout:
                self.log_step(
                    f"端口检查：{port}",
                    True,
                    f"端口 {port} 正在监听"
                )
                return True
            else:
                self.log_step(
                    f"端口检查：{port}",
                    False,
                    error=f"端口 {port} 未监听"
                )
                return False
        except Exception as e:
            self.log_step(
                f"端口检查：{port}",
                False,
                error=str(e)
            )
            return False
    
    def test_function(self, test_command, description="功能测试"):
        """执行功能测试"""
        try:
            result = subprocess.run(
                test_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            if result.returncode == 0:
                self.log_step(
                    f"{description}",
                    True,
                    result.stdout.strip()[:200] if result.stdout else "测试通过"
                )
                return True
            else:
                self.log_step(
                    f"{description}",
                    False,
                    error=result.stderr.strip()[:200] if result.stderr else "测试失败"
                )
                return False
        except Exception as e:
            self.log_step(
                f"{description}",
                False,
                error=str(e)[:200]
            )
            return False
    
    def finalize(self):
        """总结验证结果"""
        total_steps = len(self.results['steps'])
        success_steps = sum(1 for s in self.results['steps'] if s['success'])
        
        print()
        print('='*60)
        if success_steps == total_steps:
            print(f"✅ {self.software_name} 安装验证通过 ({success_steps}/{total_steps})")
            self.results['success'] = True
        else:
            print(f"⚠️ {self.software_name} 安装验证部分通过 ({success_steps}/{total_steps})")
            print()
            print("失败的步骤:")
            for step in self.results['steps']:
                if not step['success']:
                    print(f"  ❌ {step['name']}: {step.get('error', '未知错误')}")
            self.results['success'] = False
        print('='*60)
        
        return self.results['success']

# 常用软件验证模板
def validate_clash():
    """验证 Clash/Mihomo 安装"""
    v = InstallValidator("Clash/Mihomo")
    
    # 1. 检查命令
    path = v.check_command_exists('clash')
    if not path:
        path = v.check_command_exists('mihomo')
    
    if path:
        # 2. 检查版本（Clash 用 -v）
        cmd = path.split('/')[-1]
        v.check_version(cmd, ['-v'])
        
        # 3. 检查进程
        v.check_process('clash')
        
        # 4. 检查端口（用 netstat 代替 ss）
        v.check_port(7890, use_netstat=True)
        v.check_port(9090, use_netstat=True)
    
    return v.finalize()

def validate_python_package(package_name):
    """验证 Python 包安装"""
    v = InstallValidator(f"Python 包：{package_name}")
    
    # 检查包是否安装
    v.test_function(
        f"python3 -c 'import {package_name}; print({package_name}.__version__)'",
        f"包导入测试：{package_name}"
    )
    
    return v.finalize()

def validate_node_package(package_name):
    """验证 Node.js 包安装"""
    v = InstallValidator(f"Node.js 包：{package_name}")
    
    # 检查包是否全局安装
    v.test_function(
        f"npm list -g {package_name}",
        f"全局包检查：{package_name}"
    )
    
    return v.finalize()

# ==================== 更多验证模板 ====================

def validate_git():
    """验证 Git 安装"""
    v = InstallValidator("Git")
    v.check_command_exists('git')
    v.check_version('git')
    v.test_function('git config --global user.name', 'Git 用户名配置')
    v.test_function('git config --global user.email', 'Git 邮箱配置')
    return v.finalize()

def validate_docker():
    """验证 Docker 安装"""
    v = InstallValidator("Docker")
    v.check_command_exists('docker')
    v.check_version('docker', ['--version'])
    v.check_process('dockerd')
    v.test_function('docker info', 'Docker 服务状态')
    v.check_command_exists('docker-compose')
    return v.finalize()

def validate_nginx():
    """验证 Nginx 安装"""
    v = InstallValidator("Nginx")
    v.check_command_exists('nginx')
    v.check_version('nginx', ['-v'])
    v.test_function('nginx -t', 'Nginx 配置测试')
    v.check_process('nginx')
    v.check_port(80, use_netstat=True)
    v.check_port(443, use_netstat=True)
    return v.finalize()

def validate_mysql():
    """验证 MySQL 安装"""
    v = InstallValidator("MySQL")
    v.check_command_exists('mysql')
    v.check_version('mysql', ['--version'])
    v.check_process('mysqld')
    v.check_port(3306, use_netstat=True)
    return v.finalize()

def validate_redis():
    """验证 Redis 安装"""
    v = InstallValidator("Redis")
    v.check_command_exists('redis-server')
    v.check_command_exists('redis-cli')
    v.check_version('redis-server', ['--version'])
    v.check_process('redis-server')
    v.check_port(6379, use_netstat=True)
    return v.finalize()

def validate_nodejs():
    """验证 Node.js 安装"""
    v = InstallValidator("Node.js")
    v.check_command_exists('node')
    v.check_version('node', ['--version'])
    v.check_command_exists('npm')
    v.check_version('npm', ['--version'])
    v.check_command_exists('npx')
    return v.finalize()

def validate_python():
    """验证 Python 安装"""
    v = InstallValidator("Python")
    v.check_command_exists('python3')
    v.check_version('python3', ['--version'])
    v.check_command_exists('pip3')
    v.check_version('pip3', ['--version'])
    v.test_function('python3 -c "import requests"', 'requests 包检查')
    return v.finalize()

def validate_java():
    """验证 Java 安装"""
    v = InstallValidator("Java")
    v.check_command_exists('java')
    v.check_version('java', ['-version'])
    v.check_command_exists('javac')
    v.check_version('javac', ['-version'])
    import os
    java_home = os.environ.get('JAVA_HOME', '未设置')
    v.log_step('JAVA_HOME 环境变量', True if java_home != '未设置' else False, java_home)
    return v.finalize()

def validate_go():
    """验证 Go 安装"""
    v = InstallValidator("Go")
    v.check_command_exists('go')
    v.check_version('go', ['version'])
    import os
    gopath = os.environ.get('GOPATH', '未设置')
    v.log_step('GOPATH 环境变量', True if gopath != '未设置' else False, gopath)
    return v.finalize()

def validate_rust():
    """验证 Rust 安装"""
    v = InstallValidator("Rust")
    v.check_command_exists('rustc')
    v.check_version('rustc', ['--version'])
    v.check_command_exists('cargo')
    v.check_version('cargo', ['--version'])
    return v.finalize()

def validate_pnpm():
    """验证 pnpm 安装"""
    v = InstallValidator("pnpm")
    v.check_command_exists('pnpm')
    v.check_version('pnpm', ['--version'])
    return v.finalize()

def validate_yarn():
    """验证 Yarn 安装"""
    v = InstallValidator("Yarn")
    v.check_command_exists('yarn')
    v.check_version('yarn', ['--version'])
    return v.finalize()

def validate_pm2():
    """验证 PM2 安装"""
    v = InstallValidator("PM2")
    v.check_command_exists('pm2')
    v.check_version('pm2', ['--version'])
    v.test_function('pm2 list', 'PM2 进程列表')
    return v.finalize()

# ==================== 主程序 ====================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='软件安装验证工具')
    parser.add_argument('software', nargs='?', default='clash', help='要验证的软件')
    parser.add_argument('--python', help='验证 Python 包')
    parser.add_argument('--node', help='验证 Node.js 包')
    parser.add_argument('--list', action='store_true', help='列出所有支持的软件')
    args = parser.parse_args()
    
    # 支持的软件列表
    validators = {
        'clash': validate_clash,
        'mihomo': validate_clash,
        'git': validate_git,
        'docker': validate_docker,
        'nginx': validate_nginx,
        'mysql': validate_mysql,
        'redis': validate_redis,
        'nodejs': validate_nodejs,
        'node': validate_nodejs,
        'python': validate_python,
        'java': validate_java,
        'go': validate_go,
        'rust': validate_rust,
        'pnpm': validate_pnpm,
        'yarn': validate_yarn,
        'pm2': validate_pm2,
    }
    
    if args.list:
        print("支持的软件验证模板:")
        for name in validators.keys():
            print(f"  - {name}")
        print("\n特殊选项:")
        print("  --python <包名>  - 验证 Python 包")
        print("  --node <包名>    - 验证 Node.js 包")
        sys.exit(0)
    
    if args.python:
        validate_python_package(args.python)
    elif args.node:
        validate_node_package(args.node)
    elif args.software in validators:
        validators[args.software]()
    else:
        print(f"❌ 不支持的软件：{args.software}")
        print("\n使用 --list 查看所有支持的软件")
        sys.exit(1)
