#!/usr/bin/env python3
"""
腾讯企业邮未读邮件检查工具
按日期倒序获取最新未读邮件（与网页邮箱一致）
"""

import imaplib
import email
from email.header import decode_header
import sys

# 配置
EMAIL = 'red@unvw.com'
PASSWORD = '6NWETmGDsE2RWfiC'
IMAP_SERVER = 'imap.exmail.qq.com'
IMAP_PORT = 993

def check_unread(limit=1, show_body=False):
    """
    检查未读邮件
    
    Args:
        limit: 获取邮件数量
        show_body: 是否显示正文
    """
    try:
        # 连接 IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select('INBOX')
        
        # 搜索未读邮件
        status, messages = mail.search(None, 'UNSEEN')
        
        if not messages[0]:
            print('✅ 没有未读邮件')
            mail.close()
            mail.logout()
            return
        
        msg_ids = messages[0].split()
        total = len(msg_ids)
        
        print(f'📬 未读邮件总数：{total}\n')
        
        # 按日期倒序（最新的在前）
        # IMAP 返回的是 ID 递增，所以反转列表
        msg_ids = sorted(msg_ids, key=lambda x: int(x), reverse=True)
        
        for i, msg_id in enumerate(msg_ids[:limit]):
            status, msg_data = mail.fetch(msg_id, '(RFC822)')
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # 解码主题
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or 'utf-8')
                    
                    # 解码发件人
                    from_header, encoding = decode_header(msg['From'])[0]
                    if isinstance(from_header, bytes):
                        from_header = from_header.decode(encoding or 'utf-8')
                    
                    # 日期
                    date_header = msg['Date']
                    
                    print('='*70)
                    print(f'📬 第 {i+1} 封未读邮件')
                    print('='*70)
                    print(f'📤 发件人：{from_header}')
                    print(f'📝 主题：{subject}')
                    print(f'📅 日期：{date_header}')
                    print()
                    
                    if show_body:
                        # 获取正文
                        body = ''
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get('Content-Disposition'))
                                
                                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                                    try:
                                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                        break
                                    except:
                                        pass
                                elif content_type == 'text/html' and 'attachment' not in content_disposition:
                                    try:
                                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                        # 清理 HTML
                                        import re
                                        body = re.sub(r'<[^>]+>', '', body)
                                        break
                                    except:
                                        pass
                        else:
                            try:
                                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                            except:
                                body = msg.get_payload()
                        
                        if body:
                            print('📄 正文:')
                            print('-'*70)
                            print(body[:1000])
                            if len(body) > 1000:
                                print('... (内容过长，仅显示前 1000 字)')
                            print('-'*70)
                        else:
                            print('📄 正文：(无文本内容)')
                        
                        print()
                    
                    print('='*70)
                    print()
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f'❌ 错误：{e}')
        sys.exit(1)

def confirm_permanent_delete():
    """
    彻底删除二次确认
    
    Returns:
        bool: 用户是否确认
    """
    print()
    print('⚠️  ⚠️  ⚠️  警告：彻底删除  ⚠️  ⚠️  ⚠️')
    print('='*60)
    print('此操作将永久删除邮件，无法恢复！')
    print('='*60)
    print()
    response = input('请输入 "确认" 继续彻底删除（或按回车取消）: ')
    return response.strip() == '确认'

