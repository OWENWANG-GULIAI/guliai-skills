<p align="center">
  <img src="skills/guliai-daily-signature/assets/guliai-logo-on-light.png" width="240" alt="GULIAI">
</p>

# GULIAI Skills

<p align="center">
  <a href="VERSION"><img src="https://img.shields.io/badge/Version-0.1.0-9f6b13" alt="version 0.1.0"></a>
  <a href="#技能目录"><img src="https://img.shields.io/badge/Docs-中文-2f7a65" alt="Chinese documentation"></a>
  <a href="LICENSES.md"><img src="https://img.shields.io/badge/License-per--package-6e7781" alt="per package license"></a>
  <a href="#技能目录"><img src="https://img.shields.io/badge/Packages-11-9f6b13" alt="11 packages"></a>
  <a href="#技能目录"><img src="https://img.shields.io/badge/Skills-14-2f7a65" alt="14 skills"></a>
</p>

GULIAI Skills 是谷粒 AI（GULIAI）维护的实用型 Codex Skill 合集。它把内容生产、个人品牌、课程设计、社群运营与 Skill 开发等能力放在一个可检索、可安装、可持续维护的目录中。

> **定位**：面向实际业务与内容生产的独立 Skill 集合与分发入口。<br>
> **不做什么**：不把 11 个独立能力伪装成一个根 Skill，也不以总仓库名义重新授权各包内容。

这里的每个目录都是独立 Skill 包：保留自己的 `SKILL.md`、说明、脚本、测试和许可文件；总仓库只负责集中发现与分发。

## 快速开始

克隆仓库后，把需要的单个 Skill 复制到本机 Codex Skills 目录即可：

```bash
git clone https://github.com/OWENWANG-GULIAI/guliai-skills.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R guliai-skills/skills/guliai-daily-signature "${CODEX_HOME:-$HOME/.codex}/skills/"
```

请只安装你需要的目录，并先阅读其 `SKILL.md`。不同运行环境的 Skill 安装方式可能不同；以你的运行环境文档为准。

## 技能目录

| 包目录 | 主要用途 | 来源 |
| --- | --- | --- |
| `chat-to-tutorial` | 将聊天记录整理为可交付教程 | [source](https://github.com/OWENWANG-GULIAI/chat-to-tutorial) |
| `content-to-flowchart-skill` | 将内容结构化为流程图 | [source](https://github.com/OWENWANG-GULIAI/content-to-flowchart-skill) |
| `enterprise-training-outline-designer` | 企业培训需求访谈与课程大纲设计 | [source](https://github.com/OWENWANG-GULIAI/enterprise-training-outline-designer) |
| `guliai-daily-signature` | 谷粒 AI个人品牌日签海报与朋友圈文案 | [source](https://github.com/OWENWANG-GULIAI/guliai-daily-signature) |
| `guyanyan-wechat-automation` | 谷燕燕 / GULIAI 微信内容生产流水线，并含写作与视觉子 Skill | [source](https://github.com/OWENWANG-GULIAI/guyanyan-wechat-automation) |
| `ppt-page-content-director` | 课程与演示文稿单页内容策划 | [source](https://github.com/OWENWANG-GULIAI/ppt-page-content-director) |
| `publishing-skills-to-github` | Skill 的公开发布、审计与 GitHub 同步 | [source](https://github.com/OWENWANG-GULIAI/publishing-skills-to-github) |
| `skill-assetdistiller` | 将职业经历提炼为可验证、可变现的经验资产 | [source](https://github.com/OWENWANG-GULIAI/skill-assetdistiller) |
| `skill-prd-designer` | 为 Agent Skill 设计可执行 PRD | [source](https://github.com/OWENWANG-GULIAI/skill-prd-designer) |
| `student-feedback-poster` | 将真实学员反馈制作成品牌海报 | [source](https://github.com/OWENWANG-GULIAI/student-feedback-poster) |
| `wechat-group-intelligence` | 社群聊天记录的洞察、运营与内容提炼 | [source](https://github.com/OWENWANG-GULIAI/wechat-group-intelligence) |

完整机器可读目录见 [catalog.json](catalog.json)。

## 维护原则

- 每个 Skill 在 `skills/<package>/` 内独立演进；子目录的规则优先于总仓库说明。
- 同步前检查隐私、凭据、本机绝对路径和运行时状态；不把个人素材、私有知识库或本机状态提交到公开仓库。
- 总仓库不删除、不归档现有独立仓库，避免破坏已有链接。迁移或归档需单独确认。
- 聚合仓库是统一发现与分发入口；每次更新都需保留来源映射，并完成包级校验。
- 当前采用“上游仓库更新后同步到合集”的单向维护方式；不会自动双向同步。若未来要把合集改为唯一维护源，需要单独迁移与公告。

## 许可与使用边界

本仓库**不提供统一的总许可证**。请以各包目录中的 `LICENSE` 为准，并在使用、修改或再发布前阅读 [LICENSES.md](LICENSES.md)。其中 `content-to-flowchart-skill` 的上游目前未提供许可证，合集不会替其授予任何使用许可。

## 版本

集合仓库当前版本：[`0.1.0`](VERSION)。
