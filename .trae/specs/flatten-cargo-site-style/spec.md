# 去圆角与 Cargo 风格重构 Spec

## Why
当前站点虽然已完成首页与个人资料重构，但整体仍保留较多圆角卡片、首页图片叠加信息块和偏柔和的作品集样式，与用户最新提供的参考图和 `cargo` 风格目标不一致。需要将前台视觉进一步收束为更冷静、更平直、更轻细的编排系统，并重新平衡首页与全站的比例关系。

## What Changes
- 将前台页面中的圆角元素统一移除，改为直角或近似直角的平直结构。
- 将网站主色调改为低饱和度淡蓝色，替换当前偏米色/暖灰基调。
- 调整全站字体系统，中英文正文、导航、辅助信息切换为更细长的字体组合。
- 保持当前大标题风格不变，不替换现有主要展示标题的字体策略。
- 重构首页为更接近 `cargo` 参考风格的布局：左侧保留品牌与导航，右侧图片改为全屏主视觉。
- 删除首页图片区域上叠加的欢迎语、Quote、Explore 和 About 按钮等信息块，仅保留左侧信息栏。
- 将 `Wentong Zou` 与年份时间戳移动到页面左下角，而不是主内容区底部。
- 重新平衡全站比例、留白、边框和文字密度，使页面更接近用户给定示例的冷静编排感。
- **BREAKING** 首页不再在图片区域中显示欢迎语、Quote 和图上导航入口。
- **BREAKING** 全站主要容器和交互块的圆角样式被移除。

## Impact
- Affected specs: 全局视觉风格、首页布局、全局导航、页脚定位、字体系统、内容页排版
- Affected code: `templates/base.html`, `templates/content/home.html`, `templates/content/about.html`, `templates/content/media_list.html`, `templates/content/media_detail.html`, `templates/content/fragments_list.html`, `templates/content/thoughts_list.html`

## ADDED Requirements
### Requirement: Cargo 风格首页构图
系统 SHALL 将首页改造为更接近参考图的 `cargo` 风格构图，重点体现左侧信息区与右侧全屏图像区的对照关系。

#### Scenario: 在桌面端访问首页
- **WHEN** 用户访问首页
- **THEN** 页面应呈现左侧固定信息栏与右侧大面积主视觉图像
- **AND** 右侧图像应占据主要视觉面积，接近全屏展示效果
- **AND** 图像区域上不应再叠加欢迎语、Quote、Explore 或额外导航模块
- **AND** 左侧应保留网站名、姓名与导航

#### Scenario: 首页底部信息位置
- **WHEN** 用户浏览首页左侧信息栏
- **THEN** `Wentong Zou` 与年份时间戳应位于左下角
- **AND** 其位置应更接近参考图中的版权信息布局，而不是页面主内容底部

### Requirement: 去圆角前台视觉系统
系统 SHALL 在前台模板中移除圆角元素，建立更平直、更克制的视觉语言。

#### Scenario: 浏览任意前台页面
- **WHEN** 用户浏览首页、列表页、详情页或 About 页面
- **THEN** 卡片、按钮、导航项、图片容器与信息块应移除圆角
- **AND** 页面应改用直角边框、平直分区和更克制的边界表达

### Requirement: 淡蓝主色与细长字体
系统 SHALL 将前台的主配色调整为低饱和度淡蓝色，并将中英文常规文字统一替换为更细长的字体组合。

#### Scenario: 浏览任意页面文字
- **WHEN** 用户查看导航、正文、辅助标签、页脚和说明文字
- **THEN** 这些文字应使用更细长的字体
- **AND** 中文与英文都应统一更新
- **AND** 大标题仍保持现有主要展示字体与展示风格不变

#### Scenario: 浏览页面整体色调
- **WHEN** 用户打开任意前台页面
- **THEN** 页面主色调应体现为低饱和度淡蓝色
- **AND** 该配色应贯穿背景、辅助底色和分区层次

## MODIFIED Requirements
### Requirement: 全局基础模板
系统 SHALL 将基础模板从“左侧信息栏 + 底部页脚在主内容区”的布局，调整为“左侧信息栏 + 左下角署名 + 更平直的导航与分区”的 `cargo` 风格前台骨架。

#### Scenario: 渲染任意前台页面
- **WHEN** 页面使用基础模板
- **THEN** 左侧信息栏应保持为主要导航骨架
- **AND** 页脚信息应移入左侧底部区域
- **AND** 导航项应保持可识别的当前页状态，但不再使用圆角按钮风格

### Requirement: 首页展示内容
系统 SHALL 将首页从“图像上叠加文案与入口”的结构，修改为“右侧仅保留主视觉图像、左侧承担全部文字与导航”的结构。

#### Scenario: 查看首页图像区
- **WHEN** 用户查看首页的主视觉图像
- **THEN** 图像区域应仅承担图像展示功能
- **AND** 不应再显示欢迎语、Quote、Explore、About 按钮等叠加内容

### Requirement: 内容页视觉一致性
系统 SHALL 让 Music、Films、Fragments、Thoughts、About 与详情页继承新的直角风格、淡蓝主色和细长文字系统。

#### Scenario: 在不同内容页之间切换
- **WHEN** 用户从首页进入各个内容页
- **THEN** 页面应共享一致的颜色、边框、字体与比例关系
- **AND** 文字系统应延续新的细长风格
- **AND** 内容页中原有圆角外观应被移除

## REMOVED Requirements
### Requirement: 首页图像叠加欢迎语与 Explore 面板
**Reason**: 用户明确要求首页图片区域只保留图像本身，文字和导航只出现在左侧。
**Migration**: 删除首页图片上的欢迎语、Quote、Explore 卡片和 About 按钮，将必要导航保留在左侧信息栏。

### Requirement: 前台圆角卡片语言
**Reason**: 用户明确要求网页中的圆角元素全部删除，当前圆角卡片风格与目标参考图冲突。
**Migration**: 将前台模板中的圆角类统一改为直角布局，并重调边框、间距与配色以维持层次感。
