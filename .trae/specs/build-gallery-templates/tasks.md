# Tasks
- [x] Task 1: 构建全局基础母版与导航
  - [x] 新建 `templates/base.html`
  - [x] 引入 Tailwind CSS CDN 与 Google Fonts
  - [x] 将全局背景设置为低饱和度淡蓝色
  - [x] 实现顶部导航和当前页面高亮逻辑
  - [x] 实现手机与桌面均可用的响应式导航与页面容器
  - [x] 预留统一页面容器与 `{% block content %}` 区域

- [x] Task 2: 实现 Music 与 Films 列表模板
  - [x] 新建 `templates/content/media_list.html`
  - [x] 使用响应式网格展示卡片封面、标题和副标题
  - [x] 保持卡片白底黑边，与淡蓝背景形成层次
  - [x] 为卡片添加缩放、阴影与过渡动效
  - [x] 确保手机、平板、桌面下的列数和间距自适应

- [x] Task 3: 实现媒体详情模板
  - [x] 新建 `templates/content/media_detail.html`
  - [x] 实现左右分栏布局
  - [x] 加入返回列表链接与外链按钮
  - [x] 为手机端提供上下堆叠的响应式详情布局

- [x] Task 4: 实现 Fragments、Thoughts 与 About 模板
  - [x] 新建 `templates/content/fragments_list.html`
  - [x] 新建 `templates/content/thoughts_list.html`
  - [x] 新建 `templates/content/about.html`
  - [x] 确保模板标签与上下文字段和 Step 2 视图一致
  - [x] 确保 Fragments、Thoughts 与 About 在手机和桌面均具备良好可读性

- [x] Task 5: 校验模板联调与范围边界
  - [x] 验证模板路径与视图渲染名称一致
  - [x] 验证 Django 模板语法与 URL 反向解析无误
  - [x] 验证主要页面在小屏与大屏下的响应式结构成立
  - [x] 确认本轮未改动 Step 1 的模型设计和 Step 2 的核心业务逻辑

# Task Dependencies
- `Task 2` depends on `Task 1`
- `Task 3` depends on `Task 1`
- `Task 4` depends on `Task 1`
- `Task 5` depends on `Task 2`, `Task 3`, and `Task 4`
