#!/bin/bash

# goToken - 安裝 systemd 服務

SERVICE_FILE="/home/admin/.openclaw/workspace/goToken/goToken.service"
SYSTEMD_DIR="/etc/systemd/system"

echo "🚀 安裝 goToken systemd 服務..."

# 複製服務文件
sudo cp "$SERVICE_FILE" "$SYSTEMD_DIR/"
sudo systemctl daemon-reload

# 設置開機自啟
sudo systemctl enable goToken.service

echo "✅ 服務已安裝"
echo ""
echo "管理命令:"
echo "  sudo systemctl start goToken    # 啟動"
echo "  sudo systemctl stop goToken     # 停止"
echo "  sudo systemctl status goToken   # 狀態"
echo "  sudo systemctl disable goToken  # 禁用自啟"
echo "  journalctl -u goToken -f        # 查看日誌"
