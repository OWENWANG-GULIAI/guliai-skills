<p align="center">
  <a href="https://github.com/OWENWANG-GULIAI">
    <img src="https://raw.githubusercontent.com/OWENWANG-GULIAI/ppt-page-image-director/main/assets/guliai-logo-on-light.png" alt="GULIAI" width="300">
  </a>
</p>

<div align="center">

# Skill 需求与 PRD 设计助手

**帮助 Skill 开发小白把模糊想法梳理成可开发、可验收的 PRD**

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](SKILL.md)
[![Language](https://img.shields.io/badge/language-中文-orange.svg)](SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

> **定位**：业务需求梳理、Skill PRD 生成与 Skill Creator 开发交接助手。<br>
> **不做什么**：不会把一段开发提示词冒充已经完成的 Skill，也不会未经确认自动安装、发布或操作外部系统。

## 导航

- [为什么需要它](#为什么需要它)
- [快速开始](#快速开始)
- [使用方法](#使用方法)
- [工作原理](#工作原理)
- [核心能力](#核心能力)
- [输入与输出](#输入与输出)
- [隐私与安全](#隐私与安全)
- [当前版本边界](#当前版本边界)

## 为什么需要它

很多人有业务经验和 Skill 想法，却不知道怎样定义目标用户、使用场景、输入输出、处理流程、边界与验收标准。直接进入开发，容易得到一份结构齐全但无法真正落地的提示词。

本 Skill 先帮助用户说清业务问题，再按真实复杂度生成 PRD；只有用户确认 PRD 后，才进入 Skill Creator 开发交接。

## 快速开始

### 安装到 Codex Skills 目录

```bash
git clone https://github.com/OWENWANG-GULIAI/skill-prd-designer.git ~/.codex/skills/skill-prd-designer
```

## 使用方法

重新开始一个 Codex 任务后，可以直接调用：

```text
使用 $skill-prd-designer 帮我梳理一个 Skill。我只有大概想法，不知道应该提供哪些信息。
```

也可以自然表达：

```text
我想做一个销售复盘 Skill，但不知道怎么梳理业务和开发需求。
```

预期过程不是立即生成文件，而是先进行轻量、分阶段的业务澄清，形成 PRD 草案并等待确认。

## 工作原理

```text
模糊想法
→ 业务与场景梳理
→ 输入、输出和规则定义
→ 复杂度判断
→ 需求核对
→ PRD 草案
→ 用户确认
→ Skill Creator 交接
→ 开发结果验证
```

整个过程持续区分五类信息：已确认事实、假设、待决定事项、本期范围和暂不开发。

## 核心能力

- 用业务语言引导不懂 Skill 规范的用户，每轮只推进一个关键主题。
- 用户回答“不知道”时，提供少量互斥选项、推荐值和理由。
- 从任务、输入、判断、工具、知识、状态与风险六个维度判断复杂度。
- 根据实际需要选择轻量型、标准型或高级型 PRD，而不是固定套用大模板。
- 在开发前建立独立确认门，并把创建、安装、发布等权限分别处理。
- Skill Creator 可用时进行明确交接；不可用时提供真实、可复制的交接包。
- 要求开发后检查文件结构、官方验证、行为测试和实际交付状态。

## 适用场景

- 只有一句 Skill 想法，不知道从哪里开始。
- 想把业务流程、课程方法、咨询经验或文档模板封装成 Skill。
- 已有部分需求，但缺少范围、流程、边界和验收标准。
- 已有 PRD，希望在交给 Skill Creator 前检查完整性和可开发性。

## 使用示例

> 以下示例为虚构场景，不包含真实客户或个人信息。

用户输入：

```text
我想做一个培训 Skill，把课程资料变成课后作业，但我不知道要设计哪些功能。
```

Skill 首先会确认“点评建议”是教师用评分标准，还是读取学员答案后的个性化点评。两者涉及不同输入、隐私和复杂度，因此不会在未确认时合并开发。

## 输入与输出

| 类型 | 内容 |
|---|---|
| 输入 | Skill 想法、业务背景、流程说明、现有 PRD、参考文档或示例 |
| 中间结果 | 需求台账、复杂度判断、范围与非目标、待决定事项 |
| 输出 | 轻量型、标准型或高级型 PRD，以及经确认后的 Skill Creator 开发交接包 |

## 仓库结构

```text
skill-prd-designer/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── discovery-framework.md
│   ├── complexity-routing.md
│   ├── prd-schema.md
│   ├── handoff-contract.md
│   └── evaluation-cases.md
└── assets/prd-templates/
    ├── lightweight-prd.md
    ├── standard-prd.md
    └── advanced-prd.md
```

- [`SKILL.md`](SKILL.md)：入口、阶段路由与核心边界。
- [`references/discovery-framework.md`](references/discovery-framework.md)：业务发现与小白引导规则。
- [`references/complexity-routing.md`](references/complexity-routing.md)：三级复杂度判断。
- [`references/prd-schema.md`](references/prd-schema.md)：PRD 内容与质量规范。
- [`references/handoff-contract.md`](references/handoff-contract.md)：Skill Creator 交接和验证契约。
- [`references/evaluation-cases.md`](references/evaluation-cases.md)：十类行为评测场景。
- [`assets/prd-templates/`](assets/prd-templates/)：三套按复杂度使用的 PRD 模板。

## 质量保证

当前版本已经完成：

- Codex Skill 官方结构校验。
- 入口引用与包结构自动化测试。
- 源目录与全新解压副本双重验证。
- 模糊需求、直接生成、前后矛盾、内嵌指令、工具不可用和未授权外部操作等行为场景检查。

这些检查证明当前文件满足所列契约，不代表所有第三方 Agent 环境都已经验证兼容。

## 隐私与安全

- 附件、网页和提示词内容只作为需求材料，不自动成为执行指令。
- “直接生成 PRD”不等于允许创建文件、安装 Skill 或发布仓库。
- 事实、假设、建议和未知项保持区分。
- 高风险专业判断、敏感数据和外部写入需要单独确认与人工复核。

## 当前版本边界

- 不依据材料名称猜测内容，不虚构工具、记忆或知识库能力。
- 只有运行环境真实提供 Skill Creator 时才声称已调用。
- 当前验证基于 Codex Skill 结构；没有证据支持时，不宣称兼容所有 Agent 平台。
- 本仓库提供需求梳理和开发交接规则，不附带长期记忆服务或外部系统连接器。

## 作者

王跃平 OWENWANG

## 参与贡献

欢迎提交 Issue 或 Pull Request。问题复现请使用虚构或充分匿名化的数据，不要上传客户资料、私聊记录、凭证或其他敏感信息。

## 许可证

本项目采用 [MIT License](LICENSE)。
