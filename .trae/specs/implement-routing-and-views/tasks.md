# Tasks
- [x] Task 1: 调整项目根路由并接入内容子应用
  - [x] 在 `config/urls.py` 中保留 `admin` 路由
  - [x] 使用 `include()` 将站点主流量转发到 `apps/content/urls.py`
  - [x] 保留开发环境下的媒体文件访问配置

- [x] Task 2: 创建内容应用路由文件
  - [x] 新建 `apps/content/urls.py`
  - [x] 配置首页重定向、Music、Films、Fragments、Thoughts、About 的语义化路径
  - [x] 为 Music 与 Films 配置带主键的详情页路径

- [x] Task 3: 实现内容应用视图
  - [x] 实现首页重定向视图
  - [x] 实现 `music_list` 与 `films_list` 的分类列表查询逻辑
  - [x] 实现 `music_detail` 与 `films_detail` 的主键详情查询逻辑
  - [x] 实现 `fragments_list`、`thoughts_list` 与 `about_view`
  - [x] 为模板联调提供清晰的上下文字段与注释

- [x] Task 4: 校验路由与视图联动
  - [x] 使用 Django 检查命令验证路由配置无误
  - [x] 验证视图查询逻辑与 Step 1 模型字段一致
  - [x] 确认本轮未提前实现 Step 3 的模板样式

# Task Dependencies
- `Task 2` depends on `Task 1`
- `Task 3` depends on `Task 2`
- `Task 4` depends on `Task 1`, `Task 2`, and `Task 3`
