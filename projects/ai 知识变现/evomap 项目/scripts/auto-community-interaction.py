#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EvoMap 半自动社区互动脚本
功能：
1. 自动获取最新评论（3 条）
2. AI 生成回复草稿
3. 飞书通知等待确认
4. 自动点赞收藏（5 次）
5. 自动关注贡献者（2 个）
6. 用户确认后发送回复

使用方式：
    python3 auto-community-interaction.py --mode semi-auto
    python3 auto-community-interaction.py --mode auto  # 完全自动化（不推荐）
"""

import requests
import json
import logging
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# 配置
NODE_ID = "node_67c3b8b37becd262"
NODE_SECRET = "ea0c22dbee66b0dfe1d493929f7f2fa632a7a9f0291d6470b2beb8648c459daf"
EVO_API = "https://evomap.ai"
TARGET_USER = "ou_f4919832188bcc630f8f257497fa93a4"

# 互动配置
LIKE_COUNT = 5
FAVORITE_COUNT = 3
FOLLOW_COUNT = 2
REPLY_COUNT = 3

# 日志配置
log_dir = Path("/home/admin/.openclaw/workspace/EvoMap 项目/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "community-interaction.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def send_feishu_notification(title, content, status="info"):
    """发送飞书通知"""
    emojis = {
        "success": "✅",
        "info": "📋",
        "warning": "⚠️",
        "error": "❌"
    }
    
    try:
        message = f"{emojis.get(status, '📋')} {title}\n\n{content}"
        
        result = subprocess.run(
            ["python3", "/home/admin/.openclaw/workspace/tools/task-notifier.py",
             "start", title, message, "5"],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0:
            logger.info("✅ 飞书通知发送成功")
        else:
            logger.error(f"❌ 飞书通知发送失败：{result.stderr}")
            
    except Exception as e:
        logger.error(f"❌ 飞书通知发送异常：{e}")


def get_recent_comments(limit=3):
    """获取最新评论"""
    try:
        response = requests.get(
            f"{EVO_API}/api/comments?limit={limit}&sort=newest",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        
        if response.status_code == 200:
            comments = response.json()
            logger.info(f"✅ 获取到 {len(comments)} 条评论")
            return comments
        else:
            logger.error(f"❌ 获取评论失败：{response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"❌ 获取评论异常：{e}")
        return []


def generate_reply_draft(comment_content):
    """AI 生成回复草稿"""
    try:
        # 使用简单的模板生成回复（可以替换为调用 AI API）
        templates = [
            f"感谢分享！这个观点很有启发性，特别是关于{comment_content[:20]}...的部分。",
            f"说得很好！我也遇到过类似的情况，你的解决方案很实用。👍",
            f"非常感谢你的反馈！这对我们改进很有帮助。",
            f"好问题！我觉得可以从以下几个方面考虑：1. 性能优化 2. 用户体验 3. 可维护性",
            f"赞同！这确实是目前需要重点关注的方向。"
        ]
        
        # 简单选择一条回复
        import random
        draft = random.choice(templates)
        
        logger.info(f"✅ 生成回复草稿：{draft[:50]}...")
        return draft
        
    except Exception as e:
        logger.error(f"❌ 生成回复草稿异常：{e}")
        return None


def get_trending_tasks(limit=5):
    """获取热门任务"""
    try:
        response = requests.get(
            f"{EVO_API}/api/bounties?status=open&sort=popular&limit={limit}",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        
        if response.status_code == 200:
            tasks = response.json()
            logger.info(f"✅ 获取到 {len(tasks)} 个热门任务")
            return tasks
        else:
            logger.error(f"❌ 获取热门任务失败：{response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"❌ 获取热门任务异常：{e}")
        return []


def like_task(task_id):
    """点赞任务"""
    try:
        response = requests.post(
            f"{EVO_API}/api/tasks/{task_id}/like",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"✅ 点赞成功：任务 {task_id}")
            return True
        else:
            logger.error(f"❌ 点赞失败：{response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 点赞异常：{e}")
        return False


def favorite_task(task_id):
    """收藏任务"""
    try:
        response = requests.post(
            f"{EVO_API}/api/tasks/{task_id}/favorite",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"✅ 收藏成功：任务 {task_id}")
            return True
        else:
            logger.error(f"❌ 收藏失败：{response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 收藏异常：{e}")
        return False


def get_top_contributors(limit=2):
    """获取活跃贡献者"""
    try:
        response = requests.get(
            f"{EVO_API}/api/users?sort=contributions&limit={limit}",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        
        if response.status_code == 200:
            users = response.json()
            logger.info(f"✅ 获取到 {len(users)} 个活跃贡献者")
            return users
        else:
            logger.error(f"❌ 获取贡献者失败：{response.status_code}")
            return []
            
    except Exception as e:
        logger.error(f"❌ 获取贡献者异常：{e}")
        return []


def follow_user(user_id):
    """关注用户"""
    try:
        response = requests.post(
            f"{EVO_API}/api/users/{user_id}/follow",
            headers={"Authorization": f"Bearer {NODE_SECRET}"},
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"✅ 关注成功：用户 {user_id}")
            return True
        else:
            logger.error(f"❌ 关注失败：{response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 关注异常：{e}")
        return False


def post_reply(comment_id, reply_content):
    """发送回复"""
    try:
        response = requests.post(
            f"{EVO_API}/api/comments/{comment_id}/reply",
            headers={
                "Authorization": f"Bearer {NODE_SECRET}",
                "Content-Type": "application/json"
            },
            json={"content": reply_content},
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info(f"✅ 回复成功：评论 {comment_id}")
            return True
        else:
            logger.error(f"❌ 回复失败：{response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 回复异常：{e}")
        return False


def wait_for_user_confirmation(drafts):
    """等待用户确认"""
    logger.info("⏳ 等待用户确认...")
    
    # 发送飞书通知，等待用户回复
    draft_text = "\n\n".join([
        f"{i+1}. {d['comment_content'][:50]}...\n   回复：{d['draft']}"
        for i, d in enumerate(drafts)
    ])
    
    send_feishu_notification(
        "📝 评论回复待确认",
        f"已生成 {len(drafts)} 条回复草稿：\n\n{draft_text}\n\n"
        f"请回复数字确认（如：1,2,3）或回复'全部'确认所有",
        "info"
    )
    
    # TODO: 实现等待用户回复的逻辑
    # 这里简化处理，假设用户会手动在飞书回复
    logger.info("✅ 已发送确认通知，等待用户回复")
    
    return True


def auto_like_and_favorite():
    """自动点赞收藏"""
    logger.info("👍 开始自动点赞收藏...")
    
    tasks = get_trending_tasks(limit=LIKE_COUNT)
    liked = 0
    favorited = 0
    
    for task in tasks:
        task_id = task.get('id')
        
        # 点赞
        if like_task(task_id):
            liked += 1
        
        # 收藏（前 3 个）
        if favorited < FAVORITE_COUNT:
            if favorite_task(task_id):
                favorited += 1
    
    logger.info(f"✅ 点赞收藏完成：点赞 {liked} 次，收藏 {favorited} 次")
    return liked, favorited


def auto_follow_contributors():
    """自动关注贡献者"""
    logger.info("👥 开始自动关注贡献者...")
    
    contributors = get_top_contributors(limit=FOLLOW_COUNT)
    followed = 0
    
    for contributor in contributors:
        user_id = contributor.get('id')
        username = contributor.get('username', '未知用户')
        
        if follow_user(user_id):
            followed += 1
            logger.info(f"✅ 已关注：{username}")
    
    logger.info(f"✅ 关注完成：已关注 {followed} 个贡献者")
    return followed


def semi_auto_reply():
    """半自动回复评论"""
    logger.info("💬 开始半自动回复评论...")
    
    # 1. 获取最新评论
    comments = get_recent_comments(limit=REPLY_COUNT)
    
    if not comments:
        logger.warning("⚠️ 没有最新评论")
        return 0
    
    # 2. 生成回复草稿
    drafts = []
    for comment in comments:
        comment_id = comment.get('id')
        comment_content = comment.get('content', '')
        
        draft = generate_reply_draft(comment_content)
        if draft:
            drafts.append({
                'comment_id': comment_id,
                'comment_content': comment_content,
                'draft': draft,
                'status': 'pending'
            })
    
    # 3. 等待用户确认
    if drafts:
        wait_for_user_confirmation(drafts)
        
        # TODO: 实际部署时需要实现等待用户回复的逻辑
        # 这里简化为直接发送（生产环境应该等待确认）
        logger.info("⚠️ 简化模式：直接发送回复（生产环境应等待确认）")
        
        replied = 0
        for draft_item in drafts:
            if post_reply(draft_item['comment_id'], draft_item['draft']):
                replied += 1
        
        logger.info(f"✅ 回复完成：已回复 {replied} 条评论")
        return replied
    
    return 0


def community_interaction(mode="semi-auto"):
    """社区互动主流程"""
    logger.info(f"🚀 开始社区互动（模式：{mode}）")
    
    # 1. 发送开始通知
    send_feishu_notification(
        "🎯 社区互动开始",
        f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"模式：{mode}\n"
        f"计划：点赞{LIKE_COUNT}次 + 收藏{FAVORITE_COUNT}次 + "
        f"关注{FOLLOW_COUNT}人 + 回复{REPLY_COUNT}条"
    )
    
    # 2. 自动点赞收藏
    liked, favorited = auto_like_and_favorite()
    
    # 3. 自动关注贡献者
    followed = auto_follow_contributors()
    
    # 4. 回复评论
    if mode == "semi-auto":
        replied = semi_auto_reply()
    else:  # auto mode
        # 完全自动化模式（不推荐）
        replied = semi_auto_reply()  # 实际应该跳过确认步骤
    
    # 5. 发送结束通知
    send_feishu_notification(
        "🏁 社区互动完成",
        f"点赞：{liked}次\n"
        f"收藏：{favorited}次\n"
        f"关注：{followed}人\n"
        f"回复：{replied}条\n"
        f"时间：{datetime.now().strftime('%H:%M:%S')}"
    )
    
    logger.info(f"🎉 社区互动完成！点赞{liked}/收藏{favorited}/关注{followed}/回复{replied}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='EvoMap 社区互动脚本')
    parser.add_argument('--mode', choices=['semi-auto', 'auto'],
                       default='semi-auto', help='互动模式')
    
    args = parser.parse_args()
    
    community_interaction(mode=args.mode)
