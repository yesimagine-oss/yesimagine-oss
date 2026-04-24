"""
飞书文档管理工具单元测试
Feishu Document Manager Unit Tests
"""

import unittest
from unittest.mock import Mock, patch

# 测试云文档客户端
class TestDriveClient(unittest.TestCase):
    """云文档客户端测试"""
    
    def setUp(self):
        """测试前准备"""
        from feishu_common import FeishuTokenManager
        from projects.feishu_document_manager.document_manager_v2 import DriveClient
        
        token_manager = FeishuTokenManager("test_app_id", "test_app_secret")
        self.drive = DriveClient(token_manager)
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.drive.token_manager)
        self.assertEqual(self.drive.base_url, "https://open.feishu.cn")
    
    @patch('projects.feishu_document_manager.document_manager_v2.requests.post')
    def test_create_file_success(self, mock_post):
        """测试创建文档成功"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"file_token": "test_file_token"}
        }
        mock_post.return_value = mock_response
        
        file_token = self.drive.create_file("folder_token", "测试文档")
        
        self.assertEqual(file_token, "test_file_token")
    
    @patch('projects.feishu_document_manager.document_manager_v2.requests.get')
    def test_get_file_info_success(self, mock_get):
        """测试获取文档信息成功"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"title": "测试文档", "type": "docx"}
        }
        mock_get.return_value = mock_response
        
        file_info = self.drive.get_file_info("test_file_token")
        
        self.assertEqual(file_info["title"], "测试文档")

# 测试文档管理工具
class TestDocumentManager(unittest.TestCase):
    """文档管理工具测试"""
    
    def setUp(self):
        """测试前准备"""
        from projects.feishu_document_manager.document_manager_v2 import DocumentManager
        import os
        
        # 设置测试环境变量
        os.environ["FEISHU_APP_ID"] = "test_app_id"
        os.environ["FEISHU_APP_SECRET"] = "test_app_secret"
        os.environ["FEISHU_FOLDER_TOKEN"] = "test_folder_token"
        
        self.manager = DocumentManager()
    
    def test_init(self):
        """测试初始化"""
        self.assertIsNotNone(self.manager.token_manager)
        self.assertIsNotNone(self.manager.drive)
    
    def test_log_document(self):
        """测试记录文档"""
        self.manager.log_document("test_token", "测试文档", "docx")
        
        results = self.manager.execute("SELECT * FROM documents WHERE file_token = ?", ("test_token",))
        self.assertEqual(len(results), 1)
    
    def test_get_stats(self):
        """测试获取统计"""
        self.manager.log_document("token1", "文档 1", "docx")
        self.manager.log_document("token2", "文档 2", "sheet")
        
        stats = self.manager.get_stats()
        
        self.assertEqual(stats["total"], 2)
        self.assertIn("docx", stats["by_type"])
        self.assertIn("sheet", stats["by_type"])

if __name__ == "__main__":
    unittest.main()
