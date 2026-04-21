#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天天基金 Skills 客户端
支持调用天天基金 API 查询基金信息和条件选基
"""

import os
import sys
import json
import requests
from typing import Optional, Dict, Any

# API 配置
TTFUND_GATEWAY_URL = "https://skills.tiantianfunds.com/ai-smart-skill-service/openapi/skill/invoke"

# Skill 定义
SKILLS = {
    "fund_info": {
        "skill_id": "FUND_BASE_INFOS",
        "skill_name": "天天基金信息 skill",
        "version": "1.0.0",
        "description": "基金基础信息查询"
    },
    "fund_select": {
        "skill_id": "FUND_CONDITION_SELECT",
        "skill_name": "天天条件选基 skill",
        "version": "1.0.0",
        "description": "条件选基"
    }
}


def check_api_key() -> Optional[str]:
    """检查 API Key 配置"""
    api_key = os.environ.get("TTFUND_APIKEY")
    if not api_key:
        print("⚠️  未检测到环境变量 TTFUND_APIKEY")
        print("请先前往天天基金 App 搜索 skills 获取 apikey")
        print("配置方式：export TTFUND_APIKEY='your_api_key'")
        return None
    return api_key


def invoke_skill(skill_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    调用天天基金 Skill
    
    Args:
        skill_type: 技能类型 ("fund_info" 或 "fund_select")
        params: 请求参数
    
    Returns:
        API 响应结果
    """
    # 检查 API Key
    api_key = check_api_key()
    if not api_key:
        return {
            "success": False,
            "error": "缺少 TTFUND_APIKEY 环境变量"
        }
    
    # 获取技能配置
    if skill_type not in SKILLS:
        return {
            "success": False,
            "error": f"未知的技能类型：{skill_type}"
        }
    
    skill_config = SKILLS[skill_type]
    
    # 构建请求体
    payload = {
        "skill_id": skill_config["skill_id"],
        "_skill_version": skill_config["version"],
        **params
    }
    
    # 设置请求头
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # 发送请求
        response = requests.post(
            TTFUND_GATEWAY_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # 检查 HTTP 状态码
        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP 错误：{response.status_code}",
                "status_code": response.status_code
            }
        
        # 解析响应
        result = response.json()
        
        # 检查业务错误码 (网关响应格式)
        if result.get("code") != 0:
            return {
                "success": False,
                "error": result.get("message") or f"网关错误：{result.get('code')}",
                "raw_result": result
            }
        
        # 检查嵌套的业务数据
        # 响应结构：result -> data (包含 skill_id, skill_name, raw_result, field_interpretations)
        skill_data = result.get("data", {})
        raw_result = skill_data.get("raw_result", {})
        
        if skill_type == "fund_info":
            # 基金信息接口使用 errorCode (嵌套在 raw_result.body 中)
            body = raw_result.get("body", {})
            if body.get("errorCode") != 0:
                return {
                    "success": False,
                    "error": body.get("firstError") or f"业务错误：{body.get('errorCode')}",
                    "raw_result": result
                }
            # 保存 body 到返回结果中供后续使用
            return {
                "success": True,
                "skill_id": skill_config["skill_id"],
                "skill_name": skill_config["skill_name"],
                "data": body  # 直接返回 body
            }
        elif skill_type == "fund_select":
            # 条件选基接口使用 ErrCode (也在 body 里面)
            body = raw_result.get("body", {})
            if body.get("ErrCode") != 0:
                return {
                    "success": False,
                    "error": body.get("Message") or f"业务错误：{body.get('ErrCode')}",
                    "raw_result": result
                }
            # 保存 body 到返回结果中供后续使用
            return {
                "success": True,
                "skill_id": skill_config["skill_id"],
                "skill_name": skill_config["skill_name"],
                "data": body  # 直接返回 body
            }
        
        return {
            "success": True,
            "skill_id": skill_config["skill_id"],
            "skill_name": skill_config["skill_name"],
            "data": result
        }
        
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "请求超时，请稍后重试"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"网络错误：{str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"响应解析失败：{str(e)}"
        }


def query_fund_info(fcode: str) -> Dict[str, Any]:
    """
    查询基金基础信息
    
    Args:
        fcode: 基金代码，例如 "000006"
    
    Returns:
        基金信息
    """
    return invoke_skill("fund_info", {"fcode": fcode})


