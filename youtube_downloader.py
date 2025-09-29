#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import json
import subprocess
import sys
from datetime import datetime
from typing import List, Dict, Optional

class YouTubeDownloader:
    """YouTube视频下载器类"""
    
    def __init__(self):
        self.yt_dlp_path = self._get_yt_dlp_path()
        
    def _get_yt_dlp_path(self) -> str:
        """获取yt-dlp路径"""
        # 首先尝试直接运行yt-dlp
        try:
            subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
            return 'yt-dlp'
        except (subprocess.CalledProcessError, FileNotFoundError):
            # 如果失败，尝试使用python -m yt_dlp
            try:
                subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                             capture_output=True, check=True)
                return f'{sys.executable} -m yt_dlp'
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise RuntimeError("未找到yt-dlp，请先安装: pip install yt-dlp")
                
    def get_channel_videos(self, channel_url: str) -> List[Dict]:
        """
        获取频道视频列表
        
        Args:
            channel_url: YouTube频道URL
            
        Returns:
            视频信息列表
        """
        try:
            # 使用yt-dlp获取频道信息
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--print-json',
                '--skip-download',
                channel_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                raise RuntimeError(f"获取频道信息失败: {result.stderr}")
                
            videos = []
            lines = result.stdout.strip().split('\n')
            
            for line in lines:
                if line.strip():
                    try:
                        video_info = json.loads(line)
                        
                        # 提取视频信息
                        video_data = {
                            'id': video_info.get('id', ''),
                            'title': video_info.get('title', 'Unknown Title'),
                            'url': f"https://www.youtube.com/watch?v={video_info.get('id', '')}",
                            'duration': self._format_duration(video_info.get('duration', 0)),
                            'upload_date': self._format_upload_date(video_info.get('upload_date', '')),
                            'view_count': video_info.get('view_count', 0),
                            'channel': video_info.get('channel', 'Unknown Channel')
                        }
                        
                        videos.append(video_data)
                        
                    except json.JSONDecodeError:
                        continue
                        
            return videos
            
        except Exception as e:
            raise RuntimeError(f"获取频道视频失败: {str(e)}")
            
    def download_video(self, video_url: str, output_path: str, quality: str = "best") -> bool:
        """
        下载单个视频
        
        Args:
            video_url: 视频URL
            output_path: 输出路径
            quality: 视频质量
            
        Returns:
            是否下载成功
        """
        try:
            # 构建输出模板
            output_template = os.path.join(output_path, "%(title)s.%(ext)s")
            
            # 构建质量参数
            format_str = self._get_format_string(quality)
            
            cmd = [
                'yt-dlp',
                '-f', format_str,
                '--output', output_template,
                '--no-playlist',
                '--write-info-json',
                '--write-thumbnail',
                video_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True
            else:
                raise RuntimeError(f"下载失败: {result.stderr}")
                
        except Exception as e:
            raise RuntimeError(f"下载视频失败: {str(e)}")
            
    def get_video_info(self, video_url: str) -> Dict:
        """
        获取单个视频信息
        
        Args:
            video_url: 视频URL
            
        Returns:
            视频信息
        """
        try:
            cmd = [
                'yt-dlp',
                '--print-json',
                '--skip-download',
                video_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                raise RuntimeError(f"获取视频信息失败: {result.stderr}")
                
            video_info = json.loads(result.stdout.strip())
            
            return {
                'id': video_info.get('id', ''),
                'title': video_info.get('title', 'Unknown Title'),
                'description': video_info.get('description', ''),
                'duration': video_info.get('duration', 0),
                'upload_date': video_info.get('upload_date', ''),
                'view_count': video_info.get('view_count', 0),
                'like_count': video_info.get('like_count', 0),
                'channel': video_info.get('channel', ''),
                'channel_id': video_info.get('channel_id', ''),
                'thumbnail': video_info.get('thumbnail', ''),
                'formats': video_info.get('formats', [])
            }
            
        except Exception as e:
            raise RuntimeError(f"获取视频信息失败: {str(e)}")
            
    def _format_duration(self, seconds) -> str:
        """格式化时长"""
        if not seconds:
            return "Unknown"
        
        # 确保转换为整数
        seconds = int(float(seconds))
            
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
            
    def _format_upload_date(self, upload_date: str) -> str:
        """格式化上传日期"""
        if not upload_date:
            return "Unknown"
            
        try:
            # YouTube日期格式通常是 YYYYMMDD
            if len(str(upload_date)) == 8:
                date_obj = datetime.strptime(str(upload_date), "%Y%m%d")
                return date_obj.strftime("%Y-%m-%d")
            return str(upload_date)
        except:
            return str(upload_date)
            
    def _get_format_string(self, quality: str) -> str:
        """获取格式字符串"""
        quality_map = {
            "最高质量": "best",
            "720p": "best[height<=720]",
            "480p": "best[height<=480]",
            "360p": "best[height<=360]",
            "仅音频": "bestaudio"
        }
        
        return quality_map.get(quality, "best")
        
    def extract_channel_id(self, channel_url: str) -> str:
        """
        从频道URL中提取频道ID
        
        Args:
            channel_url: 频道URL
            
        Returns:
            频道ID
        """
        # 首先移除路径中的/shorts、/videos等后缀
        base_url = re.sub(r'/shorts$|/videos$|/featured$', '', channel_url)
        
        patterns = [
            r'youtube\.com/channel/([\w-]+)',
            r'youtube\.com/c/([\w-]+)',
            r'youtube\.com/@([\w-]+)',
            r'youtube\.com/user/([\w-]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, base_url)
            if match:
                return match.group(1)
                
        raise ValueError(f"无法从URL中提取频道ID: {channel_url}")
        
    def get_channel_info(self, channel_url: str) -> Dict:
        """
        获取频道信息
        
        Args:
            channel_url: 频道URL
            
        Returns:
            频道信息
        """
        try:
            cmd = [
                'yt-dlp',
                '--print-json',
                '--skip-download',
                channel_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                raise RuntimeError(f"获取频道信息失败: {result.stderr}")
                
            channel_info = json.loads(result.stdout.strip())
            
            return {
                'id': channel_info.get('channel_id', ''),
                'title': channel_info.get('channel', ''),
                'description': channel_info.get('description', ''),
                'subscriber_count': channel_info.get('subscriber_count', 0),
                'video_count': channel_info.get('playlist_count', 0)
            }
            
        except Exception as e:
            raise RuntimeError(f"获取频道信息失败: {str(e)}")