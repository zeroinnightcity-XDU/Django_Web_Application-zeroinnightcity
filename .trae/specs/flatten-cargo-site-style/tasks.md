# Tasks
- [x] Task 1: 重设全局视觉基础
  - [x] 调整 `base.html` 的主色板，从当前暖灰/米色切换为低饱和度淡蓝色
  - [x] 更新全局字体引入与 Tailwind 字体映射，使中英文正文、导航和辅助信息都改为更细长的字体
  - [x] 保持当前大标题字体策略不变

- [x] Task 2: 去除前台圆角并重排基础骨架
  - [x] 移除 `base.html` 中导航项、信息块和布局容器的圆角样式
  - [x] 将 `Wentong Zou` 与年份时间戳移动到左侧信息栏底部
  - [x] 保持当前导航高亮逻辑，但将其改为直角风格表达

- [x] Task 3: 重构首页为 Cargo 风格全屏图布局
  - [x] 将首页右侧图片改为更接近全屏的主视觉区域
  - [x] 删除图片上叠加的欢迎语、Quote、Explore 与 About 按钮
  - [x] 保留左侧网站名、姓名与导航，并重新平衡首页左右比例
  - [x] 确保移动端仍能保持清晰的层级和可访问性

- [x] Task 4: 将内容页同步为去圆角与细长文字系统
  - [x] 更新 `Music` / `Films` 列表页与详情页的边框、文字和比例
  - [x] 更新 `Fragments`、`Thoughts`、`About` 页的边框、文字和比例
  - [x] 保持现有图片网格与内容结构，不额外改动数据来源与功能
  - [x] 保留 `About` 页的社交媒体链接区域

- [x] Task 5: 验证风格统一与页面行为
  - [x] 验证首页不再显示图片叠加文字和导航模块
  - [x] 验证前台页面圆角已移除，左下角页脚定位正确
  - [x] 验证淡蓝主色和新字体已应用到主要前台页面
  - [x] 运行 Django 检查，确保模板和路由行为正常

# Task Dependencies
- `Task 2` depends on `Task 1`
- `Task 3` depends on `Task 1` and `Task 2`
- `Task 4` depends on `Task 1` and `Task 2`
- `Task 5` depends on `Task 2`, `Task 3`, and `Task 4`
