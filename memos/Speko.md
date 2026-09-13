# Speko

**Watch** | 72/100 | on-thesis | YC S26

> **Held back by: defensibility (13/25).** While they have built a custom TTS naturalness scorer and aggregate valuable multi-language benchmarks, routing layers are vulnerable to competition from larger platforms like OpenRouter or direct integrations.
>
> The strongest point is the founder's deep domain expertise and rapid shipping of a highly practical multi-model routing tool; the weakest point is the existential risk that the industry shifts to end-to-end or local voice models, rendering three-tier routing obsolete.

**Why this call:** on-thesis and score 72 is 60-74 (AI infrastructure; customers pay for software). Speko provides a hosted router and open-source gateway that benchmarks and routes voice AI models, charging for the hosted router and managed keys.

- "we charge for the hosted router and managed keys with consolidated billing." ([HN post](https://news.ycombinator.com/item?id=49332751))

[HN launch](https://news.ycombinator.com/item?id=49332751) (118 points, 69 comments, 2026-08-17) | [website](https://speko.ai/)

15 of 15 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 22/25 | The founder has four years of direct domain experience as a CTO building enterprise voice agents in multiple languages. |
| Shipping evidence | 21/25 | The company has a live hosted router, public benchmarks, and an open-source gateway repository on GitHub. |
| Demand signal | 16/25 | The startup reports strong weekly usage growth and has engaged users, though some commenters express skepticism about the longevity of the three-model architecture. |
| Defensibility | 13/25 | While they have built a custom TTS naturalness scorer and aggregate valuable multi-language benchmarks, routing layers are vulnerable to competition from larger platforms like OpenRouter or direct integrations. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "Before founding Speko, I spent four years as cofounder and CTO building voice agents for enterprises across Asia in 10+ languages." ([HN post](https://news.ycombinator.com/item?id=49332751))

**Shipping evidence**

- "We also open sourced the gateway for teams who want to avoid an extra network hop on the audio path" ([HN post](https://news.ycombinator.com/item?id=49332751))
- "A hosted, provider-neutral STT, LLM and TTS data plane at router.speko.dev" ([website](https://speko.ai/))

**Demand signal**

- "Since we started the batch in late June, external usage has grown about 25 percent per week on average" ([HN post](https://news.ycombinator.com/item?id=49332751))

**Defensibility**

- "We trained an automatic scorer for TTS naturalness on our blind head-to-head listening votes" ([HN post](https://news.ycombinator.com/item?id=49332751))

</details>

## Team

The founder, Bek, has deep technical and domain expertise, having spent four years as a co-founder and CTO building voice agents for enterprises.

- "Before founding Speko, I spent four years as cofounder and CTO building voice agents for enterprises across Asia in 10+ languages." ([HN post](https://news.ycombinator.com/item?id=49332751))

## Product

Speko offers a hosted, provider-neutral routing data plane and an open-source gateway sidecar that optimizes STT, LLM, and TTS model combinations based on latency, cost, and accuracy constraints.

- "A hosted, provider-neutral STT, LLM and TTS data plane at router.speko.dev, with typed contracts and managed routing." ([website](https://speko.ai/))
- "We also open sourced the gateway for teams who want to avoid an extra network hop on the audio path" ([HN post](https://news.ycombinator.com/item?id=49332751))

## Market

**Size:** not found in sources

**Competitors:** Livekit Gateway, Vapi, OpenRouter, LM Arena, Artificial Analysis, Prompt foo. Commenters identify several competitors in the voice gateway, routing, and evaluation space, including Livekit, Vapi, OpenRouter, and various evaluation platforms.
- "What is the difference with Livekit Gateway? https://livekit.com/blog/introducing-livekit-inference Or even something more managed like Vapi?" ([HN comment by MikhailTal](https://news.ycombinator.com/item?id=49332751))
- "why isn't openrouter gonna be the openrouter for voice ?" ([HN comment by alexcnwy](https://news.ycombinator.com/item?id=49332751))

**Why now:** The rapid release of new speech models makes manual benchmarking and switching difficult, creating a need for automated routing and evaluation.
- "Each of those layers offers a dozen credible vendors, and each month there are new models on the market." ([HN post](https://news.ycombinator.com/item?id=49332751))

## Risks

- The industry is shifting toward end-to-end single-model voice architectures, which would eliminate the need for multi-model routing.
  - "The industry is very much moving towards one-model-does-all end to end trained similar to LLMs and VLMs." ([HN comment by narrationbox](https://news.ycombinator.com/item?id=49332751))
- Future voice processing may shift entirely to local, on-device models, bypassing cloud-based routing services.
  - "hard to image a world where TTS and STT will not be done locally in the future" ([HN comment by cjjuice](https://news.ycombinator.com/item?id=49332751))

## What would change the call

- Widespread adoption of end-to-end voice models (like OpenAI's advanced voice) that perform better and cheaper than any routed ensemble.
- OpenRouter or Livekit natively launching comprehensive voice routing and benchmarking, commoditizing Speko's core offering.
- A decline in the 25% weekly growth rate as early adopters realize they prefer to lock in a single provider rather than dynamically route.

## Data gaps

- No GitHub repository statistics (stars, forks, commit history) are available in the sources.
- No explicit details on current revenue or the exact number of paying customers.
- No information on the size of the team beyond the single founder, Bek.

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash.*
