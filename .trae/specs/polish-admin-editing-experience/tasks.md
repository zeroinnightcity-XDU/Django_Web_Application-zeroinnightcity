# Tasks
- [x] Task 1: 优化 Django Admin 站点级中文展示
  - [x] 设置后台站点标题、站点头部和首页欢迎文案
  - [x] 确保整体命名更贴合博客录入场景

- [x] Task 2: 优化 `MediaItem` 后台管理体验
  - [x] 增强列表展示字段、筛选和搜索配置
  - [x] 为编辑表单增加合理的字段分组
  - [x] 为封面图片增加后台预览
  - [x] 增加必要的中文帮助提示

- [x] Task 3: 优化 `Fragment` 与 `Post` 后台管理体验
  - [x] 为 `Fragment` 增加更直观的列表字段和图片预览
  - [x] 为 `Fragment` 编辑表单增加字段组织和提示
  - [x] 为 `Post` 增强列表页的识别信息和表单布局

- [x] Task 4: 校验后台优化效果
  - [x] 验证 Django Admin 注册和页面加载正常
  - [x] 验证后台列表与编辑页字段展示更友好
  - [x] 确认未改动模型结构与前台页面逻辑

# Task Dependencies
- `Task 2` depends on `Task 1`
- `Task 3` depends on `Task 1`
- `Task 4` depends on `Task 2` and `Task 3`
