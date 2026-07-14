# eMagzines

使用 GitHub Actions 定时抓取英文杂志，并生成 PDF 和 EPUB 文件。生成的文件会发布为 GitHub Release Assets，目前抓取的杂志包括：

- The Economist

- The New Yorker
- TIME

推荐从 [Magazine Index](INDEX.md) 浏览和下载，也可以直接进入仓库的 [Releases](https://github.com/plsy1/emagzines/releases) 页面下载。

## 个人使用

### 使用 GitHub Actions

1. Fork 本仓库到你的 GitHub 账号。
2. 打开 Fork 后仓库的 **Actions** 页面，按提示启用工作流。
3. 进入 **Settings → Actions → General → Workflow permissions**，选择 **Read and write permissions** 并保存。
4. 返回 **Actions** 页面，在左侧选择要抓取的杂志工作流。
5. 点击 **Run workflow**，可选填写日期或 TIME 杂志页面 URL；如需替换已有同一期文件，可勾选 **Overwrite existing Release assets**，然后开始运行。

不填写参数时会尝试抓取最新一期。The Economist 和 The New Yorker 的日期可使用 `YYYY-MM-DD` 格式；工作流会分别对齐到最近的周六和周一。TIME 抓取历史期刊时可填写对应的杂志页面 URL。

工作流成功后，PDF 和 EPUB 会出现在你自己 Fork 的 Releases 页面。`INDEX.md` 会在新刊发布后自动更新，也可以通过 **Update magazine index** 工作流手动刷新。

### 在本地运行

本地运行需要安装 [Docker](https://www.docker.com/) 和 [act](https://github.com/nektos/act)，并准备一个对目标仓库具有写入权限的 GitHub Token。

可以在项目根目录创建 `.secrets` 文件：

```text
GITHUB_TOKEN=你的_GitHub_Token
```

然后运行：

```bash
# 抓取最新一期经济学人
./run_local.sh te

# 抓取指定日期
./run_local.sh te 你的_GitHub_Token 2024-05-04

# 其他杂志使用 ny 或 tm
./run_local.sh ny
```

`.secrets`、生成的电子书和本地缓存均已加入 `.gitignore`。

## 自动更新

三种杂志都配置了定时工作流，也可以随时手动触发。同一期重复运行时，默认保留已有 Release 和 PDF、EPUB，不会覆盖或重复创建；手动运行并开启 **Overwrite existing Release assets** 后，才会使用新生成的文件替换原有资产。定时任务始终使用默认的不覆盖行为。

## 主要组件

- [Calibre](https://calibre-ebook.com/) 负责抓取、EPUB 生成和 PDF 转换。
- GitHub Actions 负责定时运行、发布 Releases 和维护下载索引。
- Cloudflare WARP 用于改善 GitHub Actions 运行时的网络连接。

## 说明

本项目仅供个人学习和技术研究使用。使用者应自行确保对相关内容的抓取、存储和传播符合当地法律、网站条款及版权要求。
