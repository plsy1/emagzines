## eMagzines 英文杂志自动抓取
使用 Github Actions 自动抓取英文杂志，提供 PDF 与 EPUB 两种格式。抓取结果保存在 `magzines` 分支中。

#### 📚 [**经济学人 (The Economist)**](https://github.com/plsy1/emagzines/tree/magzines/the_economist)

#### 📰 [**纽约客 (The New Yorker)**](https://github.com/plsy1/emagzines/tree/magzines/the_new_yorker)

#### ⏳ [**时代杂志 (TIME Magazine)**](https://github.com/plsy1/emagzines/tree/magzines/time_magzine)

---

### 使用说明

如果你想拥有自己的抓取副本，请先 **Fork** 本仓库。

#### 0. 准备工作 (仅需一次)
1. **Fork** 本仓库到你的个人账号。
2. 进入你 Fork 后的仓库，点击 **Actions** 并点击 **I understand my workflows, go ahead and enable them** 以启用工作流。
3. 确保你的仓库中存在 `magzines` 分支（Fork 时默认会包含，该分支用于存放生成的电子书）。

#### 1. 在 GitHub Actions 页面触发 (推荐)
1. 进入仓库的 **Actions** 选项卡。
2. 在左侧选择对应的杂志工作流（如 `The Economist`）。
3. 点击右侧的 **Run workflow** 下拉按钮。
4. 在弹出框中输入 **Issue Date** (格式：`YYYY-MM-DD`)。
    - *注：TIME 杂志输入的是 URL。*
    - *提示：经济学人（对齐到周六）和纽约客（对齐到周一）会自动将你输入的日期对齐到最近的出版日。*
5. 点击 **Run workflow** 开始运行。

#### 2. 本地命令行触发 (需要安装 [act](https://github.com/nektos/act))
如果你想在本地机器上运行抓取任务（结果会同步到 `magzines` 分支），可以使用提供的脚本：

```bash
# 赋予执行权限
chmod +x run_local.sh

# 抓取最新一期 (需要配置 .secrets 或传 Token)
./run_local.sh te

# 抓取指定日期
./run_local.sh te 你的GITHUB_TOKEN 2024-05-04
```

> **提示**：建议在本地创建 `.secrets` 文件并填写 `GITHUB_TOKEN=你的Token`，这样运行脚本时无需重复输入 Token。

---

### 技术栈

本项目基于以下技术构建：

- **核心引擎**：[Calibre](https://calibre-ebook.com/) - 强大的电子书管理与转换工具，利用其内置的 Recipe 系统进行网页抓取。
- **自动化**：[GitHub Actions](https://github.com/features/actions) - 实现每日定时自动抓取与推送。
- **网络优化**：集成 [Cloudflare WARP](https://github.com/fscarmen/warp-on-actions) 以优化抓取时的网络环境。
