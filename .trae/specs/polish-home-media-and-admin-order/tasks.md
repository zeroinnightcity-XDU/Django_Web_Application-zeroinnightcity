# Tasks
- [x] Task 1: 调整首页品牌区的名称顺序
  - [x] 定位首页品牌区模板与上下文来源
  - [x] 将网站名和名字的位置互换
  - [x] 验证首页品牌区其余排版与导航逻辑不受影响

- [x] Task 2: 精简音乐与 Film 展示页卡片信息
  - [x] 调整音乐展示页卡片，移除类别标签
  - [x] 调整 Film 展示页卡片，移除类别标签
  - [x] 验证标题、创作者、年份和详情入口仍正常展示

- [x] Task 3: 收口照片墙展示页原图入口
  - [x] 调整照片墙展示页，移除查看原图入口
  - [x] 保留图片进入详情页的主要浏览路径
  - [x] 验证照片详情页仍保留查看原图入口

- [x] Task 4: 调整后台管理首页模型入口顺序
  - [x] 定位 Django Admin 首页模型分组与排序来源
  - [x] 将后台首页模型顺序调整为“音乐/电影”“照片墙”“博客”“首页与个人资料”
  - [x] 验证新增与修改入口仍可正常访问

- [x] Task 5: 联调与验证本轮微调
  - [x] 运行 Django 检查与必要测试，确认首页、列表页、详情页和后台首页改动正常
  - [x] 验证品牌区顺序、媒体卡片去类别、照片墙列表去原图、后台顺序均符合规格

# Task Dependencies
- `Task 2` can run in parallel with `Task 1`
- `Task 3` can run in parallel with `Task 1` and `Task 2`
- `Task 4` can run in parallel with `Task 1`, `Task 2`, and `Task 3`
- `Task 5` depends on `Task 1`, `Task 2`, `Task 3`, and `Task 4`
