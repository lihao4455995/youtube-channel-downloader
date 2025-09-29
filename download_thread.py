#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
from PyQt5.QtCore import QThread, pyqtSignal
from youtube_downloader import YouTubeDownloader

class DownloadThread(QThread):
    """下载线程类"""
    
    # 信号定义
    progress_updated = pyqtSignal(int, int, str, str)  # 当前进度, 总进度, 视频标题, 状态
    download_completed = pyqtSignal()  # 下载完成
    download_failed = pyqtSignal(str)  # 下载失败
    
    def __init__(self, videos, save_path, quality="best"):
        super().__init__()
        self.videos = videos
        self.save_path = save_path
        self.quality = quality
        self.downloader = YouTubeDownloader()
        self.is_running = True
        self.current_index = 0
        
    def run(self):
        """线程主函数"""
        try:
            total_videos = len(self.videos)
            
            for i, video in enumerate(self.videos):
                if not self.is_running:
                    break
                    
                self.current_index = i
                video_title = video.get('title', 'Unknown Title')
                video_url = video.get('url', '')
                
                # 发送进度更新
                self.progress_updated.emit(i + 1, total_videos, video_title, "开始下载")
                
                try:
                    # 下载视频
                    success = self._download_single_video(video_url, video_title)
                    
                    if success:
                        status = "下载完成"
                    else:
                        status = "下载失败"
                        
                    self.progress_updated.emit(i + 1, total_videos, video_title, status)
                    
                except Exception as e:
                    error_msg = f"下载失败: {str(e)}"
                    self.progress_updated.emit(i + 1, total_videos, video_title, error_msg)
                    
                # 短暂延迟，避免过于频繁的请求
                time.sleep(1)
                
            if self.is_running:
                self.download_completed.emit()
            
        except Exception as e:
            self.download_failed.emit(str(e))
            
    def stop(self):
        """停止下载"""
        self.is_running = False
        
    def _download_single_video(self, video_url: str, video_title: str) -> bool:
        """
        下载单个视频
        
        Args:
            video_url: 视频URL
            video_title: 视频标题
            
        Returns:
            是否下载成功
        """
        try:
            # 清理文件名，移除非法字符
            safe_title = self._sanitize_filename(video_title)
            
            # 为每个视频创建独立的文件夹
            video_folder = os.path.join(self.save_path, safe_title)
            os.makedirs(video_folder, exist_ok=True)
            
            # 更新状态为下载中
            self.progress_updated.emit(
                self.current_index + 1, 
                len(self.videos), 
                video_title, 
                "下载中..."
            )
            
            # 创建标题文件
            title_file_path = os.path.join(video_folder, "标题.txt")
            try:
                with open(title_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"视频标题: {video_title}\n")
                    f.write(f"视频URL: {video_url}\n")
            except Exception as e:
                print(f"创建标题文件失败: {str(e)}")
            
            # 使用yt-dlp下载视频到独立文件夹
            success = self.downloader.download_video(
                video_url, 
                video_folder, 
                self.quality
            )
            
            return success
            
        except Exception as e:
            print(f"下载视频失败: {str(e)}")
            return False
            
    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除非法字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        # 移除Windows和Linux中的非法字符
        illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
        safe_filename = re.sub(illegal_chars, '', filename)
        
        # 移除前后空格和点
        safe_filename = safe_filename.strip('. ')
        
        # 如果文件名为空，使用默认名称
        if not safe_filename:
            safe_filename = "video"
            
        # 限制文件名长度
        if len(safe_filename) > 200:
            safe_filename = safe_filename[:200]
            
        return safe_filename