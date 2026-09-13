# Adam

**Watch** | 70/100 | on-thesis | YC W25

> Strong public shipping trail and developer engagement, offset by deep skepticism from professional engineers regarding spatial reasoning and text-to-code CAD paradigms.

**Why this call:** on-thesis and score 70 is 60-74. CADAM is an AI-powered developer and engineering tool used by technical designers to generate mechanical CAD code, offered as open-source software.

[HN launch](https://news.ycombinator.com/item?id=48572553) (215 points, 97 comments, 2026-06-17) | [website](https://github.com/Adam-CAD/CADAM) | [GitHub](https://github.com/Adam-CAD/CADAM) (5134 stars, last commit 2026-09-02)

23 of 23 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 15/25 | Founder is technical and backed by YC W25 with a working open-source shipping product, though deep domain background details are light in the text. |
| Shipping evidence | 25/25 | Extensive public code, GitHub repository with over 5,000 stars, live demo links, and local runnable code. |
| Demand signal | 20/25 | High Hacker News engagement with 215 points and 97 comments, plus thousands of GitHub stars and users reporting successful prints. |
| Defensibility | 10/25 | Open-source codebase wrapping OpenSCAD via Vercel AI SDK and WebAssembly, leading to questions from users regarding moats and ease of replication. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "Hey HN! I'm Zach from Adam ( https://adam.new/ ). We're building AI agents for mechanical CAD software." ([HN post](https://news.ycombinator.com/item?id=48572553))
- "YC batch: W25" ([HN post](https://news.ycombinator.com/item?id=48572553))

**Shipping evidence**

- "Try it: https://adam.new/cadam/" ([HN post](https://news.ycombinator.com/item?id=48572553))
- "Repository: Adam-CAD/CADAM" ([GitHub](https://github.com/Adam-CAD/CADAM))

**Demand signal**

- "Points: 215 Comments: 97" ([HN post](https://news.ycombinator.com/item?id=48572553))
- "Saw this and after 5 minutes of prompting I have four custom bumpers printing. This is a great product." ([HN comments](https://news.ycombinator.com/item?id=48572553))

**Defensibility**

- "Model-agnostic via the Vercel AI SDK: Anthropic (Claude), Google (Gemini), and OpenAI/others through OpenRouter" ([HN post](https://news.ycombinator.com/item?id=48572553))
- "How do you differentiate from other open source AI CAD solutions? I’ve also had a good experience with Claude Code and CadQuery... I.e. what’s your moat?" ([HN comments](https://news.ycombinator.com/item?id=48572553))

</details>

## Team

The team is led by founder Zach from YC W25, building Adam as an open-source AI CAD platform.

- "Hey HN! I'm Zach from Adam ( https://adam.new/ ). We're building AI agents for mechanical CAD software." ([HN post](https://news.ycombinator.com/item?id=48572553))
- "YC batch: W25" ([HN post](https://news.ycombinator.com/item?id=48572553))

## Product

CADAM is an open-source Text to CAD platform that generates parametric 3D models and textured meshes from natural language and images using OpenSCAD compiled to WebAssembly.

- "We’re building CADAM, an open source Text to CAD platform." ([HN post](https://news.ycombinator.com/item?id=48572553))
- "Outputs OpenSCAD code with automatically extracted parameters that surface as interactive sliders for instant dimension tweaking" ([HN post](https://news.ycombinator.com/item?id=48572553))

## Market

**Size:** Targeting mechanical design and 3D modeling users who utilize CAD software for prototyping and manufacturing parts.
- "AI will be the primary medium for creating mechanical designs just like it is in software today." ([HN post](https://news.ycombinator.com/item?id=48572553))

**Competitors:** TinkerCAD, CADEM, tooltrace.ai, quidities.com, ModelRift. Commenters noted alternatives in the text-to-CAD and AI design space including TinkerCAD, CADEM, tooltrace.ai, quidities.com, and ModelRift.
- "Think of it like AI TinkerCAD." ([HN post](https://news.ycombinator.com/item?id=48572553))
- "FYI there is already a product with a very similar name, CADEM." ([HN comment by zardo](https://news.ycombinator.com/item?id=48572553))

**Why now:** Advancements in LLM code generation and in-browser WebAssembly compilation enable real-time text-to-CAD rendering and interactive parameter tweaking.
- "Runs fully in-browser by compiling OpenSCAD to WebAssembly (in a Web Worker, so the UI never blocks) and rendering with Three.js" ([HN post](https://news.ycombinator.com/item?id=48572553))

## Risks

- LLMs lack reliable spatial reasoning and mechanical awareness, leading to inaccurate models.
  - "LLMs are still weak at spatial reasoning, but it gets better." ([HN comments](https://news.ycombinator.com/item?id=48572553))
  - "the resulting models may be visually close to what is required, but they are not technically accurate." ([HN comments](https://news.ycombinator.com/item?id=48572553))
- Scepticism from professional engineers regarding the utility of OpenSCAD and text-based generation for real manufacturing workflows.
  - "Even if all I need is a simple little bracket or something, I can model that and know it's right much quicker than I can ask the AI" ([HN comments](https://news.ycombinator.com/item?id=48572553))
  - "OpenSCAD is a joke, and if you seriously try to tell me that 'the best paradigm for CAD generation is to generate CAD as code', I cannot take you seriously." ([HN comments](https://news.ycombinator.com/item?id=48572553))

## What would change the call

- Demonstrable adoption by professional mechanical engineers for production-grade manufacturing assemblies.
- Transition to geometry kernels or constraint-driven modeling like CadQuery/build123d solving spatial inaccuracies.
- Evidence of sustainable commercial revenue or enterprise adoption of the paid adam.new product.

## Data gaps

- Details on revenue, team size, and commercial traction of the adam.new product.
- Comprehensive benchmarks comparing OpenSCAD output accuracy against traditional CAD tools.

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash-lite.*
