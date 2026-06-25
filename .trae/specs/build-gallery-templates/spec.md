# Django 极简个人记录博客 Step 3 Spec

## Why
后端路由与视图已经就绪，当前需要补上前端模板层，让数据库内容能够以统一、现代、极简且具有艺术画廊感的方式呈现出来。
本次变更聚焦于 Django 模板与 Tailwind CSS 的页面结构实现，为后续联调、内容录入展示和风格迭代提供可用基础。

## What Changes
- 新增项目级基础母版 `base.html`，统一引入 Tailwind CSS CDN、Google Fonts 和全局布局样式。
- 全局页面背景采用低饱和度淡蓝色，内容卡片保持白底与细黑边，形成安静但有层次的画廊观感。
- 实现顶部导航栏，并通过 URL 感知逻辑为当前分区添加黑底白字的 Pinned 高亮效果。
- 所有页面采用移动端优先的响应式布局，确保在手机与桌面显示器上都能保持良好的可读性和留白节奏。
- 为 `Music` 与 `Films` 提供统一风格的响应式网格列表模板，突出封面卡片与悬停动效。
- 为 `MediaItem` 提供左右分栏的详情页模板，展示大尺寸封面、详细文本与外链按钮。
- 为 `Fragments` 提供照片墙模板，展示图片与极简时间地点信息。
- 为 `Thoughts` 提供单栏阅读型模板，强调留白、行高和分段节奏。
- 为 `About` 提供极简个人介绍模板和社交链接区域。
- 保持本次范围仅覆盖模板与前端样式，不改动 Step 1 的模型设计与 Step 2 的核心查询逻辑。

## Impact
- Affected specs: 模板渲染、导航交互、内容展示、页面视觉风格
- Affected code: `templates/base.html`、`templates/content/*.html`、必要时 `apps/content/views.py` 的模板路径适配

## ADDED Requirements
### Requirement: 全局基础母版
系统 SHALL 提供一个全局 `base.html` 模板，用于承载统一字体、背景色、导航栏、页面容器和 `{% block content %}` 内容区。

#### Scenario: 渲染任意内容页面
- **WHEN** 任意内容页面被请求
- **THEN** 页面应继承 `base.html`
- **AND** 页面应包含统一的顶部导航与基础排版风格
- **AND** 页面背景应使用低饱和度淡蓝色而非纯白底

### Requirement: 响应式页面适配
系统 SHALL 采用移动端优先的响应式设计，使页面在手机、平板和桌面显示器上都具备合适的布局、间距和组件尺寸。

#### Scenario: 在手机上浏览页面
- **WHEN** 用户使用手机访问站点
- **THEN** 导航与内容区应采用更紧凑的纵向布局
- **AND** 网格列数、字号和边距应适配小屏设备

#### Scenario: 在桌面显示器上浏览页面
- **WHEN** 用户使用桌面或大屏显示器访问站点
- **THEN** 页面应扩展为更宽的内容容器
- **AND** 列表与详情布局应利用更大的横向空间

### Requirement: 导航高亮交互
系统 SHALL 在导航中提供当前页面高亮效果，使当前分区呈现黑底白字的 Pinned 视觉状态。

#### Scenario: 访问不同分区页面
- **WHEN** 用户访问 `Music`、`Films`、`Fragments`、`Thoughts` 或 `About`
- **THEN** 对应导航项应显示为高亮状态
- **AND** 其他导航项保持透明背景

### Requirement: Music 与 Films 列表模板
系统 SHALL 提供适用于 `Music` 与 `Films` 的响应式列表模板，采用 2 到 4 列网格展示卡片。

#### Scenario: 浏览媒体列表
- **WHEN** 用户访问 `Music` 或 `Films` 列表页
- **THEN** 页面应以网格方式展示封面卡片
- **AND** 每张卡片应展示标题与作者或导演
- **AND** 悬停时应出现轻微缩放与阴影增强效果
- **AND** 网格列数应随屏幕宽度自适应变化
- **AND** 卡片本体应保持白底与细边框以和淡蓝背景形成对比

### Requirement: 媒体详情模板
系统 SHALL 提供 `MediaItem` 详情页模板，使用左右分栏布局展示封面与文字信息，并提供返回列表和外链按钮。

#### Scenario: 查看媒体详情
- **WHEN** 用户访问某个音乐或电影详情页
- **THEN** 在桌面端左侧应展示大尺寸封面
- **AND** 右侧应展示标题、作者或导演、核心介绍、详细文本和外链按钮
- **AND** 页面应提供返回列表入口

#### Scenario: 在手机上查看媒体详情
- **WHEN** 用户使用手机访问某个详情页
- **THEN** 页面应退化为上下堆叠布局
- **AND** 图片与文字区域都应保持舒适间距与可读性

### Requirement: Fragments 照片墙模板
系统 SHALL 提供照片墙模板，以整洁网格或类瀑布流方式展示图片，并附带时间与地点元信息。

#### Scenario: 浏览照片墙
- **WHEN** 用户访问 `Fragments` 页面
- **THEN** 页面应展示全部图片条目
- **AND** 每张图片下方应显示时间与地点文本
- **AND** 图片列数与卡片宽度应根据屏幕宽度自适应变化

### Requirement: Thoughts 阅读模板
系统 SHALL 提供单栏阅读型模板用于展示 Thoughts 文章列表，并保持舒适的留白与段落间距。

#### Scenario: 浏览 Thoughts 列表
- **WHEN** 用户访问 `Thoughts` 页面
- **THEN** 页面应按文章流形式展示内容
- **AND** 各文章块之间应有明显间距
- **AND** 正文宽度在大屏下不应过宽以免影响阅读

### Requirement: About 个人介绍模板
系统 SHALL 提供极简 About 页面，展示个人介绍文本与社交链接区域。

#### Scenario: 访问 About 页面
- **WHEN** 用户访问 `/about/`
- **THEN** 页面应展示个人简介
- **AND** 页面底部应展示社交平台链接

## MODIFIED Requirements
### Requirement: 当前交付范围
当前阶段的交付范围 SHALL 包含 Step 3 所需模板与基础前端交互，但不包含复杂前端框架接入、后台富文本编辑器和高级动画系统。

#### Scenario: 用户按步骤推进
- **WHEN** 用户要求开始 Step 3
- **THEN** 本次工作应聚焦 Django 模板与 Tailwind 样式实现
- **AND** 仅在必要范围内微调视图以适配模板

## REMOVED Requirements
### Requirement: 本阶段复杂前端工程化
**Reason**: 用户明确要求通过 Tailwind CDN 快速完成模板开发，无需引入额外前端构建链路。
**Migration**: 若未来需要更复杂的组件化开发，可再迁移到独立前端工程或 Tailwind 构建流程。
