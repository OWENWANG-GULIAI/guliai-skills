---
name: enterprise-training-outline-designer
description: Run a consultation-style enterprise training discovery and create confirmed client-facing course outlines or branded proposals. Use when a client provides a training request, chat records, meeting notes, or a draft brief and needs corporate-training diagnosis, a course outline, a Word proposal, or an HTML proposal. Ask one adaptive discovery question at a time, confirm the consolidated requirements before generating, and route Word/HTML work through the selected template and brand assets.
---

# 企业内训大纲设计器

将模糊培训需求转成经用户确认的课程大纲或客户方案。严格遵循状态门禁；不得跳过访谈、确认或交付物选择。

## 状态门禁

| 状态 | 允许动作 | 禁止动作 |
|---|---|---|
| `discovery` | 提取已知信息、每次问一个缺失的关键问题 | 正式大纲、默认假设、Word/HTML 文件 |
| `brief_confirmation` | 展示《课程需求确认单》，等待“补充 / 修改 / 直接开始生成” | 课程大纲、文档文件 |
| `delivery_confirmation` | 确认格式、Logo、品牌色和模板 | 生成 Word/HTML 文件 |
| `generation` | 输出用户确认的内容或文件 | 未选格式的额外交付物 |
| `verification` | 检查结构、时长、文件布局和资产使用 | 未校验即交付 |

不要把推断写成客户事实。用户说“直接给我大纲”但关键字段不完整时，仍留在 `discovery`，只问下一道问题。

## 1. 自适应逐题访谈

建立 `Training Brief`，字段见 [brief-schema.md](references/brief-schema.md)。读取聊天记录、会议纪要、附件和用户上传材料后，自动填入已知字段；每轮只问一个尚未确认、且最影响设计的问题。

使用 [adaptive-interview.md](references/adaptive-interview.md) 决定下一题。必要时运行：

```powershell
python scripts/next_interview_question.py <brief.json>
python scripts/validate_training_brief.py <brief.json>
```

在回答中只输出：简短承接语、当前的一道问题，以及该问题影响什么。不要同时列出问题清单，不要给出课程结构草案。

## 2. 需求确认

当核心字段均已确认时，进入 `brief_confirmation`。使用 [requirement-confirmation-template.md](references/requirement-confirmation-template.md) 输出《课程需求确认单》，清楚分开：

- 客户已确认事实；
- 设计理解；
- 未确认或不可用信息；
- 拟达成的学习成果；
- 交付假设。

结尾必须逐字询问：

> 以上理解是否准确？你可以选择“补充”“修改”或“直接开始生成”。

只有用户明确选择“直接开始生成”或同义确认，才能进入下一状态。

## 3. 交付物确认

在生成内容前，按 [output-routing.md](references/output-routing.md) 逐项确认：

1. 输出形式：聊天版、Markdown、Word 或 HTML；
2. 是否需要企业名称、Logo、品牌色或其他品牌规范；
3. 是否有现成 Word/HTML 模板。

若用户已在同一句话完整提供这些信息，可直接复述并请其确认；否则每轮只问一个缺失项。未确认 Word/HTML 需求时，默认生成聊天版或 Markdown，不创建文件。

## 4. 生成与模板规则

客户版内容结构使用 [client-proposal-structure.md](references/client-proposal-structure.md)，课程设计使用 [course-design-rules.md](references/course-design-rules.md)，并遵循 [course-outline-reference-template.md](references/course-outline-reference-template.md)。每个模块必须说明解决问题、内容/方法、学习方式和模块产出。

- **聊天版 / Markdown**：按参考模板的内容顺序输出客户版方案文案；表格保留“相对时间 / 模块 / AI 或讲师动作 / 学员获得什么”等可对照字段。Markdown 正文与表格使用 1.5 倍行距等效的可读性间距。
- **Word**：使用 `documents` Skill。默认参考模板是 Skill 包内的 `assets/word-consulting-proposal-template.docx`；先按 `documents` Skill 的模板蒸馏流程读取它，再从其副本改写。保留其封面、章节顺序、页眉页脚、表格层级和视觉系统，但必须把客户名称、课程名称、业务情境、工具名称和案例内容替换为本次已确认内容，不得沿用模板中的占位信息。所有正文段落及表格单元格段落必须设为 **1.5 倍行距**；封面标题、页眉页脚等非正文元素按模板保留，除非用户另有要求。用户后来提供的 Word 模板优先于包内默认模板。
- **HTML**：若用户提供模板，先读取并沿用其结构和视觉系统；否则按参考模板的章节与表格结构创建响应式方案页。正文和表格文字使用 `line-height: 1.5`。
- **品牌资产**：用户提供的 Logo、品牌色和模板优先于默认资产；不得将客户资产复制进可复用 Skill 包。没有品牌资产时使用无品牌默认模板。

Word 文件必须完成渲染与页面检查；HTML 页面必须检查响应式布局和文字可读性。无法读取用户模板时，说明原因，并询问是否改用默认模板。

## 5. 交付前检查

确认：需求确认状态已获通过、格式已选定、Logo/品牌/模板已询问、时间加总正确、所有模块均有产出、事实与判断分开、客户需配合事项和范围边界完整。对 Word/HTML 还确认实际使用的模板和品牌资产；对 Word 确认正文与表格单元格均为 1.5 倍行距，并在渲染检查中确认没有由此造成溢出、截断或异常分页。
