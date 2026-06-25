# Tasks
- [x] Task 1: 为非首页导航补回 Home 入口
  - [x] 调整非首页导航模板，在现有极简结构中新增英文 Home 按钮
  - [x] 保持现有五个主选单、当前页高亮和展开收起逻辑不受影响
  - [x] 验证桌面端与移动端都能通过该入口返回首页

- [x] Task 2: 恢复首页品牌名为原先版本
  - [x] 定位当前首页品牌名与样式来源
  - [x] 将首页品牌名恢复为此前确认的原始文案
  - [x] 验证首页品牌区其余信息与布局保持稳定

- [x] Task 3: 在 About 页面保留头像并按原规格恢复 Elsewhere
  - [x] 保持当前头像展示逻辑不回退
  - [x] 对照此前确认过的 About 规格恢复 Elsewhere 区块
  - [x] 验证 Elsewhere 缺失时页面仍正常渲染，无多余占位

- [x] Task 4: 精简音乐与 Film 展示页信息层级
  - [x] 调整音乐展示页卡片，移除简介摘要
  - [x] 调整 Film 展示页卡片，移除简介摘要
  - [x] 验证简介仍仅在详情页展示，不影响现有详情入口与元信息

- [x] Task 5: 联调与验证导航、About 与媒体展示页修正
  - [x] 运行 Django 检查与必要测试，确认导航、首页、About 与媒体展示页改动正常
  - [x] 验证非首页 Home 入口、首页品牌名恢复、About 头像与 Elsewhere、媒体展示页去简介均符合规格

# Task Dependencies
- `Task 2` can run in parallel with `Task 1`
- `Task 3` can run in parallel with `Task 1` and `Task 2`
- `Task 4` can run in parallel with `Task 1`, `Task 2`, and `Task 3`
- `Task 5` depends on `Task 1`, `Task 2`, `Task 3`, and `Task 4`
