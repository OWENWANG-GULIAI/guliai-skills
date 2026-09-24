---
name: guliai-daily-signature
description: Use when a user asks for a GULIAI daily-signature poster, today/tomorrow daily quote, weekday poster series, or matching WeChat Moments copy.
---

# GULIAI 日签海报

生成一张可发布的 2:3 谷燕燕个人品牌日签，并同步交付纯正文 `朋友圈文案.md`。内容每天变化，品牌骨架、人物身份和真实资产保持稳定。

**REQUIRED SUB-SKILL:** Use imagegen for the creative poster base.

## 运行顺序

1. 读取 `state/local-config.json`。文件缺失或素材失效时，读取 [素材合同](references/asset-contract.md)，只补齐缺失配置。
2. 用 `scripts/daily_signature_ops.py resolve-date` 解析今天、明天、昨天或明确日期；以配置时区为准，不采信用户手写星期。
3. 用户已给主题或金句时忠实使用；否则读取 [选题来源](references/content-sourcing.md)，从当前上下文、获授权的历史对话或私有理念库中选择一条可追溯、近 30 天未重复的观点。
4. 读取 [文案规范](references/copy-guide.md)，形成主标题、星期标签、2–3 行正文、英文点缀和 80–130 字朋友圈正文。朋友圈临时文件只写可发布正文。
5. 读取 [视觉系统](references/visual-system.md) 与 [底部安全区合同](references/layout-contract.json)。从配置中的人物资产池按主题选择一张人物参考与一种构图路线；日期卡、二维码和 Logo 保持稳定安全区，人物、标题、正文、英文点缀及人物标签必须围绕人物姿态动态排版。用 imagegen 一次生成包含人物、日期卡和全部指定文字的完整创意底图；底部二维码与 Logo 区必须是连续自然背景，不得出现占位色块，也不得有任何人物、手、衣物、道具或文字侵入真实资产覆盖区。
6. 用 `view_image` 逐字检查底图。日期、文字、人物、双图钉、人物标签、服装与袖子结构、信息层级、构图可读性或底部安全区任一失败，只针对失败项重生完整底图；最多两次自动返工。
7. 底图通过后，用 `daily_signature_ops.py compose` 叠加真实二维码和官方 Logo。此确定性后置合成是二维码可用性与 Logo 保真的必要步骤。
8. 读取 [验收清单](references/qa-checklist.md)，目视检查最终图，再运行 `daily_signature_ops.py validate`。只有两项都通过，才运行 `publish` 同时替换输出目录中的固定文件。
9. 更新私有 `state/usage-log.json` 的来源摘要、主题与日期。仅记录公开安全的忠实摘要，不复制敏感聊天内容。

## 交付合同

- 海报：`今日日签海报.png`，1024×1536 PNG。
- 文案：`朋友圈文案.md`，文件第一字到最后一字均属于可直接发布的朋友圈正文；保留语义换行和段落空行。
- 默认回复只展示海报预览、两个文件链接，并说明二维码与 Logo 使用原始素材合成。
- 任一步失败时保留上一组正式文件，报告具体失败项；不得把预览底图称为最终版。

运行脚本前可执行：

```bash
python3 scripts/daily_signature_ops.py --help
```
