# 导航品牌、About 与媒体展示精简 Spec

## Why
最近一轮前台微调后，非首页导航缺少回到首页的直接入口，首页品牌名也偏离了原先约定；同时 About 页虽然保留了头像，但 Elsewhere 的呈现不再符合之前确认过的规格，音乐和 Film 展示页也保留了不必要的简介文案。需要做一次小范围修正，恢复既有信息层级和浏览路径。

## What Changes
- 在非首页展开导航中增加一个英文的回到首页按钮
- 将首页品牌名恢复为原先约定的样式与文案
- 保留 About 页头像展示，同时按既有规格重新恢复 Elsewhere 区块
- 移除音乐和 Film 展示页中的简介文案，仅在详情页保留简介
- 确保上述调整不影响现有五个主选单、高亮逻辑与移动端可用性

## Impact
- Affected specs: 非首页导航入口、首页品牌展示、About 页面资料呈现、音乐与 Film 展示页信息层级
- Affected code: `base.html` 导航模板与脚本、首页模板或首页上下文、About 模板、媒体列表模板与相关测试

## ADDED Requirements
### Requirement: 非首页导航提供回到首页入口
系统 SHALL 在非首页页面的可展开导航中提供一个英文的回到首页按钮，方便用户从任意内容页直接返回首页。

#### Scenario: 用户打开非首页导航
- **WHEN** 用户在音乐、Film、Fragments、Thoughts 或 About 页面展开导航
- **THEN** 导航中显示一个英文的回到首页按钮
- **AND** 点击后返回首页
- **AND** 该按钮不替代原有五个主选单，而是作为附加入口存在

### Requirement: About 页面保留头像并恢复 Elsewhere
系统 SHALL 在保留个人资料头像展示的同时，按既有规格恢复 Elsewhere 区块的展示方式。

#### Scenario: 资料已配置头像与 Elsewhere
- **WHEN** 用户访问 About 页面
- **THEN** 页面继续展示头像
- **AND** Elsewhere 重新出现
- **AND** Elsewhere 的展示方式与此前确认过的规格一致

#### Scenario: 资料未配置 Elsewhere
- **WHEN** 用户访问 About 页面且后台未填写任何 Elsewhere 链接
- **THEN** 页面仍正常渲染
- **AND** 不出现多余占位内容

### Requirement: 音乐与 Film 展示页不显示简介
系统 SHALL 在音乐与 Film 的展示页中移除简介文案，只保留更简洁的卡片信息，简介内容继续放在详情页展示。

#### Scenario: 用户浏览音乐或 Film 展示页
- **WHEN** 用户打开音乐或 Film 列表页面
- **THEN** 每张卡片不再显示简介摘要
- **AND** 卡片仍保留作品基本识别信息和详情入口

#### Scenario: 用户进入音乐或 Film 详情页
- **WHEN** 用户从展示页进入某个作品详情页
- **THEN** 详情页继续展示完整简介
- **AND** 展示页的信息收口不会影响详情阅读

## MODIFIED Requirements
### Requirement: 首页品牌信息恢复原样
系统 SHALL 将首页品牌区中的品牌名恢复为原先约定的文案与样式，不继续沿用最近偏离规格的改动。

#### Scenario: 用户访问首页
- **WHEN** 首页加载完成
- **THEN** 首页品牌名显示为原先版本
- **AND** 其余首页品牌信息与当前导航结构保持兼容

### Requirement: 非首页导航保持极简结构并增加 Home 入口
系统 SHALL 在保持非首页导航极简风格的基础上，只额外增加一个 Home 入口，不恢复其他已移除的说明性内容。

#### Scenario: 用户查看非首页导航
- **WHEN** 非首页导航展开
- **THEN** 导航仍以主选单和简洁信息为主
- **AND** 只新增 Home 入口
- **AND** 不引入额外冗余说明文案
