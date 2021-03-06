# pwsearch

PwnWiki 数据库搜索命令行工具。

## 安装

您可以直接用 `pip` 命令从 PyPI 安装 pwsearch：

```shell
pip3 install -U pwsearch
```

您也可以 clone 该仓库并直接从源码启动：

```shell
git clone https://github.com/pwnwikiorg/pwsearch.git
cd pwsearch
pip3 install -U -r pwsearch/requirements.txt
pwsearch search <Keyword> -t
pwsearch open -p <Page ID>
```

## 使用方法

![image](https://user-images.githubusercontent.com/21986859/121893584-1f098d80-ccec-11eb-927f-4d377807eb6f.png)

```shell
# 搜寻关键词
pwsearch search CVE-2019-0708

# 在浏览器中打开详细页面
pwsearch open -p 2051
```

## 友情链接

- 社區: https://forums.pwnwiki.org
- PwnWiki: https://www.pwnwiki.org
- 中文 Telegram 群組: https://t.me/pwnwiki_zh

