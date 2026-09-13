# TesterArmy

**Watch** | 60/100 | on-thesis | YC P26

> **Held back by: founder depth (9/25).** The founders are named but there is no information about their technical backgrounds, prior shipped products, or domain expertise in the sources.
>
> The strongest point is the rapid adoption by 30+ daily active teams and strong testimonials from engineering leaders, while the weakest point is the high token cost of running LLM agents and the risk of customers building their own local solutions using open-source tools.

**Why this call:** on-thesis and score 60 is 60-74 (engineering software; customers pay for software). An agentic end-to-end testing platform for web and mobile apps that allows engineers to define tests in natural language and pay for test runs or subscriptions.

- "TesterArmy is an agentic testing platform that runs end-to-end checks before deployment and in production." ([HN post](https://news.ycombinator.com/item?id=48586299))

[HN launch](https://news.ycombinator.com/item?id=48586299) (132 points, 69 comments, 2026-06-18) | [website](https://tester.army)

18 of 18 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 9/25 | The founders are named but there is no information about their technical backgrounds, prior shipped products, or domain expertise in the sources. |
| Shipping evidence | 19/25 | The product is live with 30+ daily active teams, integrations with major tools, and they have open-sourced a trace explorer tool called unbox-ai. |
| Demand signal | 20/25 | They have 30+ daily active teams and numerous highly positive, named testimonials from developers, CTOs, and CEOs. |
| Defensibility | 12/25 | They offer workflow depth by handling OTPs, SSO, and captchas, but face risks of being bypassed by local LLM-based test generation or Playwright MCP. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "we’re Oskar, Szymon, and Piotr, and we’re building TesterArmy" ([HN post](https://news.ycombinator.com/item?id=48586299))

**Shipping evidence**

- "Over the past few months, we scaled from 0 to 30+ teams using our product every day." ([HN post](https://news.ycombinator.com/item?id=48586299))
- "We built unbox-ai to read our own QA agent's traces." ([website](https://tester.army))

**Demand signal**

- "Over the past few months, we scaled from 0 to 30+ teams using our product every day." ([HN post](https://news.ycombinator.com/item?id=48586299))
- "In sixteen years of building mobile apps, TesterArmy is the first tool that actually does what I always expected AI-powered testing to do." ([website](https://tester.army))

**Defensibility**

- "If I'm already using Opus to write the code, surely it would know best what E2E tests to write" ([HN comment by dbbk](https://news.ycombinator.com/item?id=48586299))
- "We tried out playwright mcp and it easily consumes 1M+ tokens for a test with ~20 steps" ([HN comment by pranshuchittora](https://news.ycombinator.com/item?id=48586299))

</details>

## Team

Founded by Oskar, Szymon, and Piotr, with no further details on their professional backgrounds or prior exits provided in the sources.

- "we’re Oskar, Szymon, and Piotr, and we’re building TesterArmy" ([HN post](https://news.ycombinator.com/item?id=48586299))

## Product

An agentic testing platform that executes end-to-end tests on web, iOS, and Android platforms using natural language inputs, integrating with CLI, GitHub, Slack, Discord, and coding agents.

- "Instead of wasting hours on manual testing or maintaining static scripts, we let you specify your tests in natural language and handle everything in between." ([HN post](https://news.ycombinator.com/item?id=48586299))
- "Test web, iOS and Android." ([website](https://tester.army))

## Market

**Size:** not found in sources

**Competitors:** Cypress, Revyl, mobileboost.io, Rainforest QA, Playwright, Momentic, Spur, QA Wolf, Mabl, BrowserStack. The company competes with traditional testing frameworks, AI-driven mobile testing tools, and established QA automation platforms.
- "We use cypress heavily for our core flows" ([HN comment by msencenb](https://news.ycombinator.com/item?id=48586299))
- "I'm curious how your mobile testing compares to https://revyl.com" ([HN comment by tcoff91](https://news.ycombinator.com/item?id=48586299))

**Why now:** AI coding tools have dramatically accelerated code generation, making testing the primary bottleneck, while LLMs now enable agentic, natural-language-driven testing.
- "AI coding tools have made it dramatically faster to write and ship code, but testing is still a bottleneck." ([HN post](https://news.ycombinator.com/item?id=48586299))

## Risks

- High token costs and pricing sustainability for running LLM agents per test run.
  - "We tried out playwright mcp and it easily consumes 1M+ tokens for a test with ~20 steps" ([HN comment by pranshuchittora](https://news.ycombinator.com/item?id=48586299))
- Security concerns and configuration overhead regarding outsourcing critical testing and potential credential leaks.
  - "But config overhead and potential security leaks makes it a no go" ([HN comment by negamax](https://news.ycombinator.com/item?id=48586299))
- Nondeterminism and stability of agentic test runs.
  - "How do you make sure results stay stable regardless of the nondeterministic nature?" ([HN comment by poisonborz](https://news.ycombinator.com/item?id=48586299))

## What would change the call

- Evidence of unsustainable unit economics due to high LLM token consumption per test run.
- A significant security breach or leak of encrypted customer credentials/OTPs.
- Customers successfully migrating back to local, deterministic LLM-generated E2E tests to save costs.

## Data gaps

- The professional and technical backgrounds of the founders Oskar, Szymon, and Piotr.
- The exact pricing structure and margins/token costs per test run.
- Quantitative benchmarks proving the reliability and accuracy of their testing agents compared to traditional E2E frameworks.

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash.*
