---
name: guliai-wechat-automation-suite
description: "Install and use the GULIAI WeChat automation skill suite: writing, information-carrying visuals, typesetting, and saving reviewed articles to the WeChat draft box."
---

# GULIAI 公众号自动化套件

这是一个多 Skill 套件仓库。安装时，将 `skills/` 目录下的三个子目录复制到 Codex 的 Skills 目录，再安装 README 中列出的两个外部依赖。

完整请求使用 `guyanyan-wechat-pipeline`；只写内容使用 `guyanyan-wechat-writer`；只生成知识卡或横版封面使用 `guliai-visual-design`。

所有涉及公众号的完整流程只会保存草稿，不会自动群发、发布、定时发送或删除既有草稿。详细配置、公开边界和安装方法见 [README](README.md)。
