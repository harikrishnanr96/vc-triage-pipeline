# Adam

**Pass** | 53/100 | on-thesis | YC W25

> **Held back by founder depth (5/25).** The sources only mention one founder, Zach, with no details about his technical background, prior shipped products, or domain depth.

**Why this call:** on-thesis but score 53 < 60 (engineering software; no revenue model stated yet). An open-source AI-powered Text-to-CAD platform that generates parametric 3D models from natural language, though how the company plans to generate revenue is not specified in the sources.

- "We’re building CADAM, an open source Text to CAD platform." ([HN post](https://news.ycombinator.com/item?id=48572553))
- "We're building AI agents for mechanical CAD software." ([HN post](https://news.ycombinator.com/item?id=48572553))

[HN launch](https://news.ycombinator.com/item?id=48572553) (215 points, 97 comments, 2026-06-17) | [website](https://github.com/Adam-CAD/CADAM) | [GitHub](https://github.com/Adam-CAD/CADAM) (5134 stars, last commit 2026-09-02)

27 of 27 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 5/25 | The sources only mention one founder, Zach, with no details about his technical background, prior shipped products, or domain depth. |
| Shipping evidence | 23/25 | The product is live, open-source, runs fully in-browser, has a public GitHub repository with over 5,000 stars, and has a recent commit from September 2026. |
| Demand signal | 15/25 | There is strong engagement on Hacker News (215 points, 97 comments) and some users report successful real-world usage (e.g., printing custom bumpers), though professional engineers express heavy skepticism about its accuracy and utility. |
| Defensibility | 10/25 | The project is open-source (GPL licensed) and relies on third-party LLMs via Vercel AI SDK, though they are building custom workflows like in-browser WebAssembly compilation of OpenSCAD and plan to add UI for face/edge selection. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "I'm Zach from Adam" ([HN post](https://news.ycombinator.com/item?id=48572553))

**Shipping evidence**

- "Try it: https://adam.new/cadam/" ([HN post](https://news.ycombinator.com/item?id=48572553))
- "Stars: 5134" ([GitHub](https://github.com/Adam-CAD/CADAM))

**Demand signal**

- "Points: 215" ([HN post](https://news.ycombinator.com/item?id=48572553))
- "Comments: 97" ([HN post](https://news.ycombinator.com/item?id=48572553))

**Defensibility**

- "We’re building CADAM, an open source Text to CAD platform." ([HN post](https://news.ycombinator.com/item?id=48572553))
- "Model-agnostic via the Vercel AI SDK" ([HN post](https://news.ycombinator.com/item?id=48572553))

</details>

## Team

The team includes Zach, but further details about the founders' backgrounds, technical depth, or other team members are not found in the sources.

- "I'm Zach from Adam" ([HN post](https://news.ycombinator.com/item?id=48572553))

## Product

CADAM is an open-source React app with a Supabase backend that compiles OpenSCAD to WebAssembly to run fully in-browser, generating parametric 3D models from text prompts and image references.

- "We’re building CADAM, an open source Text to CAD platform. It's a React app (TanStack Start) with a Supabase backend" ([HN post](https://news.ycombinator.com/item?id=48572553))
- "Generates parametric 3D models from natural language, with support for both text prompts and image references." ([HN post](https://news.ycombinator.com/item?id=48572553))

## Market

**Size:** not found in sources

**Competitors:** CADEM, tooltrace.ai, modelrift.com, Claude Code, CadQuery, quidities.com. Competitors and alternative tools mentioned by commenters include CADEM, tooltrace.ai, modelrift.com, Claude Code with CadQuery, and quidities.com.
- "FYI there is already a product with a very similar name, CADEM." ([HN comment by zardo](https://news.ycombinator.com/item?id=48572553))
- "I’ve also had a good experience with Claude Code and CadQuery" ([HN comment by fxtentacle](https://news.ycombinator.com/item?id=48572553))

**Why now:** The rise of newer LLMs with adaptive thinking and better code-generation capabilities, such as Gemini 3.1 Pro, enables more effective text-to-CAD generation.
- "Model-agnostic via the Vercel AI SDK: Anthropic (Claude), Google (Gemini), and OpenAI/others through OpenRouter, with adaptive thinking auto-enabled on newer models." ([HN post](https://news.ycombinator.com/item?id=48572553))

## Risks

- LLMs currently have poor spatial awareness and reasoning, leading to technically inaccurate models that lack precision, correct tolerances, or proper assembly features.
  - "I find all current LLMs to have pretty poor spatial awareness." ([HN comment by murkt](https://news.ycombinator.com/item?id=48572553))
  - "the resulting models may be visually close to what is required, but they are not technically accurate." ([HN comment by dmpanch](https://news.ycombinator.com/item?id=48572553))
- Professional engineers are highly skeptical of AI for mechanical design, noting that CAD modeling is only a small fraction of engineering work and that verifying AI-generated models can take longer than manual creation.
  - "There are so many reasons why I, as an engineer, will never even attempt to use AI for mechanical design" ([HN comment by incorene2](https://news.ycombinator.com/item?id=48572553))
  - "Even if all I need is a simple little bracket or something, I can model that and know it's right much quicker than I can ask the AI to do it" ([HN comment by incorene2](https://news.ycombinator.com/item?id=48572553))
- The choice of OpenSCAD as the primary CAD paradigm is criticized by some users as being a 'joke' or less powerful than alternatives like CadQuery or FreeCAD.
  - "And besides all of that, and with love....OpenSCAD is a joke" ([HN comment by incorene2](https://news.ycombinator.com/item?id=48572553))
  - "why did you choose OpenSCAD instead of more powerful alternatives like CadQuery?" ([HN comment by c7b](https://news.ycombinator.com/item?id=48572553))

## What would change the call

- Evidence of successful integration and accurate exports to professional CAD software like Fusion, Solidworks, or Onshape without losing constraints.
- Release of the planned face/edge selection UI and viewport image integration that demonstrably improves LLM spatial context and accuracy.
- A clear monetization strategy or revenue traction from the commercial product (adam.new) or plugins.

## Data gaps

- No information on the founders' professional backgrounds, technical expertise, or prior achievements.
- No details on the commercial business model, pricing, or current revenue/paying customers.
- No information on the team size or other contributors beyond Zach.

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash.*
