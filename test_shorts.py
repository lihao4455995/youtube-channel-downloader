#!/usr/bin/env python3
"""
测试YouTube Shorts链接解析和下载
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from youtube_downloader import YouTubeDownloader

def test_shorts_url():
    """测试YouTube Shorts链接"""
    downloader = YouTubeDownloader()
    
    # 测试的YouTube Shorts链接
    test_urls = [
        "https://www.youtube.com/@gushan-ny6my/shorts",
        "https://www.youtube.com/@gushan-ny6my",
        "https://www.youtube.com/c/gushan-ny6my",
        "https://www.youtube.com/channel/UC1234567890abcdef"
    ]
    
    for url in test_urls:
        print(f"\n{'='*60}")
        print(f"测试URL: {url}")
        print(f"{'='*60}")
        
        try:
            # 测试URL验证
            is_valid = downloader.is_valid_youtube_url(url) if hasattr(downloader, 'is_valid_youtube_url') else True
            print(f"URL验证: {'✓' if is_valid else '✗'}")
            
            # 测试频道ID提取
            try:
                channel_id = downloader.extract_channel_id(url)
                print(f"频道ID: {channel_id}")
            except Exception as e:
                print(f"频道ID提取失败: {e}")
                channel_id = None
            
            # 测试获取频道视频
            try:
                print("正在获取频道视频列表...")
                videos = downloader.get_channel_videos(url)
                print(f"找到 {len(videos)} 个视频")
                
                if videos:
                    print("前3个视频:")
                    for i, video in enumerate(videos[:3]):
                        print(f"  {i+1}. {video.get('title', 'Unknown')} - {video.get('duration', 'Unknown')}")
                        print(f"     URL: {video.get('url', 'Unknown')}")
                        
            except Exception as e:
                print(f"获取频道视频失败: {e}")
                
                # 尝试获取单个视频信息（如果是单个视频URL）
                try:
                    print("尝试作为单个视频获取信息...")
                    video_info = downloader.get_video_info(url)
                    print(f"视频标题: {video_info.get('title', 'Unknown')}")
                    print(f"视频时长: {video_info.get('duration', 'Unknown')}")
                    print(f"频道名称: {video_info.get('channel', 'Unknown')}")
                except Exception as e2:
                    print(f"作为单个视频也失败: {e2}")
                    
        except Exception as e:
            print(f"测试失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("YouTube Shorts链接测试工具")
    print("="*60)
    test_shorts_url()