def select_funds(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    条件选基
    
    Args:
        params: 筛选参数 (参考文档中的参数说明)
    
    Returns:
        筛选结果
    """
    return invoke_skill("fund_select", params)


def format_fund_info(result: Dict[str, Any]) -> str:
    """格式化基金信息输出"""
    if not result.get("success"):
        return f"❌ 查询失败：{result.get('error')}"
    
    # 现在 data 直接是 body
    body = result.get("data", {})
    fund_data = body.get("data", [])
    
    if not fund_data:
        return "❌ 未找到基金信息"
    
    # 提取核心字段
    fund = fund_data[0] if isinstance(fund_data, list) else fund_data
    
    output = []
    output.append(f"✅ {result.get('skill_name', '天天基金信息 skill')}")
    output.append("=" * 50)
    output.append(f"基金代码：{fund.get('FCODE', 'N/A')}")
    output.append(f"基金简称：{fund.get('SHORTNAME', 'N/A')}")
    output.append(f"基金公司：{fund.get('JJGS', 'N/A')}")
    output.append(f"基金类型：{fund.get('FTYPE', 'N/A')}")
    output.append(f"单位净值：{fund.get('DWJZ', 'N/A')}")
    output.append(f"累计净值：{fund.get('LJJZ', 'N/A')}")
    output.append(f"风险等级：{fund.get('RISKLEVEL', 'N/A')}")
    output.append(f"成立日期：{fund.get('ESTABDATE', 'N/A')}")
    output.append(f"净值日期：{fund.get('FSRQ', 'N/A')}")
    output.append(f"近一周收益：{fund.get('SYL_Z', 'N/A')}%")
    output.append(f"近一年收益：{fund.get('SYL_1N', 'N/A')}%")
    output.append(f"成立以来收益：{fund.get('SYL_LN', 'N/A')}%")
    output.append(f"波动率：{fund.get('STDDEV1', 'N/A')}")
    output.append(f"最大回撤：{fund.get('MAXRETRA1', 'N/A')}")
    output.append(f"日涨跌幅：{fund.get('RZDF', 'N/A')}%")
    
    return "\n".join(output)


def format_fund_select(result: Dict[str, Any]) -> str:
    """格式化条件选基输出"""
    if not result.get("success"):
        return f"❌ 筛选失败：{result.get('error')}"
    
    # 现在 data 直接是 body
    body = result.get("data", {})
    total_count = body.get("TotalCount", 0)
    fund_list = body.get("Data", [])
    
    output = []
    output.append(f"✅ {result.get('skill_name', '天天条件选基 skill')}")
    output.append("=" * 50)
    output.append(f"符合条件的基金数量：{total_count}")
    output.append("")
    
    if not fund_list:
        output.append("❌ 未找到符合条件的基金")
        return "\n".join(output)
    
    # 显示前 10 只基金
    for i, fund in enumerate(fund_list[:10], 1):
        output.append(f"{i}. {fund.get('fundName', 'N/A')} ({fund.get('fundCode', 'N/A')})")
        output.append(f"   公司：{fund.get('company', 'N/A')}")
        output.append(f"   类型：{fund.get('ftype', 'N/A')}")
        output.append(f"   规模：{fund.get('fundSize', 'N/A')}")
        output.append(f"   评级：{fund.get('fundLevel', 'N/A')}星")
        output.append(f"   近 1 年收益：{fund.get('yearSyl', 'N/A')}%")
        output.append(f"   风险等级：{fund.get('riskLevel', 'N/A')}")
        output.append(f"   日涨跌：{fund.get('daySyl', 'N/A')}%")
        output.append("")
    
    if total_count > 10:
        output.append(f"... 还有 {total_count - 10} 只基金")
    
    return "\n".join(output)


# CLI 入口
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="天天基金 Skills 客户端")
    parser.add_argument("action", choices=["info", "select"], help="操作类型")
    parser.add_argument("--fcode", help="基金代码 (info 模式)")
    parser.add_argument("--params", help="筛选参数 JSON (select 模式)")
    
    args = parser.parse_args()
    
    if args.action == "info":
        if not args.fcode:
            print("❌ 请提供基金代码：--fcode 000006")
            sys.exit(1)
        result = query_fund_info(args.fcode)
        print(format_fund_info(result))
    
    elif args.action == "select":
        params = {}
        if args.params:
            try:
                params = json.loads(args.params)
            except json.JSONDecodeError:
                print("❌ 参数格式错误，需要有效的 JSON")
                sys.exit(1)
        result = select_funds(params)
        print(format_fund_select(result))
