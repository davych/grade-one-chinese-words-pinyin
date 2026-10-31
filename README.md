# 语文练习册

适合 A4 打印的一年级语文练习册。单个 HTML 内嵌全部样式、脚本、拼音、汉字矢量与笔顺数据，无需安装或联网。

**[在线使用](https://davych.github.io/grade-one-chinese-words-pinyin/)** · [使用说明](使用说明.txt)

## 练习内容

- **认一认**：119 个汉字，每字一个拼音田字格。屏幕可以显示或隐藏拼音，打印时拼音栏始终留空。
- **写一写**：75 个汉字，一字一行。默认 18 mm 田字格，每行首格预填范字，其余 9 格为空白。
- **笔顺参考**：显示或隐藏逐笔图示，点击范字可播放笔顺，也可逐步查看。
- **打印设置**：分类筛选、姓名、18 / 20 mm 格子、可选打印笔顺图。18 mm 默认全部内容为 13 页。

打印时选择 **A4、纵向、100% 缩放**，关闭浏览器的页眉和页脚。屏幕拼音与笔顺提示不改变默认练习页的留白。

## 本地使用与修改

直接用浏览器打开 `index.html`；只复制这个文件也能离线使用。

词表位于 `data/words.json`，笔顺数据位于 `data/strokes.json`，页面源模板位于 `tools/index.template.html`。修改后运行：

```sh
python3 tools/build.py
```

此可选维护脚本只使用 Python 标准库。日常使用练习册无需 Python，也无需构建。

## GitHub Pages 部署

仓库的 **Settings → Pages → Source** 使用 **GitHub Actions**。

推送到 `main` 自动运行 [Deploy GitHub Pages](https://github.com/davych/grade-one-chinese-words-pinyin/actions/workflows/deploy-pages.yml)，也可在 Actions 页面选择 **Run workflow** 手动触发。

工作流重新生成 HTML 并检查与已提交成品一致，然后仅发布 `index.html` 与数据许可证。源码、词表和本机检查产物不进入网站发布包。构建与部署使用独立任务，部署通过 `github-pages` 环境和 GitHub OIDC 完成，无需配置部署密钥。

## 词表与许可

按 [原始词表](原始词表.txt) 中实际列出的汉字整理：识字 121 条去重为 119 字，写字 77 条去重为 75 字；没有补齐原文标题声称的 300 / 100 字。两类之间的重合字分别保留，具体见 [校对说明](data/词表校对说明.txt)。

汉字字形与笔顺来自 [Hanzi Writer Data](https://github.com/chanind/hanzi-writer-data) / [Make Me a Hanzi](https://github.com/skishore/makemeahanzi)，覆盖两类并集 153 字。原始字形数据遵循 [Arphic Public License](data/ARPHICPL.TXT)，许可证也已内嵌在成品 HTML 中。版本和来源记录见 [笔顺数据来源](data/笔顺数据来源.txt)。

本机截图、打印检查 PDF 等保留在本地 `检查/`，不提交仓库。
