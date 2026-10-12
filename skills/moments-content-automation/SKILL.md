---
name: moments-content-automation
description: Use when drafting or revising a WeChat Moments post from a topic, viewpoint, source material, case, product idea, or rough draft. Focuses on audience fit, natural voice, grounded content, and copy-ready formatting.
---

# Moments Copywriting

Write WeChat Moments copy only. Default to Chinese unless the user asks for another language. Do not generate images, image prompts, visual strategies, posters, or companion assets.

## Start by choosing the audience

Decide who the post is for before choosing its angle or wording. Use this order:

1. Follow an audience the user explicitly names.
2. If the topic or supplied material clearly centers one audience, write specifically for that audience. For example, solo business ownership and personal service delivery usually point to individual OPC readers; team training, organizational processes, and business collaboration usually point to enterprise readers.
3. If there is no clear audience lean, write for a broad readership around the concrete issue they share. “Broad” must still feel relevant to a real situation; avoid vague lines aimed at everyone.
4. If the user asks to reach both enterprise and OPC readers, look for one genuine shared problem. Use that as the through-line and mention each context only where it clarifies relevance. Do not force both groups into a post when their needs diverge.
5. If the audience remains materially ambiguous and the choice would change the message, ask one concise question or suggest separate versions.

## Understand the post's job and material

Before drafting, determine:

- What one thing should the reader understand, reconsider, or do after reading?
- What situation or question makes this relevant to the chosen reader?
- What facts, actions, opinions, plans, and unknowns are actually present in the source material?

Keep one main communication task. A post may show professional value, a point of view, a useful method, a real process, a personal observation, or an invitation. Choose only what the task and material support. Do not force every post to contain a story, counterintuitive turn, case result, or call to action.

When the material is too thin for the requested claim or story, ask for the missing detail or write only what the material supports. Never invent first-person experience, customer dialogue, emotions, numbers, results, or testimonials. Mark illustrative examples as examples; do not present them as events that happened to the author. For unstable product or feature details, verify important claims when current sources are available; otherwise retain the uncertainty instead of overstating it.

## Develop the idea without a fixed formula

Let the material determine the length, order, and shape. There is no required character count, paragraph count, or opening-body-ending formula. Do not shorten a post merely to avoid structure, and do not pad it to feel substantial.

Build enough depth for the reader to follow the thought. Depending on the material, this may mean starting from a recognizable situation, explaining what is actually causing the difficulty, showing a concrete action or distinction, and ending with a useful observation. These are available moves, not mandatory steps. A concise reflection can stay concise; a complicated idea may need more explanation.

Translate abstract claims into something the reader can recognize: a task, decision, behavior, obstacle, method, or observable result. Keep examples close to the main idea. If adding an example would imply an unsupported fact, use a clearly hypothetical example or leave it out.

## Keep the voice human and specific

- Write in natural, spoken Chinese. Keep the author's own wording and point of view when they are available.
- Prefer plain, concrete language over polished slogans, business jargon, and abstract summaries.
- Avoid familiar AI-copy patterns: generic hooks such as “最近有个变化很有意思”; formulaic turns such as “真正的变化不是……而是……” when they add no meaning; repeated parallel clauses; forced “反认知”; and tidy motivational conclusions that could fit any topic.
- Do not manufacture intimacy by claiming “我最近发现 / 我一直在做” unless the user supplied that personal experience.
- Do not make every post sound like a lesson, advertisement, or conversion script. A natural ending may simply complete the thought.
- Emojis and hashtags are optional. Use them only when they fit the author's voice or the user requests them.

## Format for reading on a phone

Group sentences that belong to the same thought in one paragraph. Add natural line breaks within a paragraph to create breathing room; put a blank line between distinct thoughts. Keep related meaning together, avoid both dense text walls and fragmenting every sentence into its own paragraph. Let the copy decide how many paragraphs and line breaks it needs.

Preserve the chosen line breaks in the final output. Do not add a title, audience label, explanation, or writing notes to the copy itself.

## Output

Return one final copy-ready post by default. Put the post alone in a `social_post` writing block so the user can copy it directly. Keep analysis and any necessary factual note outside the block, and omit them when they are not needed. If the user asks for multiple versions, make each version a complete, distinct post and label them outside their copy blocks.

Do not return image concepts, image-generation prompts, or image files.

## Final check

Before returning the post, confirm:

- The audience matches the request and the source material.
- The post has one clear purpose and enough substance to develop it.
- Facts, interpretations, plans, and examples are not presented as the same thing.
- The wording sounds like a person speaking, not a reusable marketing template.
- Paragraphs keep related ideas together, with natural line breaks and blank lines between distinct thoughts.
- The output block contains only copy the user can publish.

## Style references

These examples show audience routing and voice; they are not structures to copy.

**Broad audience, no clear OPC or enterprise lean:**

> 事情一时没进展，很多人的第一反应是赶紧找办法：换个工具、改个流程，或者再多做一点。
>
> 可忙了一圈，结果还是没变。也许不是办法不够多，而是一开始就把“问题出在哪儿”想当然了。
>
> 先停一下，把问题拆小：现在具体卡在哪一步？如果解决了，什么会发生变化？
>
> 把问题问清楚，不是拖延。是先确认力气该用在哪里，再往前走。

**Enterprise and OPC share a real question:**

> 企业找讲师、顾问或服务伙伴，通常不是只想听一遍履历。做 OPC 也一样：客户更想知道的往往是，“你能帮我把什么事做好？”
>
> 企业端可能关心，这套做法能不能落进业务、让团队接着用；个人 OPC 的客户，可能更关心你能不能帮他少绕弯路，把眼前的事往前推进。场景不一样，想确认的其实相近：你能不能解决我现在的问题？

Use the first pattern only when the topic is genuinely broad. Use the second only when the source material supports a shared concern across the two audiences. For a clearly OPC-specific or enterprise-specific topic, write directly to that audience.
