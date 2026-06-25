# Tasks
- [x] Task 1: 规划 Django 项目目录结构并明确应用边界
  - [x] 输出推荐目录结构，覆盖项目配置目录、业务应用目录、模板目录、静态资源目录和媒体上传目录
  - [x] 明确 Step 1 采用单独内容应用承载 `MediaItem`、`Fragment`、`Post`
  - [x] 说明该结构如何支持后续 Step 2 的视图与路由扩展

- [x] Task 2: 配置项目级媒体上传设置
  - [x] 在 `settings.py` 中加入 `MEDIA_URL`
  - [x] 在 `settings.py` 中加入 `MEDIA_ROOT`
  - [x] 约定上传文件的存储目录命名，便于后续封面图和照片墙图片管理

- [x] Task 3: 设计 `MediaItem`、`Fragment`、`Post` 三个核心模型
  - [x] 为 `MediaItem` 定义标题、作者或导演、类别、封面图、核心介绍、详细文本、外部链接、创建时间等字段
  - [x] 为 `Fragment` 定义图片、时间、地点标签及基础排序字段
  - [x] 为 `Post` 定义标题、正文、摘要或展示辅助字段，并兼容 Markdown 内容存储
  - [x] 明确模型的 `__str__` 表达与默认排序策略

- [x] Task 4: 明确后台管理接入要求
  - [x] 约定哪些字段应在 Django Admin 中优先展示
  - [x] 约定哪些字段可用于筛选、搜索或分类
  - [x] 确保模型设计便于后台上传图片和维护内容

- [x] Task 5: 校验 Step 1 规格边界
  - [x] 确认本轮不包含 `views.py`、`urls.py`、模板与样式实现
  - [x] 确认规格内容能直接支撑后续 Step 2 与 Step 3

# Task Dependencies
- `Task 2` depends on `Task 1`
- `Task 3` depends on `Task 1`
- `Task 4` depends on `Task 3`
- `Task 5` depends on `Task 2` and `Task 3`
