# 为 Lazy-Flask 贡献代码

感谢你对本项目的兴趣！🎉

我们欢迎各种形式的贡献，包括：修复 Bug、新功能、文档改进、测试补充等。

## 贡献流程

### 1. Fork & Clone
- 在 GitHub 上 Fork 本仓库到你的账号。
- 将你的 Fork 克隆到本地：
  ```bash
  git clone https://github.com/<your-username>/lazy-flask.git
  cd lazy-flask
  ```

### 2. 设置开发环境
- 安装依赖：
  ```bash
  pip install -r .
  ```
- 运行测试，确保一切正常：
  ```bash
  python -m unittest discover -s tests
  ```

### 3. 开发修改
- 新建分支：
  ```bash
  git checkout -b feature/my-feature
  ```
- 完成修改，如果涉及功能请补充相应测试，并提交。

### 4. 运行测试与代码检查
- 确认所有测试通过：
  ```bash
  python -m unittest discover -s tests
  ```

### 5. 提交 Pull Request
- 将分支推送到你的 Fork：
  ```bash
  git push origin feature/my-feature
  ```
- 在 GitHub 上发起 Pull Request，目标分支为 `master`。

---

## 行为准则
参与贡献即表示你同意遵守我们的 [行为准则](./CODE_OF_CONDUCT_zh.md)。
