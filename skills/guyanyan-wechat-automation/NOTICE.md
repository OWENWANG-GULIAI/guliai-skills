# 外部依赖说明

本仓库只包含 GULIAI 的工作流编排、写作路由、视觉规则和草稿幂等脚本；不复制外部 Skill 的源码。

运行完整工作流需要安装以下外部 Skill：

- [`gzh-design-skill`](https://github.com/isjiamu/gzh-design-skill)：将 Markdown 变为微信公众号适配的 HTML。其仓库以 AGPL-3.0 发布，使用、修改或再分发时请遵守其许可证。
- [`baoyu-skills`](https://github.com/JimLiu/baoyu-skills)：通过 API 或浏览器将文章保存到微信公众号草稿箱。请遵守其仓库中的许可证、配置和平台规则。

外部依赖的名称、接口或安装方式发生变化时，应以其上游仓库的当前说明为准。
