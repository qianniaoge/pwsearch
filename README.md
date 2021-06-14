# pwsearch

PwnWiki 数据库搜索命令行工具。

## 安装

*该应用处于 alpha 测试阶段，该页面内容不准确。*

您可以直接用 `pip` 命令从 PyPI 安装 pwsearch：

```shell
pip install -U pwsearch
```

您也可以 clone 该仓库并直接从源码启动：

```shell
git clone https://github.com/k4yt3x/pwsearch
cd pwsearch
pip install -U -r pwsearch/requirements.txt
python -m pwsearch -k CVE
```

## 使用方法

```shell
# 搜寻关键词
pwsearch -k CVE-2019-0708

# 最大搜索结果
pwsearch -r 20 -k CVE-2019
```

## 友情链接

- 社區: https://forums.pwnwiki.org/t/23
- PwnWiki: https://www.pwnwiki.org
- 中文 Telegram 群組: https://t.me/pwnwiki_zh
