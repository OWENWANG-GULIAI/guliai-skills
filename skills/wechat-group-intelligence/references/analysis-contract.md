# Analysis Contract

Read this reference before scoring, identifying key people, interpreting relationships, or drafting findings.

## Internal analysis layers

Build analysis data before writing the report:

1. `message`: time, speaker, content, reply/quote, source pointer.
2. `meaning`: fact, viewpoint, question, need, feedback, decision, task, risk, opportunity, emotion.
3. `entities`: people, organizations, products, dates, money, action owner, deadline, deliverable.
4. `topic/event`: related messages and their change over time.
5. `scene`: four-factor score and primary/secondary selection.
6. `intelligence`: relevance, importance, business value, action value, evidence level.
7. `report`: ranked findings, people, quotes, actions, assets, and limitations.

Do not expose private chain-of-thought. Expose evidence, concise rationale, calculations when useful, and uncertainties.

## Evidence levels

|Level|Meaning|Allowed wording|
|-|-|-|
|明确事实|Direct statement or observable interaction|“聊天中明确提到……”|
|有依据推断|Several messages support a reasonable interpretation|“根据……推断，可信度中/高”|
|弱推断|One ambiguous clue or unresolved context|“可能……，需确认”|
|未知|No usable evidence|“未知 / 证据不足”|

Claims about identity, decision authority, relationship, satisfaction, outcome, purchase intent, consensus, and trend require particular care. A title such as “王总” does not prove formal role; “知道了” does not prove acceptance; “有预算” does not prove purchasing authority; silence does not prove loss of interest.

## Scene decision

Use `config/scene_rules.yaml`. Score keyword, topic, relationship, and behavior dimensions separately. Group name can support but cannot determine the result. Explain each score with observed signals.

- Primary scene: highest supported score at or above 60.
- Secondary scene: independently supported and within the configured gap; it supplements rather than replaces the primary template.
- General scene: highest score below 60, mixed-purpose chat, or insufficient scene evidence.

Do not manufacture a precise percentage from intuition. When evidence does not support a defensible numeric score, give a range or qualitative confidence and explain the limit.

## Information value

Use `config/scoring_rules.yaml`. Score 0–100 only when each dimension can be briefly justified. Otherwise use a star band with evidence notes. Keywords identify candidates; negation, speaker, context, timing, and later messages can reverse the meaning.

Core intelligence must satisfy at least two configured criteria and include a reliable source pointer. Rank by value, not chronology or message volume.

## People and relationships

A key person may be a decision-maker, demand owner, expert, executor, influencer, connector, or active contributor. Evaluate decision impact, business relevance, professional contribution, relationship position, and action involvement. Message count is descriptive, not decisive.

For every role or relationship output:

- observed behavior or quote;
- role/relationship label;
- fact or inference status;
- confidence;
- unresolved ambiguity.

Keep conflicting roles and duplicate nicknames separate. Do not infer the user's relationship to a person solely from friendliness, mention frequency, or honorifics.

## Finding unit

Every core finding uses this shape:

```markdown
### 发现：一句可判断的标题

#### 事实
What directly occurred.

#### 证据
Speaker, time/source pointer, and an exact quote or faithful excerpt.

#### 推断
Interpretation, confidence, and alternatives.

#### 对用户的影响
Why this matters under the supplied profile or stated goal.

#### 建议行动
Who should do what, when, for what expected result, with human review status.
```

Long quotes may be excerpted without changing meaning; mark them as excerpted. Conflicting evidence stays visible.

## Actions and assets

Split actions into 24 hours, 7 days, and long-term. Do not turn an idea into an assignment unless an owner accepts it. Do not turn a recommendation into an external operation.

Possible asset destinations are customer, content, knowledge, case, product-feedback, and project/task systems. For each proposed asset include source evidence, suggested title/type, reuse value, privacy treatment, and next human decision.