def delete_email(msg_id, permanent=False, skip_confirm=False):
    """
    删除邮件
    
    Args:
        msg_id: 邮件 ID
        permanent: 是否彻底删除（默认 False=移动到垃圾箱）
        skip_confirm: 跳过确认（仅用于测试）
    """
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select('INBOX')
        
        # 获取邮件信息
        status, msg_data = mail.fetch(msg_id, '(RFC822.HEADER)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject = msg['Subject']
                from_header = msg['From']
                
                print('='*60)
                print('🗑️  准备删除:')
                print('='*60)
                print(f'📤 发件人：{from_header}')
                print(f'📝 主题：{subject}')
                print('='*60)
                print()
        
        # 仅彻底删除需要二次确认
        if permanent and not skip_confirm:
            if not confirm_permanent_delete():
                print('❌ 已取消删除')
                mail.close()
                mail.logout()
                return
        
        if permanent:
            # 彻底删除
            print()
            print('⚠️  正在彻底删除...')
            mail.store(msg_id, '+FLAGS', '\\Deleted')
            mail.expunge()
            print('✅ 邮件已彻底删除（无法恢复）')
        else:
            # 移动到垃圾箱
            print()
            print('📦 正在移动到垃圾箱...')
            try:
                # 复制到垃圾箱（腾讯企业邮用 Junk 文件夹）
                mail.copy(msg_id, 'Junk')
                # 从收件箱删除
                mail.store(msg_id, '+FLAGS', '\\Deleted')
                mail.expunge()
                print('✅ 邮件已移动到垃圾箱（可恢复）')
            except Exception as e:
                # 如果 Junk 文件夹不存在，尝试其他名称
                for folder in ['Trash', 'Deleted Items', 'Deleted Messages', 'Spam']:
                    try:
                        mail.copy(msg_id, folder)
                        mail.store(msg_id, '+FLAGS', '\\Deleted')
                        mail.expunge()
                        print(f'✅ 邮件已移动到 {folder}（可恢复）')
                        break
                    except:
                        continue
                else:
                    # 都没有，直接标记删除
                    print('⚠️  垃圾箱文件夹不存在，改为标记删除')
                    mail.store(msg_id, '+FLAGS', '\\Deleted')
                    mail.expunge()
                    print('✅ 邮件已标记删除')
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f'❌ 错误：{e}')
        sys.exit(1)

def delete_latest(permanent=False):
    """删除最新一封未读邮件"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select('INBOX')
        
        status, messages = mail.search(None, 'UNSEEN')
        msg_ids = messages[0].split()
        
        if not msg_ids:
            print('✅ 没有未读邮件')
            mail.close()
            mail.logout()
            return
        
        # 按日期倒序（最新的在前）
        msg_ids = sorted(msg_ids, key=lambda x: int(x), reverse=True)
        latest_msg_id = msg_ids[0]
        
        delete_email(latest_msg_id, permanent=permanent)
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f'❌ 错误：{e}')
        sys.exit(1)

def check_junk():
    """检查垃圾箱内容"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select('INBOX')
        
        print('📂 检查垃圾箱...\n')
        
        # 尝试打开 Junk 文件夹
        junk_folder = 'Junk'
        try:
            mail.select(junk_folder)
        except:
            for folder in ['Trash', 'Deleted Items', 'Deleted Messages', 'Spam']:
                try:
                    mail.select(folder)
                    junk_folder = folder
                    break
                except:
                    continue
            else:
                print('❌ 找不到垃圾箱文件夹')
                mail.close()
                mail.logout()
                return
        
        status, messages = mail.search(None, 'ALL')
        msg_ids = messages[0].split()
        count = len(msg_ids)
        
        print(f'🗑️  垃圾箱 ({junk_folder}): {count} 封邮件')
        print()
        
        if count > 0:
            msg_ids = sorted(msg_ids, key=lambda x: int(x), reverse=True)
            print('='*70)
            print('📋 最新 10 封邮件:')
            print('='*70)
            
            for i, msg_id in enumerate(msg_ids[:10]):
                status, msg_data = mail.fetch(msg_id, '(RFC822.HEADER)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg['Subject'])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or 'utf-8')
                        from_header = msg['From'][:50]
                        date_header = msg['Date']
                        print(f'{i+1}. 📤 {from_header}')
                        print(f'   📝 {subject[:60]}')
                        print(f'   📅 {date_header}')
                        print()
        
        mail.close()
        mail.logout()
        
    except Exception as e:
        print(f'❌ 错误：{e}')
        sys.exit(1)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='检查腾讯企业邮未读邮件')
    parser.add_argument('-n', '--limit', type=int, default=1, help='获取邮件数量')
    parser.add_argument('-b', '--body', action='store_true', help='显示正文内容')
    parser.add_argument('-d', '--delete', action='store_true', help='删除最新一封未读邮件（移动到垃圾箱）')
    parser.add_argument('-D', '--delete-permanent', action='store_true', help='彻底删除最新一封未读邮件（无法恢复）')
    parser.add_argument('-j', '--junk', action='store_true', help='检查垃圾箱内容')
    args = parser.parse_args()
    
    if args.junk:
        check_junk()
    elif args.delete_permanent:
        print('⚠️  警告：彻底删除无法恢复！\n')
        delete_latest(permanent=True)
    elif args.delete:
        # 删除前先检查垃圾箱
        check_junk()
        print()
        delete_latest(permanent=False)
    else:
        check_unread(limit=args.limit, show_body=args.body)
