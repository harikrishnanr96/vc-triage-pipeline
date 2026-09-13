# Context.dev

**Take a meeting** | 81/100 | on-thesis | YC S26

> The strongest point is the founder's proven track record of shipping and exits combined with immediate, high-quality customer adoption from named startups; the weakest point is the intense competition and low technical defensibility in a highly commoditized web scraping market.

**Why this call:** on-thesis and score 81 >= 75 (ai infrastructure, customers pay for software). Context.dev provides a web scraping and brand data API that delivers structured data, markdown, and brand intelligence to developers and AI agents on a subscription or usage-based credit model.

- "Context.dev offers Developer ($25/mo), Pro ($149/mo), and Scale ($499/mo), plus Enterprise for teams that need more than 2M credits a month" ([website](https://www.context.dev))

[HN launch](https://news.ycombinator.com/item?id=48847562) (119 points, 86 comments, 2026-07-09) | [website](https://www.context.dev)

23 of 23 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 23/25 | Yahia is a solo founder with a strong technical background at Amazon and Sunrun, and a proven track record of building and successfully exiting two startups (StockAlarm.io and essense.io). |
| Shipping evidence | 24/25 | The product is fully live with comprehensive documentation, multiple official SDKs, and active paying users who have integrated the API into production. |
| Demand signal | 23/25 | Strong demand signal with multiple named, high-profile startup customers (Mintlify, SiteGPT, daily.dev, DocsBot, Tinfoil) actively using the product and migrating from competitors. |
| Defensibility | 11/25 | While the workflow integrations (JSON schema extraction, brand profiles) add value, the core technology relies on web scraping, which is highly commoditized and faces numerous direct competitors. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "Before, I worked at Amazon and Sunrun, and co-founded StockAlarm.io & essense.io, both of which were acquired." ([HN post](https://news.ycombinator.com/item?id=48847562))

**Shipping evidence**

- "Since it’s an API, here are the docs: https://docs.context.dev/quickstart ." ([HN post](https://news.ycombinator.com/item?id=48847562))
- "We provide official SDKs for TypeScript, Python, Ruby, Go, and PHP." ([website](https://www.context.dev))

**Demand signal**

- "SiteGPT, the AI chatbot platform for customer support, switched from Firecrawl to Context.dev" ([website](https://www.context.dev))
- "We used Zyte before, but switched to Context.dev due to the ZDR offering" ([website](https://www.context.dev))

**Defensibility**

- "How did you find your differentiation in a highly commoditized space? It's probably one of the most crowded spaces." ([HN comment by jackienotchan](https://news.ycombinator.com/item?id=48847562))

</details>

## Team

The company is led by solo founder Yahia, a former Amazon and Sunrun engineer who previously co-founded two acquired startups, StockAlarm.io and essense.io.

- "Hi Hacker News, I’m Yahia." ([HN post](https://news.ycombinator.com/item?id=48847562))
- "Before, I worked at Amazon and Sunrun, and co-founded StockAlarm.io & essense.io, both of which were acquired." ([HN post](https://news.ycombinator.com/item?id=48847562))

## Product

Context.dev is an API that scrapes websites, crawls sitemaps, extracts structured data via JSON Schema, and retrieves brand assets like logos, colors, and fonts.

- "You can send us a URL and get back clean Markdown, rendered HTML, screenshots, extracted images, etc.." ([HN post](https://news.ycombinator.com/item?id=48847562))
- "For more custom use cases, you can send a URL plus a JSON Schema and ask us to extract structured data" ([HN post](https://news.ycombinator.com/item?id=48847562))

## Market

**Size:** The market is driven by the transition of the web to become legible to AI agents, requiring clean, real-time context rather than frozen training data.
- "Agents need clean/current context from the web, and this is the best way I’ve found to give it to them." ([HN comment by modo_](https://news.ycombinator.com/item?id=48847562))
- "The internet is clearly moving in this direction: companies are starting to realize their sites need to be legible to agents." ([HN comment by modo_](https://news.ycombinator.com/item?id=48847562))

**Competitors:** Firecrawl, BrowserUse, Browserbase, CloudCruise, NotteLabs, Intuned, Expand.ai, Reworkd, Parallel, Exa, Cloudflare, Tavily, Zyte, Crawl4AI. The web scraping and retrieval space is highly crowded, featuring well-funded players, other YC startups, and self-hosted alternatives.
- "Even within YC, there are many competitors that do pretty much the same thing: - Firecrawl - BrowserUse - Browserbase - CloudCruise" ([HN comment by jackienotchan](https://news.ycombinator.com/item?id=48847562))
- "And then you have the extremely well-funded web retrieval players like Parallel and Exa." ([HN comment by jackienotchan](https://news.ycombinator.com/item?id=48847562))

**Why now:** AI agents and LLMs require real-time web context to avoid knowledge cutoff limitations, but building and maintaining custom scraping infrastructure internally is highly inefficient.
- "Feeding agents knowledge frozen at the model's cutoff" ([website](https://www.context.dev))
- "Building crawlers, scrapers, and pipelines internally" ([website](https://www.context.dev))

## Risks

- Intense competition and commoditization in the web scraping and retrieval market, making differentiation difficult.
  - "How did you find your differentiation in a highly commoditized space? It's probably one of the most crowded spaces." ([HN comment by jackienotchan](https://news.ycombinator.com/item?id=48847562))
- Backlash and blocking from website owners due to the negative side effects of AI crawlers, such as costs and downtime.
  - "AI crawlers come with negative side effects for website owners (costs, downtime, etc.), as repeatedly reported here on HN" ([HN comment by jackienotchan](https://news.ycombinator.com/item?id=48847562))
- Simple client-side workarounds using open-source libraries can replicate a significant portion of the product's core scraping value.
  - "If you want to vibe something that gets you 70% of the way to this well funded startup in like 15 minutes" ([HN comment by SOLAR_FIELDS](https://news.ycombinator.com/item?id=48847562))

## What would change the call

- If major competitors like Firecrawl or Exa aggressively cut prices, rendering Context.dev's pricing uncompetitive.
- If website anti-bot protections (like Cloudflare Turnstile) become so advanced that Context.dev's bypass rates drop significantly, causing high failure rates.
- If legal or regulatory crackdowns on AI web scraping make it impossible to scrape public websites without explicit opt-in.

## Data gaps

- No GitHub repository stats or public code repository links were provided to evaluate the open-source traction or code quality.
- No exact revenue figures, MRR, or growth rates are disclosed in the sources.
- No details on the exact infrastructure or proxy network used to bypass advanced bot protections (e.g., whether they use residential proxies).

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash.*
