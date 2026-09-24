# Input Handling

Read this reference whenever chat content must be extracted, normalized, filtered, chunked, or compared across groups.

## Establish the analysis envelope

Record what is actually available:

|Field|Rule|
|-|-|
|Group name|Use supplied value; otherwise `未知`|
|Requested range|Apply only when timestamps support it|
|Actual covered range|Derive from readable messages; do not copy the requested range blindly|
|Source|Text paste or file name/type|
|Focus|Topic, person, decision, risk, opportunity, or full analysis|
|User profile|Optional; missing fields limit only user-specific relevance|

If the user's request is clear, start the analysis. Ask only about missing information that materially changes the result, and place those questions after a useful first output.

## Supported inputs

- Direct text, TXT, Markdown: parse speaker/time patterns and preserve raw paragraphs.
- CSV: map `time/时间/发送时间/日期`, `speaker/发送人/昵称/成员`, `message/内容/消息/正文`, `message_type/类型/消息类型`, and `group/source/来源群`.
- Excel: inspect sheets and headers, then normalize rows to the message schema.
- Word or PDF: extract readable text first; retain page or paragraph source pointers when available.
- Images, voice, video, links, files: analyze only successfully extracted content. A placeholder such as `[图片]` is evidence that media existed, not evidence of its contents.

For TXT, Markdown, and CSV, `python3 scripts/normalize_chat.py --input <path> --group-name <name>` produces a deterministic JSON envelope. Run `--help` for options.

## Stable message schema

```json
{
  "message_id": "0001",
  "group_name": "群名称",
  "time": "2026-09-08 10:20",
  "speaker": "张三",
  "message_type": "text",
  "message": "今天课程内容很有启发",
  "reply_to": null,
  "source": "wechat",
  "raw_text": "原始文本"
}
```

Unknown values are `null` or `未知`; never fabricate them.

## Cleaning without losing meaning

You may suppress isolated emoji, system join/leave notices, exact duplicate forwards, irrelevant ads, and unreadable attachment placeholders from the main analysis. Keep a count in the quality note.

Do not automatically discard short replies such as “同意”, “就按这个做”, “价格可以”, “下周安排”, “我来负责”, or “有预算”. Resolve them with nearby messages. Keep repeated views from different people because repetition can indicate demand or consensus.

When consecutive messages from one speaker form one expression, analyze them together while preserving the original message pointers. When replies or pronouns cannot be resolved, state the ambiguity.

## Large inputs

1. Inventory files, groups, date coverage, message counts, and missing media.
2. Split on conversation boundaries or time windows with a small overlap; do not split a quoted/reply chain when avoidable.
3. Extract the same intermediate fields from every chunk: events, people, topics, evidence, decisions, tasks, risks, opportunities, and limitations.
4. Merge by evidence ID. Preserve disagreements, changes over time, duplicates across groups, and original provenance.
5. Report whether all chunks were processed. If not, label the output partial and identify omitted ranges.

## Multi-group analysis

Analyze each group independently before aggregation. A cross-group trend requires evidence from at least two named groups. Distinguish:

- same message forwarded to several groups;
- independent people expressing the same need;
- one person's repeated statement;
- actual change over time.

Never merge same-named speakers across groups unless identity is explicitly established.
