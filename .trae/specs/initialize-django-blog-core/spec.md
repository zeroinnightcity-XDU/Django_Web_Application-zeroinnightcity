# Django 极简个人记录博客 Step 1 Spec

## Why
本次变更用于为课程期末大作业搭建可持续扩展的 Django 后端基础骨架，先完成项目级配置与内容模型设计，确保后续视图、模板、后台管理和部署工作可以在稳定结构上继续推进。
当前用户明确要求先从 Step 1 开始，因此本规格只覆盖目录规划、`settings.py` 的媒体配置以及核心 `models.py` 设计，不提前实现视图与页面模板。

## What Changes
- 规划一个符合 Django 最佳实践的项目目录结构，区分项目配置层、应用层、模板层、静态资源层与媒体上传层。
- 在项目级 `settings.py` 中配置 `MEDIA_URL` 与 `MEDIA_ROOT`，为图片上传和开发环境访问媒体文件提供基础支持。
- 设计统一的 `MediaItem` 内容模型，用于承载 `Music` 与 `Films` 两类内容，并保留清晰的类型字段与可扩展文本字段。
- 设计 `Fragment` 模型，用于照片墙内容的图片、时间和地点标签管理。
- 设计 `Post` 模型，用于 Thoughts 文字博客，支持 Markdown 或后续富文本扩展。
- 规划 Django Admin 的接入要求，确保后续可在后台录入、上传、编辑和分类内容。
- 明确模型字段、排序策略、字符串展示、可选字段策略与后续迁移兼容性要求。
- 明确本次变更不包含前端模板、路由实现、详情页交互及 Tailwind 页面开发。

## Impact
- Affected specs: 内容建模、媒体上传、后台录入、项目结构规范
- Affected code: `config/settings.py`、`apps/content/models.py`、`apps/content/admin.py`、项目根目录媒体目录与应用目录

## ADDED Requirements
### Requirement: 项目目录结构规划
系统 SHALL 提供一个清晰的 Django 项目目录结构建议，用于承载项目配置、业务应用、模板、静态资源和媒体上传目录，并能支持后续继续添加 `views.py`、`urls.py` 与模板文件。

#### Scenario: 结构建议可支持后续开发
- **WHEN** 开发者查看 Step 1 的输出内容
- **THEN** 可以看到推荐的项目目录结构
- **AND** 该结构可以明确区分项目配置目录与业务应用目录
- **AND** 该结构包含媒体上传目录的放置建议

### Requirement: 媒体上传配置
系统 SHALL 在 Django 项目级配置中定义 `MEDIA_URL` 与 `MEDIA_ROOT`，用于支持封面图片与照片墙图片的上传和访问。

#### Scenario: 开发环境需要图片上传基础
- **WHEN** 开发者初始化项目配置
- **THEN** `settings.py` 中应包含媒体资源访问路径与本地存储路径
- **AND** 该配置应兼容后续在开发环境中通过 URL 访问上传文件

### Requirement: MediaItem 内容模型
系统 SHALL 提供一个通用 `MediaItem` 模型，用于统一管理音乐与电影条目，并至少包含标题、作者或导演、类别、封面图片、核心介绍、详细文本、外部链接和创建时间字段。

#### Scenario: 录入音乐或电影条目
- **WHEN** 管理员在后台创建一个音乐或电影条目
- **THEN** 可以录入标题与作者或导演信息
- **AND** 可以选择类别为 `Music` 或 `Films`
- **AND** 可以上传封面图片
- **AND** 可以填写简要介绍与详细文本
- **AND** 可以选填第三方链接

### Requirement: Fragment 照片墙模型
系统 SHALL 提供 `Fragment` 模型，用于存储照片墙图片及其时间、地点等元信息。

#### Scenario: 录入照片墙内容
- **WHEN** 管理员在后台创建一个 Fragment
- **THEN** 可以上传一张图片
- **AND** 可以填写拍摄时间信息
- **AND** 可以填写地点标签

### Requirement: Post 文字博客模型
系统 SHALL 提供 `Post` 模型，用于支持 Thoughts 分区的文字内容发布，并保留 Markdown 或后续富文本扩展空间。

#### Scenario: 录入 Thoughts 文章
- **WHEN** 管理员在后台创建一篇 Post
- **THEN** 可以填写标题与正文
- **AND** 正文字段应适合保存 Markdown 原文或可迁移到富文本方案
- **AND** 系统应保留文章创建时间

### Requirement: Admin 可管理性
系统 SHALL 为上述模型提供适合 Django Admin 管理的基础设计，以便后续方便上传图片、填写文字与按类型分类。

#### Scenario: 后台管理内容
- **WHEN** 开发者在后续步骤接入 Django Admin
- **THEN** 模型字段命名与类型应适合后台表单直接录入
- **AND** 模型应具备合理的字符串展示和默认排序设计

## MODIFIED Requirements
### Requirement: 当前交付范围
当前阶段的交付范围 SHALL 仅包含 Step 1 所需的后端基础架构规划与模型规格，不包含 `views.py`、路由实现、模板实现和前端交互效果。

#### Scenario: 用户要求按步骤推进
- **WHEN** 用户要求先从 Step 1 开始
- **THEN** 本次工作仅输出 Step 1 的规格与任务拆解
- **AND** 后续 Step 2 与 Step 3 将在本规格基础上继续推进

## REMOVED Requirements
### Requirement: 本阶段前端页面实现
**Reason**: 用户当前仅要求先完成 Step 1，提前实现前端页面会扩大范围并降低阶段边界清晰度。
**Migration**: 在后续 Step 2 与 Step 3 中继续补充视图、路由和模板规格与实现。
