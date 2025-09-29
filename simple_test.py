#!/usr/bin/env python3
"""
简单测试主窗口
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

def test_main_window():
    """测试主窗口"""
    app = QApplication(sys.argv)
    
    # 创建主窗口但不显示
    window = MainWindow()
    
    # 测试URL验证
    test_urls = [
        "https://www.youtube.com/@gushan-ny6my/shorts",
        "https://www.youtube.com/@gushan-ny6my",
        "https://www.youtube.com/c/gushan-ny6my",
        "https://www.youtube.com/user/gushan-ny6my"
    ]
    
    print("测试URL验证:")
    for url in test_urls:
        is_valid = window.is_valid_youtube_url(url)
        channel_name = window.get_channel_name_from_url(url)
        print(f"URL: {url}")
        print(f"  有效: {is_valid}")
        print(f"  频道名: {channel_name}")
        print()
    
    print("✅ 主窗口测试完成！")

if __name__ == "__main__":
    test_main_window()