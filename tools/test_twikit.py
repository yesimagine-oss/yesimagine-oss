#!/usr/bin/env python3.8
"""測試 twikit 抓取推文"""

import asyncio
from twikit import Client

async def get_tweet(username):
    """抓取最新推文"""
    client = Client('en-US')
    
    # 使用 Gmail 登錄（需要用戶提供）
    # await client.login(
    #     auth_info_1='your_email@gmail.com',
    #     auth_info_2='your_password',
    #     username='your_username'
    # )
    
    # 先測試免登錄抓取
    try:
        tweets = await client.get_user_tweets(username, 'tweets', count=1)
        if tweets:
            return tweets[0].text
        return "無推文"
    except Exception as e:
        return f"錯誤：{str(e)[:50]}"

if __name__ == '__main__':
    tweet = asyncio.get_event_loop().run_until_complete(get_tweet('NASA'))
    print(f"@NASA: {tweet}")
