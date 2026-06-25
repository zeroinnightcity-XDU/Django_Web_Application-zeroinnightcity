# 后台 CONTENT 条目名称调整计划

## Summary

- 目标：将 Django 后台 `CONTENT` 分组下的三个模型名称从“媒体条目”改为“音乐/电影”、从“文章”改为“博客”、从“照片碎片”改为“照片墙”。
- 范围：仅调整后台模型显示名称，不修改应用分组标题 `CONTENT`，不改后台字段文案与页面结构。
- 实现原则：以模型 `Meta.verbose_name` / `verbose_name_plural` 为主进行修改，并新增迁移同步模型选项，避免只改代码不改迁移状态。

## Current State Analysis

- `apps/content/models.py`
  - `MediaItem.Meta.verbose_name` 与 `verbose_name_plural` 当前都是“媒体条目”。
  - `Fragment.Meta.verbose_name` 与 `verbose_name_plural` 当前都是“照片碎片”。
  - `Post.Meta.verbose_name` 与 `verbose_name_plural` 当前都是“文章”。
- `apps/content/apps.py`
  - `ContentConfig.verbose_name = 'Content'`，这对应后台分组标题 `CONTENT`。
  - 用户当前需求没有要求修改这一项，因此保持不变。
- `apps/content/admin.py`
  - 存在“录入媒体条目”“文章信息”等说明性文案，但它们不会决定后台首页三个模型入口名称。
  - 本次需求聚焦后台分组列表名称，因此这些说明文案默认不纳入修改范围。
- `apps/content/migrations/0001_initial.py`
  - 初始迁移中也记录了三个模型当前的 `verbose_name` / `verbose_name_plural`。
  - 不应直接改历史迁移，应新增一个迁移来更新模型选项。

## Proposed Changes

### 1. 修改模型显示名称

- 文件：`apps/content/models.py`
- 调整内容：
  - 将 `MediaItem` 的 `verbose_name` 与 `verbose_name_plural` 改为“音乐/电影”。
  - 将 `Post` 的 `verbose_name` 与 `verbose_name_plural` 改为“博客”。
  - 将 `Fragment` 的 `verbose_name` 与 `verbose_name_plural` 改为“照片墙”。
- 原因：
  - Django 后台首页和模型管理页的名称主要由模型 `Meta` 中的这两个字段决定。

### 2. 新增模型选项迁移

- 文件：`apps/content/migrations/0002_rename_admin_labels.py`（文件名可按 Django 实际生成结果为准）
- 调整内容：
  - 为 `MediaItem`、`Post`、`Fragment` 生成 `AlterModelOptions` 迁移，更新 `verbose_name`、`verbose_name_plural`。
- 原因：
  - 保持迁移状态与代码一致。
  - 避免后续执行 `makemigrations` 时再次因为模型选项差异产生未提交迁移。

### 3. 明确不修改的内容

- 文件：`apps/content/apps.py`
  - 保持 `ContentConfig.verbose_name = 'Content'` 不变，因此后台分组标题继续显示为 `CONTENT`。
- 文件：`apps/content/admin.py`
  - 暂不修改“录入媒体条目”“文章信息”等表单说明文案，因为用户需求仅针对后台入口名称。
  - 若后续希望后台表单页内的说明文案也同步改名，可作为额外优化再处理。

## Assumptions & Decisions

- 决策：本次“修改后台 CONTENT 部分的名称”解释为修改该分组下三个模型入口名称，而不是修改分组标题 `CONTENT` 本身。
- 决策：采用“改模型 Meta + 新增迁移”的标准 Django 做法，不直接改已有历史迁移。
- 假设：当前后台截图对应的就是 `apps.content` 应用下 `MediaItem`、`Post`、`Fragment` 三个模型入口。
- 假设：用户未要求同步修改后台表单页中的说明文本，因此这些文案保持现状。

## Verification Steps

1. 运行 `python manage.py makemigrations --check`，确认模型选项变更已被迁移覆盖，不再产生新的未迁移改动。
2. 启动本地后台并进入 Django Admin 首页，确认 `CONTENT` 分组下显示为“音乐/电影”“博客”“照片墙”。
3. 分别进入三个模型列表页，确认页面标题和面包屑中的模型名称也同步更新。
4. 确认 `CONTENT` 分组标题仍保持不变，符合当前需求范围。
