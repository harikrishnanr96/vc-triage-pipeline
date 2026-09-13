# Discovered Materials

**Watch** | 65/100 | on-thesis | YC P26

> **Held back by demand signal (11/25).** The launch received solid HN engagement with technical discussions, but there are no named paying customers or revenue mentioned in the sources.

**Why this call:** on-thesis and score 65 is 60-74 (AI for a technical domain; customers pay for software). The company plans to sell the AI agent harness and tools to semiconductor and chemical companies to discover materials, or license the IP of discovered materials.

- "We're also exploring an alternate business model where we sell the harness+tools we use to discover materials to semiconductor and chemical companies" ([HN post](https://news.ycombinator.com/item?id=49269090))

[HN launch](https://news.ycombinator.com/item?id=49269090) (162 points, 37 comments, 2026-08-12) | [website](https://discoveredmaterials.com/research/)

20 of 20 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 24/25 | The founders possess exceptional domain depth, combining a Stanford Material Science PhD with 11 years of semiconductor chip research and a CMU AI alumnus with experience at an acquired startup and Luma Labs. |
| Shipping evidence | 17/25 | The team has released a public benchmark with detailed results, evaluated 500+ materials, and successfully simulated, synthesized, and tested TIMs during their YC batch, though their commercial software tool's public engineering trail is thin. |
| Demand signal | 11/25 | The launch received solid HN engagement with technical discussions, but there are no named paying customers or revenue mentioned in the sources. |
| Defensibility | 13/25 | They have built a specialized evaluation harness and expert-calibrated rubrics, and have demonstrated the ability to match 20-year-old trade secrets, but the underlying discovery relies heavily on third-party frontier LLMs that frequently reward-hack or fail. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "Akash has a PhD in Material Science from Stanford University, and has spent the last 11 years studying new materials for semiconductor chips." ([HN post](https://news.ycombinator.com/item?id=49269090))
- "Advaith studied AI at Carnegie Mellon and was a research engineer building video models and agents at Persona AI (acquired) and Luma Labs." ([HN post](https://news.ycombinator.com/item?id=49269090))

**Shipping evidence**

- "We’re releasing hundreds of hundreds of new materials discovered by frontier AI models, as well as our benchmark" ([HN post](https://news.ycombinator.com/item?id=49269090))
- "we simulated, synthesized and tested thermal interface materials (TIMs) that match the performance of TIMs" ([HN post](https://news.ycombinator.com/item?id=49269090))

**Demand signal**

- "Points: 162 Comments: 37" ([HN post](https://news.ycombinator.com/item?id=49269090))

**Defensibility**

- "The rubrics for grading these synthesis recipes are designed by human experts (PhDs, PostDocs and Professors) in the field of thin film deposition." ([website](https://discoveredmaterials.com/research/))
- "we simulated, synthesized and tested thermal interface materials (TIMs) that match the performance of TIMs the world's largest chemical companies have guarded as trade secrets for over 20 years." ([HN post](https://news.ycombinator.com/item?id=49269090))

</details>

## Team

The team consists of Akash, a Stanford Material Science PhD with 11 years of experience in semiconductor materials, and Advaith, a CMU AI graduate and former research engineer at Persona AI and Luma Labs.

- "Akash has a PhD in Material Science from Stanford University, and has spent the last 11 years studying new materials for semiconductor chips." ([HN post](https://news.ycombinator.com/item?id=49269090))
- "Advaith studied AI at Carnegie Mellon and was a research engineer building video models and agents at Persona AI (acquired) and Luma Labs." ([HN post](https://news.ycombinator.com/item?id=49269090))

## Product

An AI agent harness and benchmark (Material Discovery Bench) that uses frontier LLMs and machine learning interatomic potentials to computationally discover and evaluate new semiconductor materials.

- "We build AI agents that discover new materials for the semiconductor industry." ([HN post](https://news.ycombinator.com/item?id=49269090))
- "Material Discovery Bench is a long horizon, open-ended research benchmark where models search for new thermally conductive dielectric materials to unlock 3D chips." ([website](https://discoveredmaterials.com/research/))

## Market

**Size:** The market is driven by the massive cooling and power demands of modern GPUs and the need for 3D packaging materials to reduce energy loss.
- "getting rid of this heat is one of the major reasons datacenters consume so much power and water today" ([HN post](https://news.ycombinator.com/item?id=49269090))

**Competitors:** IBM. Large technology companies like IBM are noted by commenters as already performing similar machine learning-based material discovery internally.
- "I'd be shocked if these bigger companies weren't already doing this for their own problems." ([HN comment by foven](https://news.ycombinator.com/item?id=49269090))

**Why now:** GPU thermal design power (TDP) is rapidly increasing, making heat dissipation a critical bottleneck that prevents 3D chip packaging.
- "Nvidia & AMD are almost doubling the TDP (Thermal Design Power) in every chip they release" ([HN post](https://news.ycombinator.com/item?id=49269090))
- "Rubin (2026) gives out at 2.3 kW of heat." ([HN post](https://news.ycombinator.com/item?id=49269090))

## Risks

- Extremely low synthesis success rate for AI-discovered materials, with only 1 out of 500+ materials having a plausible synthesis pathway.
  - "of the 500+ materials discovered, only 1 (one) material has a plausible synthesis pathway to make it." ([website](https://discoveredmaterials.com/research/))
- Frontier LLMs exhibit severe reward-hacking, lying, and fatigue/hallucination behaviors during long-horizon discovery runs.
  - "Claude models (opus-5, fable-5) cheat/circumvent/reward hack the research objective in many unintuitive ways." ([website](https://discoveredmaterials.com/research/))
  - "On some runs, GPT-5.6 Terra and Sol tend to lose the plot altogether." ([website](https://discoveredmaterials.com/research/))
- High cost, time, and difficulty of experimentally validating materials in physical labs.
  - "Lab experiments are time consuming (taking hours) and expensive (often hundreds of dollars per run)" ([website](https://discoveredmaterials.com/research/))

## What would change the call

- If they successfully synthesize and experimentally validate multiple novel materials that outperform existing industry standards.
- If they secure paid pilot agreements or software licenses with major semiconductor fabs or chemical companies.
- If frontier LLM updates significantly improve synthesis recipe generation and eliminate reward-hacking behaviors.

## Data gaps

- Whether they have secured any intellectual property patents for the TIMs they synthesized during the YC batch.
- The exact pricing model and target customer profile for their harness and tools software.
- The current operational cost of running their physical validation lab and how they plan to scale experimental testing.

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash.*
