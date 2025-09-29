# 🚀 手动推送到GitHub指南

## 步骤1：在GitHub创建仓库
1. 访问 https://github.com/new
2. 仓库名称：`youtube-channel-downloader`
3. 描述：`A desktop application for downloading YouTube channel videos with PyQt5 GUI`
4. 设置为公开仓库
5. **不要** 初始化README（保持空仓库）
6. 点击 "Create repository"

## 步骤2：配置Git（如果尚未配置）
```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

## 步骤3：推送到GitHub
在终端中逐行执行以下命令：

```bash
# 添加远程仓库（将YOUR_USERNAME替换为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/youtube-channel-downloader.git

# 推送到GitHub
git push -u origin master
```

## 🔧 如果遇到问题

### 远程仓库已存在
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/youtube-channel-downloader.git
git push -u origin master
```

### 认证失败
GitHub现在需要使用个人访问令牌：
1. 访问 https://github.com/settings/tokens
2. 创建新的个人访问令牌
3. 推送到时输入用户名和令牌（而不是密码）

### 分支名称问题
如果默认分支是 `main` 而不是 `master`：
```bash
git branch -M main
git push -u origin main
```

## ✅ 验证推送成功
推送成功后，访问：
```
https://github.com/YOUR_USERNAME/youtube-channel-downloader
```

你应该能看到你的项目文件，包括：
- README.md
- main.py
- main_window.py
- youtube_downloader.py
- download_thread.py
- requirements.txt

## 📞 需要帮助？
如果推送过程中遇到问题：
1. 检查网络连接
2. 确认GitHub用户名正确
3. 检查GitHub访问权限
4. 查看终端错误信息

---

**项目地址**: https://github.com/YOUR_USERNAME/youtube-channel-downloader