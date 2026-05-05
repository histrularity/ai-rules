# gitea 使用说明

## 环境设置

通过 HTTP API 操作 gitea, 不使用 tea 命令 (tea命令在非交互式环境下有大量问题)。

认证 token 从 `~/.config/tea/config.yml` 中读取, 通过 Header `Authorization: token <TOKEN>` 传入, 不要硬编码。

## 基础信息获取

从 `git remote -v` 的输出中解析出 gitea 的 host 和 owner/repo, 端口固定 5000, API 地址为 `http://<host>:5000/api/v1`。

如果不在 git 仓库中, 需要用户指定。

## 常用操作

以下示例中 `$TOKEN` 为从配置文件读取的 token, `$BASE` 为 API 地址, `$REPO` 为 `owner/repo`。

### 列出 issue

```bash
curl -s -H "Authorization: token $TOKEN" "$BASE/repos/$REPO/issues?state=open&limit=20&type=issues"
```

参数: `state` 可选 open/closed/all, `limit` 控制数量, `page` 翻页, `type=issues` 只返回 issue 不含 pull request。

### 查看单个 issue

```bash
curl -s -H "Authorization: token $TOKEN" "$BASE/repos/$REPO/issues/1"
```

### 查看 issue 评论

```bash
curl -s -H "Authorization: token $TOKEN" "$BASE/repos/$REPO/issues/1/comments"
```

### 创建 issue

```bash
curl -s -X POST -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"标题","body":"内容"}' \
  "$BASE/repos/$REPO/issues"
```

### 评论 issue

```bash
curl -s -X POST -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"body":"评论内容"}' \
  "$BASE/repos/$REPO/issues/1/comments"
```

### 列出合并请求 (Pull Request)

```bash
curl -s -H "Authorization: token $TOKEN" "$BASE/repos/$REPO/pulls?state=open&limit=20"
```

### 查看单个合并请求

```bash
curl -s -H "Authorization: token $TOKEN" "$BASE/repos/$REPO/pulls/1"
```

### 评论合并请求

合并请求的评论和 issue 共用同一个接口:
```bash
curl -s -X POST -H "Authorization: token $TOKEN" -H "Content-Type: application/json" \
  -d '{"body":"评论内容"}' \
  "$BASE/repos/$REPO/issues/1/comments"
```

### 查看仓库文件内容

直接用 raw 地址访问, 不需要 token (公开仓库), 返回纯文本:
```bash
curl -s "http://<host>:5000/$REPO/raw/branch/main/path/to/file"
```

其中 `branch/main` 可以换成其它分支或 `tag/v1.0` 等。如果是私有仓库, 加上 token header。

### 列出仓库目录文件

```bash
curl -s -H "Authorization: token $TOKEN" "$BASE/repos/$REPO/contents/?ref=main"
curl -s -H "Authorization: token $TOKEN" "$BASE/repos/$REPO/contents/my_dir?ref=main"
```

返回 JSON 数组, 每个条目有 `name`、`type` (file/dir)、`size` 等字段。路径为空或 `/` 表示根目录。

### 搜索仓库

```bash
curl -s -H "Authorization: token $TOKEN" "$BASE/repos/search?q=关键词&limit=10"
```

## 注意事项

1. API 返回的都是 JSON, 用 python3 解析即可, 注意 `json.dumps` 时 `ensure_ascii=False`
2. 创建/评论等写入操作的请求体用 JSON 格式, 需要 `Content-Type: application/json`
3. 完整 API 文档可访问 `http://<host>:5000/api/swagger`
4. 如果需要其它未列出的操作, 参考 swagger 文档或 gitea 官方 API 文档
