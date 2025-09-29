#!/usr/bin/env python3
"""
快速测试YouTube Shorts链接
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from youtube_downloader import YouTubeDownloader

def test_shorts():
    """简单测试YouTube Shorts链接"""
    downloader = YouTubeDownloader()
    
    # 测试YouTube Shorts链接
    test_url = "https://www.youtube.com/@gushan-ny6my/shorts"
    
    print(f"测试URL: {test_url}")
    
    try:
        # 测试频道ID提取
        channel_id = downloader.extract_channel_id(test_url)
        print(f"✓ 频道ID: {channel_id}")
        
        # 测试获取前几个视频
        print("正在获取视频列表...")
        videos = downloader.get_channel_videos(test_url)
        print(f"✓ 找到 {len(videos)} 个视频")
        
        if videos:
            print("前3个视频:")
            for i, video in enumerate(videos[:3]):
                title = video.get('title', 'Unknown')
                duration = video.get('duration', 'Unknown')
                upload_date = video.get('upload_date', 'Unknown')
                print(f"  {i+1}. {title}")
                print(f"     时长: {duration}, 上传日期: {upload_date}")
                
        print("\n✅ YouTube Shorts链接测试成功！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_shorts()