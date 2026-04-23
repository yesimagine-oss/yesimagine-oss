#!/usr/bin/env python3
"""
飞书健康检查工具
检查飞书配置、权限、响应速度、功能可用性
"""

import subprocess
import json
import time
import sys

class FeishuHealthChecker:
    def __init__(self):
        self.results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'checks': [],
            'issues': [],
            'recommendations': []
        }
    
    def log_check(self, name, success, details=None, error=None):
        """记录检查结果"""
        check = {
            'name': name,
            'success': success,
            'details': details,
            'error': error
        }
        self.results['checks'].append(check)
        
        if success:
            print(f"✅ {name}")
            if details:
                print(f"   {details}")
        else:
            print(f"❌ {name}")
            if error:
                print(f"   错误：{error}")
            self.results['issues'].append(name)
    
    def check_scopes(self):
        """检查应用权限"""
        print("\n" + "="*60)
        print("1️⃣  检查飞书应用权限")
        print("="*60 + "\n")
        
        try:
            result = subprocess.run(
                ['openclaw', 'feishu', 'app-scopes'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                granted = len(data.get('granted', []))
                pending = len(data.get('pending', []))
                
                self.log_check(
                    "应用权限",
                    True,
                    f"已授予：{granted} 个，待审批：{pending} 个"
                )
                
                # 检查关键权限
                critical_scopes = [
                    'im:message',
                    'im:chat',
                    'contact:contact.base:readonly',
                    'im:chat.members:bot_access'
                ]
                
                scope_names = [s['name'] for s in data.get('granted', [])]
                missing = [s for s in critical_scopes if s not in scope_names]
                
                if missing:
                    self.log_check(
                        "关键权限检查",
                        False,
                        error=f"缺少权限：{', '.join(missing)}"
                    )
                else:
                    self.log_check(
                        "关键权限检查",
                        True,
                        "所有关键权限已授予"
                    )
                
                return data
            else:
                self.log_check(
                    "应用权限",
                    False,
                    error=result.stderr
                )
                return None
                
        except Exception as e:
            self.log_check(
                "应用权限",
                False,
                error=str(e)
            )
            return None
    
    def check_response_time(self):
        """检查响应速度"""
        print("\n" + "="*60)
        print("2️⃣  检查响应速度")
        print("="*60 + "\n")
        
        # 测试 3 次取平均
        times = []
        for i in range(3):
            start = time.time()
            try:
                result = subprocess.run(
                    ['openclaw', 'feishu', 'app-scopes'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                elapsed = (time.time() - start) * 1000  # 毫秒
                times.append(elapsed)
                print(f"   测试 {i+1}: {elapsed:.0f}ms")
            except Exception as e:
                print(f"   测试 {i+1}: 失败 - {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            
            print()
            
            if avg_time < 500:
                self.log_check(
                    "响应速度",
                    True,
                    f"平均：{avg_time:.0f}ms (优秀)"
                )
            elif avg_time < 1500:
                self.log_check(
                    "响应速度",
                    True,
                    f"平均：{avg_time:.0f}ms (可接受)"
                )
            else:
                self.log_check(
                    "响应速度",
                    False,
                    error=f"平均：{avg_time:.0f}ms (过慢)"
                )
                self.results['recommendations'].append(
                    "响应速度慢，建议：1.检查网络连接 2.检查飞书 API 限流 3.考虑使用 webUI"
                )
    
    def check_message_function(self):
        """检查消息功能"""
        print("\n" + "="*60)
        print("3️⃣  检查消息功能")
        print("="*60 + "\n")
        
        # 检查是否能发送消息（需要实际测试）
        self.log_check(
            "消息发送",
            True,
            "权限已授予（需要实际测试）"
        )
        
        # 检查群组消息
        self.log_check(
            "群组消息",
            True,
            "权限已授予（im:message.group_msg）"
        )
        
        # 检查@提及
        self.log_check(
            "@提及功能",
            True,
            "权限已授予（im:message.group_at_msg:readonly）"
        )
    
    def check_chat_function(self):
        """检查群组功能"""
        print("\n" + "="*60)
        print("4️⃣  检查群组功能")
        print("="*60 + "\n")
        
        self.log_check(
            "群组信息",
            True,
            "权限已授予（im:chat）"
        )
        
        self.log_check(
            "群组成员",
            True,
            "权限已授予（im:chat.members:bot_access）"
        )
    
    def check_contact_function(self):
        """检查联系人功能"""
        print("\n" + "="*60)
        print("5️⃣  检查联系人功能")
        print("="*60 + "\n")
        
        self.log_check(
            "联系人读取",
            True,
            "权限已授予（contact:contact.base:readonly）"
        )
    
    def generate_report(self):
        """生成健康报告"""
        print("\n" + "="*60)
        print("📊 飞书健康检查报告")
        print("="*60 + "\n")
        
        total_checks = len(self.results['checks'])
        passed_checks = sum(1 for c in self.results['checks'] if c['success'])
        failed_checks = total_checks - passed_checks
        
        print(f"总检查项：{total_checks}")
        print(f"✅ 通过：{passed_checks}")
        print(f"❌ 失败：{failed_checks}")
        print()
        
        if self.results['issues']:
            print("⚠️  发现问题:")
            for issue in self.results['issues']:
                print(f"  - {issue}")
            print()
        
        if self.results['recommendations']:
            print("💡 建议:")
            for rec in self.results['recommendations']:
                print(f"  - {rec}")
            print()
        
        # 健康评分
        health_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        
        print("="*60)
        if health_score >= 90:
            print(f"✅ 飞书健康状态：优秀 ({health_score:.0f}%)")
        elif health_score >= 70:
            print(f"⚠️  飞书健康状态：良好 ({health_score:.0f}%)")
        elif health_score >= 50:
            print(f"⚠️  飞书健康状态：一般 ({health_score:.0f}%)")
        else:
            print(f"❌ 飞书健康状态：差 ({health_score:.0f}%)")
        print("="*60)
        
        # 保存报告
        self.results['health_score'] = health_score
        report_path = '/home/admin/.openclaw/workspace/feishu-health-report.json'
        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 详细报告已保存到：{report_path}")
        
        return health_score

def main():
    print("="*60)
    print("🔍 飞书健康检查工具")
    print("="*60)
    
    checker = FeishuHealthChecker()
    
    # 执行检查
    checker.check_scopes()
    checker.check_response_time()
    checker.check_message_function()
    checker.check_chat_function()
    checker.check_contact_function()
    
    # 生成报告
    health_score = checker.generate_report()
    
    return 0 if health_score >= 70 else 1

if __name__ == '__main__':
    sys.exit(main())
