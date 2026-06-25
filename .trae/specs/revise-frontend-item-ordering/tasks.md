# Tasks
- [x] Task 1: 调整音乐与 Film 前台列表排序
  - [x] 定位音乐与 Film 列表查询当前的排序来源
  - [x] 将音乐列表改为按添加顺序展示
  - [x] 将 Film 列表改为按添加顺序展示

- [x] Task 2: 调整博客前台列表排序
  - [x] 定位博客列表查询当前的排序来源
  - [x] 将博客列表改为按添加顺序展示
  - [x] 验证详情页跳转与列表渲染不受影响

- [x] Task 3: 保持照片墙排序逻辑不变
  - [x] 核对照片墙当前排序来源
  - [x] 确保本次改动不影响照片墙列表顺序

- [x] Task 4: 联调与验证排序规则
  - [x] 运行 Django 检查与必要测试，验证音乐、Film、博客的前台顺序已按添加顺序展示
  - [x] 验证照片墙顺序保持不变，且本轮改动未引入其他列表页回归

# Task Dependencies
- `Task 2` can run in parallel with `Task 1`
- `Task 3` can run in parallel with `Task 1` and `Task 2`
- `Task 4` depends on `Task 1`, `Task 2`, and `Task 3`
