# 锡息相关

全球锡产业监测台的 GitHub Pages 正式版。

## 文件

- `index.html`：网站入口，由本地 `build_tin_dashboard_review.py` 生成。
- `.github/workflows/pages.yml`：推送到 `main` 后自动部署 GitHub Pages。
- `.nojekyll`：关闭 Jekyll 处理。

## 更新

在本地重新运行构建脚本后，提交并推送新的 `index.html`。GitHub Actions 会自动发布。

GitHub Actions 每 5 分钟尝试刷新沪锡和 LME 锡行情，网页每 15 秒检查新的 `quotes.json`。调度和 Pages 部署可能延迟，因此公开站属于分钟级准实时；其他基本面数据随本地构建更新。本地服务仍提供 15 秒行情刷新。
