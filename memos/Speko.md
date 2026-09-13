# Speko

**Watch** | 68/100 | on-thesis | YC S26

> Strong technical founder with deep domain experience and live open-source infra, but faces strategic risk from the industry trend toward end-to-end native voice models.

**Why this call:** on-thesis and score 68 is 60-74. Speko is an AI infrastructure and developer tool providing a model router and evaluation API for voice agents, used by software engineering teams building AI applications, who pay for hosted routing and managed keys.

[HN launch](https://news.ycombinator.com/item?id=49332751) (118 points, 69 comments, 2026-08-17) | [website](https://speko.ai/)

15 of 16 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 22/25 | The founder spent four years as a cofounder and CTO building enterprise voice agents across multiple languages before launching Speko. |
| Shipping evidence | 20/25 | The product features a live hosted router, open-sourced gateway binary under MIT, and published multilingual benchmark boards. |
| Demand signal | 15/25 | External usage has grown 25% per week since late June, and customer anecdotes indicate early adoption, though revenue figures are not disclosed. |
| Defensibility | 11/25 | Moat relies on proprietary evaluation methodologies and benchmark test suites for spontaneous speech and naturalness, though basic routing logic can be replicated. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "Before founding Speko, I spent four years as cofounder and CTO building voice agents for enterprises across Asia in 10+ languages." ([HN post](https://news.ycombinator.com/item?id=49332751))

**Shipping evidence**

- "We also open sourced the gateway for teams who want to avoid an extra network hop... ( https://github.com/SpekoAI/gateway , MIT): one Go binary" ([HN post](https://news.ycombinator.com/item?id=49332751))
- "Every speech model, benchmarked language by language, wired into one API." ([website](https://speko.ai/))

**Demand signal**

- "Since we started the batch in late June, external usage has grown about 25 percent per week on average" ([HN post](https://news.ycombinator.com/item?id=49332751))
- "A team running thousands of calls a day told us: "we can literally go to this dashboard, switch the model, and it will do it for us."" ([HN post](https://news.ycombinator.com/item?id=49332751))

**Defensibility**

- "We trained an automatic scorer for TTS naturalness on our blind head-to-head listening votes" ([HN post](https://news.ycombinator.com/item?id=49332751))

</details>

## Team

Bek is the founder and YC S26 participant, with four years of prior experience as co-founder and CTO building voice agents for enterprises across Asia.

- "Hi HN! I'm Bek, founder of Speko, a platform that finds an optimal combination of speech-to-text" ([HN post](https://news.ycombinator.com/item?id=49332751))
- "Before founding Speko, I spent four years as cofounder and CTO building voice agents for enterprises across Asia in 10+ languages." ([HN post](https://news.ycombinator.com/item?id=49332751))

## Product

Speko is a router and evaluation platform for voice AI that dynamically selects and connects speech-to-text, LLM, and text-to-speech models via an API or open-source gateway.

- "a platform that finds an optimal combination of speech-to-text, LLM, and text-to-speech models, given your constraints" ([HN post](https://news.ycombinator.com/item?id=49332751))
- "The Router for Voice AI. Every speech model, benchmarked language by language, wired into one API." ([website](https://speko.ai/)) **(not found word for word in this source)**

## Market

**Size:** The market encompasses developers and enterprises building voice agents, with external usage growing about 25 percent per week since late June.
- "Since we started the batch in late June, external usage has grown about 25 percent per week on average" ([HN post](https://news.ycombinator.com/item?id=49332751))

**Competitors:** Livekit Gateway, Vapi, LM Arena, Artificial Analysis. Commenters noted potential overlap with LiveKit Gateway, Vapi, and existing evaluation tools like LM Arena and Artificial Analysis.
- "What is the difference with Livekit Gateway? https://livekit.com/blog/introducing-livekit-inference Or even something more managed like Vapi?" ([HN comment by MikhailTal](https://news.ycombinator.com/item?id=49332751))
- "There are many companies now with evals as a core business model: LM Arena, Artificial Analysis, Prompt foo" ([HN comment by narrationbox](https://news.ycombinator.com/item?id=49332751))

**Why now:** Rapid expansion of voice model options and frequent vendor updates make manual integration and static stacking obsolete, creating a need for automated routing.
- "Each of those layers offers a dozen credible vendors, and each month there are new models on the market. Almost everyone evaluates once, picks a stack of their choice, and never rechecks" ([HN post](https://news.ycombinator.com/item?id=49332751))

## Risks

- Industry shifts toward end-to-end trained omni-models could bypass the multi-vendor STT/LLM/TTS stack architecture.
  - "The industry is very much moving towards one-model-does-all end to end trained similar to LLMs and VLMs." ([HN comments](https://news.ycombinator.com/item?id=49332751))
- Stakeholders often make voice stack decisions only once at the project start, questioning the ongoing value of dynamic routing.
  - "stakeholders usually make this sort of decisions once at the start of the project." ([HN comments](https://news.ycombinator.com/item?id=49332751))

## What would change the call

- Evidence that end-to-end multimodal voice models completely replace multi-vendor architectures
- Data showing net retention and recurring paid contracts from production teams
- Proof that automated benchmark routing significantly outperforms static enterprise selections

## Data gaps

- Exact revenue or paying customer count
- Granular architecture details of the automated scoring engine
- Retention metrics beyond the initial 25% weekly growth claim

## Quotes that failed the source check

- product (site): "The Router for Voice AI. Every speech model, benchmarked language by language, wired into one API."

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash-lite.*
