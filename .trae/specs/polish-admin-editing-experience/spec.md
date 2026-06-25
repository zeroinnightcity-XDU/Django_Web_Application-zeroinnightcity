# Django 后台录入体验优化 Spec

## Why
当前 Django Admin 已可用，但录入体验仍偏基础。为了让日常上传图片、填写文字和管理分类更顺手，需要进一步优化后台的字段展示方式、中文标题和表单组织结构。

## What Changes
- 优化 Django Admin 的站点标题、站点头部和首页欢迎文案，统一为中文界面。
- 为 `MediaItem`、`Fragment`、`Post` 提供更友好的后台列表展示字段。
- 为后台表单增加字段分组、帮助提示和更清晰的中文说明。
- 为图片相关模型提供封面或缩略图预览，帮助录入时快速确认内容。
- 优化搜索、筛选和排序配置，降低日常维护成本。
- 保持本次范围仅覆盖 Django Admin 展示与录入体验，不改动模型结构和前台模板。

## Impact
- Affected specs: 后台录入体验、后台内容管理
- Affected code: `apps/content/admin.py`、必要时 `config/urls.py` 或项目级 admin 配置

## ADDED Requirements
### Requirement: Admin 中文化展示
系统 SHALL 为 Django Admin 提供更友好的中文站点标题和入口文案，使后台界面更贴近内容录入场景。

#### Scenario: 进入后台首页
- **WHEN** 管理员访问 Django Admin 首页
- **THEN** 页面应显示清晰的中文标题或中文说明

### Requirement: 列表页信息增强
系统 SHALL 在后台列表页中展示更有用的字段，帮助管理员快速定位和区分内容。

#### Scenario: 管理媒体条目
- **WHEN** 管理员进入 `MediaItem` 列表页
- **THEN** 应看到标题、类别、作者或导演、创建时间等核心字段
- **AND** 如条件允许，应看到封面预览

#### Scenario: 管理照片碎片或文章
- **WHEN** 管理员进入 `Fragment` 或 `Post` 列表页
- **THEN** 应看到适合快速辨识内容的字段

### Requirement: 后台表单录入优化
系统 SHALL 对后台编辑表单进行分组和说明优化，使常用字段更容易理解与填写。

#### Scenario: 新增或编辑媒体条目
- **WHEN** 管理员打开 `MediaItem` 编辑页
- **THEN** 字段应按基础信息、内容介绍、资源链接等进行合理分组
- **AND** 图片字段和文本字段应有更明确的中文说明

### Requirement: 图片预览支持
系统 SHALL 在后台中为图片字段提供预览展示，以提升录入和检查效率。

#### Scenario: 检查封面图片
- **WHEN** 管理员查看已有 `MediaItem` 或 `Fragment`
- **THEN** 应能在后台看到封面或图片缩略预览

## MODIFIED Requirements
### Requirement: 当前交付范围
当前阶段的交付范围 SHALL 仅包含 Django Admin 界面的易用性优化，不包含新的业务模型、视图、路由或前端页面改动。

#### Scenario: 本轮后台优化
- **WHEN** 用户要求让后台录入更顺手
- **THEN** 本次工作应集中于 Admin 体验本身

## REMOVED Requirements
### Requirement: 本阶段前台页面调整
**Reason**: 用户当前只要求优化后台录入体验。
**Migration**: 如后续需要，可再单独规划前台内容编辑联动或富文本增强。
