# Bullet

**Pass** | 48/100 | on-thesis | YC S26

> **Held back by defensibility (6/25).** The product is a closed-source harness/wrapper around existing LLMs, which commenters note is easy to replicate, clone, or replace with custom prompts and open-source alternatives.

**Why this call:** on-thesis but score 48 < 60 (engineering software; no revenue model stated yet). Bullet is a fast coding agent for software developers, currently offered for free with no clear monetization model mentioned.

- "Free to use. No subscriptions. Just a faster way to ship." ([website](https://www.codewithbullet.com))
- "A Faster Coding Agent" ([HN post](https://news.ycombinator.com/item?id=49283063))

[HN launch](https://news.ycombinator.com/item?id=49283063) (121 points, 89 comments, 2026-08-13) | [website](https://www.codewithbullet.com)

26 of 26 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 13/25 | The founders have technical backgrounds from AppLovin and Citadel, but they are fresh out of college (dorm room startup) and have pivoted six times without prior exits or deep domain depth in AI research. |
| Shipping evidence | 15/25 | The product is live with macOS, Linux, and Windows builds, a CLI, and published SWE-bench results, but the code is closed-source and there is no public GitHub repository. |
| Demand signal | 14/25 | Solid HN engagement with some active users praising the speed, but many commenters are highly skeptical of the benchmark validity and the value of a proprietary harness. |
| Defensibility | 6/25 | The product is a closed-source harness/wrapper around existing LLMs, which commenters note is easy to replicate, clone, or replace with custom prompts and open-source alternatives. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "Bullet started in a senior year dorm. We were fresh out of working at AppLovin and Citadel" ([HN post](https://news.ycombinator.com/item?id=49283063))

**Shipping evidence**

- "DOWNLOAD FOR MAC 1.4.17" ([website](https://www.codewithbullet.com))
- "npm install -g @trybullet/cli" ([website](https://www.codewithbullet.com))

**Demand signal**

- "I recently switched over to using primarily Bullet for my projects and the speed of it makes it very nice" ([HN comment by lucasdimarco](https://news.ycombinator.com/item?id=49283063))
- "I think this adds no value. I would stick to OpenCode." ([HN comment by esafak](https://news.ycombinator.com/item?id=49283063))

**Defensibility**

- "Proprietary software is no longer a moat" ([HN comment by lrvick](https://news.ycombinator.com/item?id=49283063))
- "nobody would use it because they’d just point their own AI at it and clone it. It’s just not that hard." ([HN comment by lowbloodsugar](https://news.ycombinator.com/item?id=49283063))

</details>

## Team

Founded by Adi and Alex, who started the company in their senior year dorm after working at AppLovin and Citadel.

- "We’re Adi and Alex, founders of Bullet, a faster coding agent." ([HN post](https://news.ycombinator.com/item?id=49283063))
- "Bullet started in a senior year dorm. We were fresh out of working at AppLovin and Citadel" ([HN post](https://news.ycombinator.com/item?id=49283063))

## Product

A fast coding agent and harness that optimizes speed by reducing round trips, parallelizing independent tool calls, routing models, and performing targeted code search.

- "Bullet routes, searches, and executes with one purpose: keeping up with you." ([website](https://www.codewithbullet.com))
- "On SWE-bench Verified, Bullet resolved 479/500 (95.8%) in one attempt, averaging 119s per task" ([HN post](https://news.ycombinator.com/item?id=49283063))

## Market

**Size:** not found in sources

**Competitors:** Claude Code, Codex, OpenCode, maki.sh, pellmell.ai, mini-SWE-agent. Competes with existing coding agents and harnesses like Claude Code, Codex, OpenCode, maki.sh, and pellmell.ai.
- "Let’s take on Claude Code and Codex, we can do it!" ([HN post](https://news.ycombinator.com/item?id=49283063))
- "I guess I can fund raise just by having built https://maki.sh" ([HN comment by tontinton](https://news.ycombinator.com/item?id=49283063))

**Why now:** Developers are increasingly frustrated by the slow execution speeds and high costs of existing coding agents.
- "We were spending hours waiting for coding agents like Claude Code and Codex, and got so frustrated" ([HN post](https://news.ycombinator.com/item?id=49283063))
- "At our company, we were burning hours waiting on agent runs." ([website](https://www.codewithbullet.com))

## Risks

- History of frequent pivots (six pivots before this product) which may indicate a lack of long-term focus.
  - "Bullet started as an AI hedge fund, a browser-use agent, synthetic financial data (oof), a mobile IDE, and a bunch of other things." ([HN post](https://news.ycombinator.com/item?id=49283063))
  - "Is there another pivot coming? This would make me nervous." ([HN comment by throw03172019](https://news.ycombinator.com/item?id=49283063))
- Security and trust issues due to closed-source distribution requiring root access.
  - "Installing a .deb requires root. Okay, a coding agent that wants root access." ([HN comment by lrvick](https://news.ycombinator.com/item?id=49283063))
  - "Proprietary software is no longer a moat, and for something like this it just makes your software very hard to trust." ([HN comment by lrvick](https://news.ycombinator.com/item?id=49283063))
- Low defensibility as a harness that can be easily replicated or built via prompting.
  - "I'm genuinely confused about what is mechanically different in this harness that could not be accomplished with a prompt/skill in another harness." ([HN comment by yetanotherjosh](https://news.ycombinator.com/item?id=49283063))
  - "nobody would use it because they’d just point their own AI at it and clone it. It’s just not that hard." ([HN comment by lowbloodsugar](https://news.ycombinator.com/item?id=49283063))

## What would change the call

- Evidence of paying enterprise customers willing to pay for a proprietary agent harness.
- A detailed technical breakdown proving their parallel execution and context hygiene cannot be easily replicated via prompting in open-source harnesses.
- Open-sourcing the core agent loop to resolve developer trust and security concerns while maintaining a monetization strategy.

## Data gaps

- No information on how the company plans to generate revenue or monetize the product.
- No details on the exact model providers supported or how API costs are handled.
- No public GitHub repository or source code to verify security and implementation details.

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash.*
