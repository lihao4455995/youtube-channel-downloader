#!/usr/bin/env python3
"""
测试中文YouTube频道链接的视频时长和上传日期获取
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main_window import MainWindow
from youtube_downloader import YouTubeDownloader

def test_chinese_url():
    """测试中文URL的视频信息获取"""
    
    # 测试中文URL
    chinese_url = "https://www.youtube.com/@%E7%B5%A6%E4%BD%A0%E7%9A%84%E5%BF%839/shorts"
    
    print("测试中文YouTube频道链接")
    print("="*60)
    print(f"URL: {chinese_url}")
    print("="*60)
    
    # 测试YouTubeDownloader
    downloader = YouTubeDownloader()
    
    try:
        # 测试频道ID提取
        channel_id = downloader.extract_channel_id(chinese_url)
        print(f"✓ 频道ID: {channel_id}")
        
        # 测试获取频道视频
        print("正在获取视频列表...")
        videos = downloader.get_channel_videos(chinese_url)
        print(f"✓ 找到 {len(videos)} 个视频")
        
        if videos:
            print("\n前5个视频的详细信息:")
            for i, video in enumerate(videos[:5]):
                print(f"\n视频 {i+1}:")
                print(f"  标题: {video.get('title', 'Unknown')}")
                print(f"  时长: {video.get('duration', 'Unknown')}")
                print(f"  上传日期: {video.get('upload_date', 'Unknown')}")
                print(f"  观看次数: {video.get('view_count', 'Unknown')}")
                print(f"  URL: {video.get('url', 'Unknown')}")
                
                # 检查是否有缺失信息
                missing_info = []
                if video.get('duration') == 'Unknown':
                    missing_info.append('时长')
                if video.get('upload_date') == 'Unknown':
                    missing_info.append('上传日期')
                
                if missing_info:
                    print(f"  ⚠️  缺失信息: {', '.join(missing_info)}")
                else:
                    print(f"  ✅ 信息完整")
        
        # 测试MainWindow的URL验证
        print("\n" + "="*60)
        print("测试MainWindow的URL验证功能")
        
        # 创建MainWindow实例（不显示界面）
        from PyQt5.QtWidgets import QApplication
        app = QApplication(sys.argv)
        main_window = MainWindow()
        
        # 测试URL验证
        is_valid = main_window.is_valid_youtube_url(chinese_url)
        print(f"URL验证结果: {'✓ 有效' if is_valid else '✗ 无效'}")
        
        # 测试频道名提取
        channel_name = main_window.get_channel_name_from_url(chinese_url)
        print(f"提取的频道名: {channel_name}")
        
        print("\n✅ 中文URL测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chinese_url()