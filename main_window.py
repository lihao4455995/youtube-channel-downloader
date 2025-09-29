#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import threading
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, 
                             QProgressBar, QFileDialog, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QSplitter, QGroupBox, QCheckBox, QComboBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont
from youtube_downloader import YouTubeDownloader
from download_thread import DownloadThread

class ParseThread(QThread):
    """解析线程类"""
    parse_completed = pyqtSignal(list)  # 解析完成信号
    parse_failed = pyqtSignal(str)      # 解析失败信号
    
    def __init__(self, url, downloader):
        super().__init__()
        self.url = url
        self.downloader = downloader
    
    def run(self):
        """线程主函数"""
        try:
            videos = self.downloader.get_channel_videos(self.url)
            self.parse_completed.emit(videos)
        except Exception as e:
            error_msg = f"解析频道失败: {str(e)}"
            import traceback
            detailed_error = f"{error_msg}\n详细错误: {traceback.format_exc()}"
            self.parse_failed.emit(detailed_error)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.downloader = YouTubeDownloader()
        self.videos = []
        self.parse_thread = None  # 保存解析线程引用self.download_thread = None
        self.downloaded_videos = []
        
        self.init_ui()
        self.connect_signals()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("YouTube频道视频下载器")
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧面板
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右侧面板
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(splitter)
        
        # 状态栏
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("就绪")
        
    def create_left_panel(self):
        """创建左侧面板"""
        group_box = QGroupBox("下载设置")
        layout = QVBoxLayout()
        
        # URL输入区域
        url_layout = QVBoxLayout()
        url_label = QLabel("YouTube频道URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入YouTube频道URL，例如: https://www.youtube.com/@channelname")
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        
        # 解析按钮
        self.parse_btn = QPushButton("解析频道")
        self.parse_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        # 下载设置
        settings_layout = QVBoxLayout()
        
        # 保存路径
        path_layout = QHBoxLayout()
        path_label = QLabel("保存路径:")
        self.path_input = QLineEdit()
        self.path_input.setText(os.path.join(os.path.expanduser("~"), "Downloads", "YouTubeVideos"))
        self.browse_btn = QPushButton("浏览...")
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        
        # 视频质量选择
        quality_layout = QHBoxLayout()
        quality_label = QLabel("视频质量:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["最高质量", "720p", "480p", "360p", "仅音频"])
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)
        
        # 下载选项
        self.download_all_cb = QCheckBox("下载所有视频")
        self.download_all_cb.setChecked(True)
        self.create_folder_cb = QCheckBox("为每个频道创建文件夹")
        self.create_folder_cb.setChecked(True)
        
        settings_layout.addLayout(path_layout)
        settings_layout.addLayout(quality_layout)
        settings_layout.addWidget(self.download_all_cb)
        settings_layout.addWidget(self.create_folder_cb)
        
        # 下载控制按钮
        button_layout = QHBoxLayout()
        self.download_btn = QPushButton("开始下载")
        self.download_btn.setEnabled(False)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        
        self.stop_btn = QPushButton("停止下载")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.stop_btn)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        layout.addLayout(url_layout)
        layout.addWidget(self.parse_btn)
        layout.addLayout(settings_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress_bar)
        layout.addStretch()
        
        group_box.setLayout(layout)
        return group_box
        
    def create_right_panel(self):
        """创建右侧面板"""
        group_box = QGroupBox("视频列表")
        layout = QVBoxLayout()
        
        # 视频列表表格
        self.video_table = QTableWidget()
        self.video_table.setColumnCount(5)
        self.video_table.setHorizontalHeaderLabels(["选择", "标题", "时长", "上传日期", "状态"])
        self.video_table.horizontalHeader().setStretchLastSection(True)
        self.video_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.video_table.setAlternatingRowColors(True)
        
        # 设置选择列的宽度
        self.video_table.setColumnWidth(0, 50)  # 选择列较窄
        
        # 日志输出
        self.log_output = QTextEdit()
        self.log_output.setMaximumHeight(200)
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Consolas", 9))
        
        # 添加选择控制按钮
        select_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("全选")
        self.select_all_btn.clicked.connect(self.select_all_videos)
        self.select_none_btn = QPushButton("取消全选")
        self.select_none_btn.clicked.connect(self.select_none_videos)
        self.invert_selection_btn = QPushButton("反选")
        self.invert_selection_btn.clicked.connect(self.invert_selection)
        
        select_layout.addWidget(self.select_all_btn)
        select_layout.addWidget(self.select_none_btn)
        select_layout.addWidget(self.invert_selection_btn)
        select_layout.addStretch()
        
        layout.addLayout(select_layout)
        layout.addWidget(self.video_table)
        layout.addWidget(QLabel("日志:"))
        layout.addWidget(self.log_output)
        
        group_box.setLayout(layout)
        return group_box
        
    def connect_signals(self):
        """连接信号和槽"""
        self.parse_btn.clicked.connect(self.parse_channel)
        self.browse_btn.clicked.connect(self.browse_folder)
        self.download_btn.clicked.connect(self.start_download)
        self.stop_btn.clicked.connect(self.stop_download)
        
    def browse_folder(self):
        """浏览文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self, "选择保存文件夹", self.path_input.text())
        if folder:
            self.path_input.setText(folder)
            
    def parse_channel(self):
        """解析YouTube频道"""
        url = self.url_input.text().strip()
        self.log(f"用户输入的URL: {url}")
        
        if not url:
            QMessageBox.warning(self, "警告", "请输入YouTube频道URL")
            return
            
        # URL解码，处理中文等特殊字符
        import urllib.parse
        decoded_url = urllib.parse.unquote(url)
        self.log(f"解码后的URL: {decoded_url}")
        
        # 验证URL格式（使用解码后的URL）
        if not self.is_valid_youtube_url(decoded_url):
            QMessageBox.warning(self, "警告", "请输入有效的YouTube频道URL")
            return
            
        # 使用解码后的URL进行后续处理
        url = decoded_url
            
        self.log("开始解析频道...")
        self.parse_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        
        # 创建解析线程
        self.log(f"创建解析线程，URL: {url}")
        self.parse_thread = ParseThread(url, self.downloader)
        self.parse_thread.parse_completed.connect(self._on_parse_completed)
        self.parse_thread.parse_failed.connect(self._on_parse_failed)
        self.log("连接信号完成，启动线程...")
        self.parse_thread.start()
        self.log("解析线程已启动")
        
        # 确保线程不会被垃圾回收
        self.parse_thread.finished.connect(lambda: self.log("解析线程已结束"))
        
    def _on_parse_completed(self, videos):
        """解析完成处理"""
        self.log(f"成功获取 {len(videos)} 个视频")
        self.videos = videos
        self._update_video_list(videos)
        self._finish_parsing()
        
    def _on_parse_failed(self, error_msg):
        """解析失败处理"""
        self.log(f"解析失败: {error_msg}")
        self._show_error(error_msg)
        self._finish_parsing()
            
    def _update_video_list(self, videos):
        """更新视频列表"""
        self.video_table.setRowCount(len(videos))
        
        for row, video in enumerate(videos):
            # 添加复选框
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(Qt.Checked)  # 默认选中
            self.video_table.setItem(row, 0, checkbox_item)
            
            # 添加视频信息
            self.video_table.setItem(row, 1, QTableWidgetItem(video.get('title', 'Unknown')))
            self.video_table.setItem(row, 2, QTableWidgetItem(video.get('duration', 'Unknown')))
            self.video_table.setItem(row, 3, QTableWidgetItem(video.get('upload_date', 'Unknown')))
            self.video_table.setItem(row, 4, QTableWidgetItem("等待下载"))
            
        self.log(f"找到 {len(videos)} 个视频")
        self.download_btn.setEnabled(True)
        
    def _show_error(self, message):
        """显示错误信息"""
        QMessageBox.critical(self, "错误", message)
        self.log(f"错误: {message}")
        
    def _finish_parsing(self):
        """完成解析"""
        self.parse_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
    def select_all_videos(self):
        """全选视频"""
        for row in range(self.video_table.rowCount()):
            self.video_table.item(row, 0).setCheckState(Qt.Checked)
        self.log("已全选所有视频")
        
    def select_none_videos(self):
        """取消全选"""
        for row in range(self.video_table.rowCount()):
            self.video_table.item(row, 0).setCheckState(Qt.Unchecked)
        self.log("已取消所有视频选择")
        
    def invert_selection(self):
        """反选"""
        for row in range(self.video_table.rowCount()):
            item = self.video_table.item(row, 0)
            if item.checkState() == Qt.Checked:
                item.setCheckState(Qt.Unchecked)
            else:
                item.setCheckState(Qt.Checked)
        self.log("已反选视频")
        
    def get_selected_videos(self):
        """获取选中的视频列表"""
        selected_videos = []
        for row in range(self.video_table.rowCount()):
            item = self.video_table.item(row, 0)
            if item.checkState() == Qt.Checked:
                # 获取对应的视频数据
                if row < len(self.videos):
                    selected_videos.append(self.videos[row])
        return selected_videos
        
    def start_download(self):
        """开始下载"""
        if not hasattr(self, 'videos') or not self.videos:
            QMessageBox.warning(self, "警告", "请先解析频道")
            return
            
        # 获取选中的视频
        selected_videos = self.get_selected_videos()
        if not selected_videos:
            QMessageBox.warning(self, "警告", "请选择要下载的视频")
            return
            
        save_path = self.path_input.text()
        if not save_path:
            QMessageBox.warning(self, "警告", "请选择保存路径")
            return
            
        # 创建保存目录
        if self.create_folder_cb.isChecked():
            channel_name = self.get_channel_name_from_url(self.url_input.text())
            save_path = os.path.join(save_path, channel_name)
            
        os.makedirs(save_path, exist_ok=True)
        
        quality = self.quality_combo.currentText()
        
        self.log(f"开始下载 {len(selected_videos)} 个选中的视频...")
        self.download_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, len(selected_videos))
        
        # 创建下载线程
        self.download_thread = DownloadThread(selected_videos, save_path, quality)
        self.download_thread.progress_updated.connect(self.update_download_progress)
        self.download_thread.download_completed.connect(self.download_completed)
        self.download_thread.download_failed.connect(self.download_failed)
        self.download_thread.start()
        
    def stop_download(self):
        """停止下载"""
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.stop()
            self.log("下载已停止")
            
        self.download_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
    def update_download_progress(self, current, total, video_title, status):
        """更新下载进度"""
        self.progress_bar.setValue(current)
        self.status_bar.showMessage(f"下载进度: {current}/{total}")
        
        # 更新表格中的状态
        for row in range(self.video_table.rowCount()):
            title_item = self.video_table.item(row, 1)
            if title_item and title_item.text() == video_title:
                self.video_table.setItem(row, 4, QTableWidgetItem(status))
                break
                
        self.log(f"[{current}/{total}] {video_title}: {status}")
        
    def download_completed(self):
        """下载完成"""
        self.log("所有视频下载完成！")
        QMessageBox.information(self, "完成", "所有视频下载完成！")
        
        self.download_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
    def download_failed(self, error_message):
        """下载失败"""
        self.log(f"下载失败: {error_message}")
        QMessageBox.critical(self, "错误", f"下载失败: {error_message}")
        
        self.download_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
    def log(self, message):
        """添加日志"""
        from PyQt5.QtCore import QDateTime
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.log_output.append(f"[{current_time}] {message}")
        
    def is_valid_youtube_url(self, url):
        """验证YouTube URL是否有效"""
        # URL解码，处理中文等特殊字符
        import urllib.parse
        decoded_url = urllib.parse.unquote(url)
        
        patterns = [
            r'https?://(www\.)?youtube\.com/@?[\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\-]+(/shorts)?/?$',  # 支持Unicode字符
            r'https?://(www\.)?youtube\.com/@?[\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\-]+(/videos)?/?$',   # 支持Unicode字符
            r'https?://(www\.)?youtube\.com/@?[\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\-]+(/featured)?/?$', # 支持Unicode字符
            r'https?://(www\.)?youtube\.com/channel/[\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\-]+(/shorts)?/?$',  # 支持Unicode字符
            r'https?://(www\.)?youtube\.com/c/[\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\-]+(/shorts)?/?$',    # 支持Unicode字符
            r'https?://(www\.)?youtube\.com/user/[\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\-]+(/shorts)?/?$'   # 支持Unicode字符
        ]
        
        return any(re.match(pattern, decoded_url) for pattern in patterns)
        
    def get_channel_name_from_url(self, url):
        """从URL中提取频道名称"""
        # URL解码，处理中文等特殊字符
        import urllib.parse
        decoded_url = urllib.parse.unquote(url)
        
        # 首先移除路径中的/shorts、/videos等后缀
        base_url = re.sub(r'/shorts$|/videos$|/featured$', '', decoded_url)
        
        # 更新正则表达式，支持Unicode字符（包括中文）
        match = re.search(r'youtube\.com/@?([\w\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\-]+)', base_url)
        if match:
            return match.group(1)
        return "UnknownChannel"