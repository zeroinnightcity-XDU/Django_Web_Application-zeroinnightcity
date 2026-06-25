# Django 极简个人记录博客 Step 2 Spec

## Why
Step 1 已完成项目结构、媒体配置与核心模型设计，当前需要推进到数据读取与页面入口层，为后续模板联调提供稳定的后端接口。
本次变更聚焦于主路由分发、子应用语义化路由和视图逻辑实现，确保数据库内容能够按分区正确查询并传递给模板。

## What Changes
- 在项目根级 `config/urls.py` 中保留 `admin` 路由，并使用 `include()` 将站点主要流量分发到内容子应用。
- 在开发环境下保留静态与媒体文件访问配置，确保通过 `settings.MEDIA_URL` 与 `settings.MEDIA_ROOT` 可访问上传图片。
- 为内容应用新增独立 `urls.py`，配置首页、音乐、电影、照片墙、Thoughts 与 About 的语义化路径。
- 在 `apps/content/views.py` 中实现首页重定向、音乐列表、音乐详情、电影列表、电影详情、照片墙列表、Thoughts 列表和 About 静态页。
- 采用 Django 通用类视图或函数式视图实现数据查询，并为模板提供清晰一致的上下文字段。
- 保持本次范围仅覆盖路由与视图，不提前实现完整模板视觉效果。

## Impact
- Affected specs: 路由组织、数据查询、页面入口、开发环境媒体访问
- Affected code: `config/urls.py`、`apps/content/urls.py`、`apps/content/views.py`

## ADDED Requirements
### Requirement: 项目级路由分发
系统 SHALL 在项目根级路由中保留 `admin` 后台入口，并通过 `include()` 将主要博客流量转发至内容应用路由。

#### Scenario: 访问站点主入口
- **WHEN** 用户访问站点根路径
- **THEN** 请求应由内容应用路由接管
- **AND** 管理后台仍可通过 `/admin/` 访问

### Requirement: 开发环境媒体访问
系统 SHALL 在开发环境下配置静态与媒体文件路由扩展，以支持上传图片在本地开发环境中的访问。

#### Scenario: 模板引用上传图片
- **WHEN** 页面模板渲染 `ImageField` 对应的媒体文件 URL
- **THEN** 开发环境应能通过 `settings.MEDIA_URL` 正常访问该文件

### Requirement: 内容应用语义化路由
系统 SHALL 在内容应用中提供清晰且解耦的 URL 路径，覆盖首页、Music、Films、Fragments、Thoughts 和 About 页面。

#### Scenario: 访问各内容分区
- **WHEN** 用户访问 `/music/`、`/films/`、`/fragments/`、`/thoughts/` 或 `/about/`
- **THEN** 系统应进入对应视图
- **AND** Music 与 Films 详情页应支持通过主键路径访问

### Requirement: 首页入口行为
系统 SHALL 提供站点首页视图，并在当前阶段自动重定向到 Music 页面。

#### Scenario: 访问首页
- **WHEN** 用户访问 `/`
- **THEN** 系统应重定向到 `/music/`

### Requirement: Music 与 Films 列表查询
系统 SHALL 提供 Music 与 Films 列表视图，分别从 `MediaItem` 中按类别过滤数据并按创建时间倒序返回。

#### Scenario: 查看音乐列表
- **WHEN** 用户访问 `/music/`
- **THEN** 视图只返回类别为 `Music` 的媒体条目
- **AND** 数据按创建时间倒序排列

#### Scenario: 查看电影列表
- **WHEN** 用户访问 `/films/`
- **THEN** 视图只返回类别为 `Films` 的媒体条目
- **AND** 数据按创建时间倒序排列

### Requirement: Music 与 Films 详情查询
系统 SHALL 提供 Music 与 Films 详情视图，支持根据主键获取单个媒体条目并渲染详情模板。

#### Scenario: 查看音乐详情
- **WHEN** 用户访问 `/music/<int:pk>/`
- **THEN** 视图应获取对应主键且类别为 `Music` 的条目

#### Scenario: 查看电影详情
- **WHEN** 用户访问 `/films/<int:pk>/`
- **THEN** 视图应获取对应主键且类别为 `Films` 的条目

### Requirement: Fragments 与 Thoughts 列表查询
系统 SHALL 提供照片墙列表和 Thoughts 列表视图，并返回对应模型的全部数据集。

#### Scenario: 查看照片墙
- **WHEN** 用户访问 `/fragments/`
- **THEN** 视图应返回全部 `Fragment` 数据

#### Scenario: 查看 Thoughts 列表
- **WHEN** 用户访问 `/thoughts/`
- **THEN** 视图应返回全部 `Post` 数据
- **AND** 数据按创建时间倒序排列

### Requirement: About 静态页面视图
系统 SHALL 提供一个不依赖数据库查询的 About 视图，用于直接渲染个人简介模板。

#### Scenario: 访问 About 页面
- **WHEN** 用户访问 `/about/`
- **THEN** 系统应直接渲染 About 模板

## MODIFIED Requirements
### Requirement: 当前交付范围
当前阶段的交付范围 SHALL 包含 Step 2 所需的主路由、子路由与视图实现，但不包含完整前端模板和最终页面样式。

#### Scenario: 用户按步骤推进
- **WHEN** 用户要求开始 Step 2
- **THEN** 本次工作应只实现后端路由与视图逻辑
- **AND** 模板文件仅作为后续 Step 3 的联调目标

## REMOVED Requirements
### Requirement: 本阶段模板视觉实现
**Reason**: 用户当前要求聚焦在数据查询与路由层，提前实现模板会扩大范围。
**Migration**: 在 Step 3 中继续补充 `base.html` 与各分区模板。
