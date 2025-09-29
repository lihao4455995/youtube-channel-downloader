#!/usr/bin/env python3
"""
测试视频时长和上传日期获取
"""

import sys
import os
import json
import subprocess
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from youtube_downloader import YouTubeDownloader

def test_video_info_methods():
    """测试不同的视频信息获取方法"""
    downloader = YouTubeDownloader()
    
    # 测试URL
    test_url = "https://www.youtube.com/@gushan-ny6my/shorts"
    
    print(f"测试URL: {test_url}")
    print("="*60)
    
    try:
        # 方法1: 使用当前的get_channel_videos方法
        print("方法1: 使用--flat-playlist参数")
        cmd_flat = [
            'yt-dlp',
            '--flat-playlist',
            '--print-json',
            '--skip-download',
            test_url
        ]
        
        result_flat = subprocess.run(cmd_flat, capture_output=True, text=True, encoding='utf-8')
        
        if result_flat.returncode == 0:
            lines = result_flat.stdout.strip().split('\n')
            if lines and lines[0].strip():
                video_info = json.loads(lines[0])
                print(f"flat-playlist返回的数据结构:")
                for key, value in video_info.items():
                    print(f"  {key}: {value}")
                print(f"  duration: {video_info.get('duration', '无')}")
                print(f"  upload_date: {video_info.get('upload_date', '无')}")
        
        print("\n" + "="*60)
        
        # 方法2: 不使用--flat-playlist参数
        print("方法2: 不使用--flat-playlist参数")
        cmd_full = [
            'yt-dlp',
            '--print-json',
            '--skip-download',
            '--playlist-end', '3',  # 只获取前3个视频
            test_url
        ]
        
        result_full = subprocess.run(cmd_full, capture_output=True, text=True, encoding='utf-8')
        
        if result_full.returncode == 0:
            lines = result_full.stdout.strip().split('\n')
            print(f"获取到 {len(lines)} 个视频的详细信息")
            
            for i, line in enumerate(lines[:3]):  # 只显示前3个
                if line.strip():
                    try:
                        video_info = json.loads(line)
                        print(f"\n视频 {i+1}:")
                        print(f"  标题: {video_info.get('title', '无')}")
                        print(f"  duration: {video_info.get('duration', '无')}")
                        print(f"  upload_date: {video_info.get('upload_date', '无')}")
                        print(f"  view_count: {video_info.get('view_count', '无')}")
                        
                        # 检查所有可用的字段
                        available_fields = [key for key in video_info.keys() if 'duration' in key.lower() or 'date' in key.lower() or 'time' in key.lower()]
                        if available_fields:
                            print(f"  相关字段: {available_fields}")
                            
                    except json.JSONDecodeError:
                        continue
        
        print("\n" + "="*60)
        
        # 方法3: 获取单个视频的信息
        print("方法3: 获取单个视频信息")
        # 先用flat方法获取一个视频的ID
        if result_flat.returncode == 0 and lines and lines[0].strip():
            video_info = json.loads(lines[0])
            video_id = video_info.get('id', '')
            
            if video_id:
                single_video_url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"测试单个视频: {single_video_url}")
                
                try:
                    single_info = downloader.get_video_info(single_video_url)
                    print(f"  标题: {single_info.get('title', '无')}")
                    print(f"  duration: {single_info.get('duration', '无')}")
                    print(f"  upload_date: {single_info.get('upload_date', '无')}")
                    print(f"  view_count: {single_info.get('view_count', '无')}")
                except Exception as e:
                    print(f"  获取单个视频信息失败: {e}")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_video_info_methods()