#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 核心技能集成配置

技能组合:
- evomap: 项目执行
- serper: 信息搜索
- proactive-agent: 主动监控
- self-improving-agent: 持续进化

功能:
1. 统一配置管理
2. 技能间调用接口
3. 错误处理机制
4. 日志记录系统
"""

import json
import logging
from pathlib import Path
from datetime import datetime

# 配置
CONFIG_DIR = Path(__file__).parent
LOGS_DIR = CONFIG_DIR.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / "skill-integration.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class SkillIntegrationConfig:
    """技能集成配置类"""
    
    def __init__(self):
        self.config = {
            "evomap": {
                "enabled": True,
                "node_id": "node_67c3b8b37becd262",
                "node_secret": "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf",
                "base_url": "https://evomap.ai",
                "claim_limit": 3,
                "retry_attempts": 3
            },
            "serper": {
                "enabled": True,
                "api_key": "01529847d4aa3cf47b86ca87d28519110db06390",
                "base_url": "https://google.serper.dev",
                "cache_enabled": True,
                "cache_ttl": 3600  # 1 小时
            },
            "proactive-agent": {
                "enabled": True,
                "check_interval": 300,  # 5 分钟
                "alert_enabled": True,
                "alert_channel": "feishu"
            },
            "self-improving-agent": {
                "enabled": True,
                "learning_enabled": True,
                "optimization_enabled": True,
                "record_errors": True,
                "generate_suggestions": True
            }
        }
        
        # 集成规则
        self.integration_rules = {
            "evomap_claim_task": {
                "pre_actions": ["serper_search_task_info"],
                "post_actions": ["proactive_report_status"],
                "on_error": ["self-improving_record_error", "proactive_send_alert"]
            },
            "evomap_execute_task": {
                "pre_actions": ["serper_search_solution"],
                "post_actions": ["proactive_report_result", "self-improving_record_success"],
                "on_error": ["self-improving_record_error", "proactive_send_alert"]
            },
            "proactive_check": {
                "pre_actions": [],
                "post_actions": ["proactive_report_status"],
                "on_error": ["self-improving_record_error"]
            }
        }
        
        logger.info("技能集成配置初始化完成")
    
    def get_config(self, skill_name: str) -> dict:
        """获取技能配置"""
        return self.config.get(skill_name, {})
    
    def get_integration_rules(self, action: str) -> dict:
        """获取集成规则"""
        return self.integration_rules.get(action, {})
    
    def save_config(self, filepath: str = None):
        """保存配置到文件"""
        if not filepath:
            filepath = CONFIG_DIR / "integration-config.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        
        logger.info(f"配置已保存到 {filepath}")
    
    def load_config(self, filepath: str = None):
        """从文件加载配置"""
        if not filepath:
            filepath = CONFIG_DIR / "integration-config.json"
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logger.info(f"配置已从 {filepath} 加载")
        else:
            logger.warning(f"配置文件不存在：{filepath}，使用默认配置")
    
    def validate_config(self) -> bool:
        """验证配置有效性"""
        required_skills = ["evomap", "serper", "proactive-agent", "self-improving-agent"]
        
        for skill in required_skills:
            if skill not in self.config:
                logger.error(f"缺少必需的技能配置：{skill}")
                return False
        
        logging.info("配置验证通过")
        return True


class SkillIntegrationLogger:
    """技能集成日志记录器"""
    
    def __init__(self):
        self.log_file = LOGS_DIR / f"integration-{datetime.now().strftime('%Y%m%d')}.log"
    
    def log_action(self, skill: str, action: str, status: str, details: str = ""):
        """记录技能动作"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "skill": skill,
            "action": action,
            "status": status,
            "details": details
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        logger.info(f"{skill}.{action}: {status} - {details}")
    
    def log_error(self, skill: str, action: str, error: str, context: dict = None):
        """记录错误"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "ERROR",
            "skill": skill,
            "action": action,
            "error": error,
            "context": context or {}
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        logger.error(f"{skill}.{action}: {error}")
    
    def log_learning(self, lesson: str, source: str, applied: bool = False):
        """记录学习内容"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "LEARNING",
            "lesson": lesson,
            "source": source,
            "applied": applied
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        logger.info(f"学习：{lesson} (来自：{source}, 已应用：{applied})")


# 单例模式
_integration_config = None
_integration_logger = None

def get_integration_config() -> SkillIntegrationConfig:
    """获取集成配置单例"""
    global _integration_config
    if _integration_config is None:
        _integration_config = SkillIntegrationConfig()
    return _integration_config

def get_integration_logger() -> SkillIntegrationLogger:
    """获取集成日志记录器单例"""
    global _integration_logger
    if _integration_logger is None:
        _integration_logger = SkillIntegrationLogger()
    return _integration_logger


if __name__ == "__main__":
    # 测试配置
    config = get_integration_config()
    logger = get_integration_logger()
    
    # 验证配置
    if config.validate_config():
        logger.log_action("system", "init", "success", "技能集成配置初始化成功")
        
        # 保存配置
        config.save_config()
        
        # 记录测试日志
        logger.log_learning("测试学习记录", "skill-integration-config.py", True)
        
        print("✅ 技能集成配置测试通过")
    else:
        print("❌ 技能集成配置验证失败")
