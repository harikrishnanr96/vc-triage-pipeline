# Context.dev

**Watch** | 72/100 | on-thesis | YC S26

> Strong founder background with rapid shipping and named customers, countered by extreme competition in a crowded web scraping commodity market.

**Why this call:** on-thesis and score 72 is 60-74. Context.dev is an AI infrastructure and developer tool providing an API for web scraping and data extraction used by software engineers and AI agents, paying via metered API subscription plans.

[HN launch](https://news.ycombinator.com/item?id=48847562) (119 points, 86 comments, 2026-07-09) | [website](https://www.context.dev)

18 of 18 supporting quotes were found word for word in the sources.

## Scores

| | Score | Why |
|---|---|---|
| Founder depth | 22/25 | Founder has deep technical experience, having worked at Amazon/Sunrun, successfully co-founded and exited two startups (StockAlarm.io, essense.io), and previously shipped Brand.dev. |
| Shipping evidence | 22/25 | Fully functional live product with public docs, SDKs across multiple languages, a self-serve dashboard, and active pricing tiers. |
| Demand signal | 20/25 | Strong HN engagement with 119 points, active early adopters, and named production customers like Mintlify, SiteGPT, and Sourcely. |
| Defensibility | 8/25 | Operates in a highly crowded web-scraping and API abstraction space with numerous named competitors, open-source alternatives, and basic proxy capabilities. |

<details><summary>Quotes behind the scores</summary>

**Founder depth**

- "Before, I worked at Amazon and Sunrun, and co-founded StockAlarm.io & essense.io, both of which were acquired." ([HN post](https://news.ycombinator.com/item?id=48847562))

**Shipping evidence**

- "Since it’s an API, here are the docs: https://docs.context.dev/quickstart ." ([HN post](https://news.ycombinator.com/item?id=48847562))
- "We provide official SDKs for TypeScript, Python, Ruby, Go, and PHP." ([website](https://www.context.dev))

**Demand signal**

- "SiteGPT, the AI chatbot platform for customer support, switched from Firecrawl to Context.dev to scrape entire websites" ([website](https://www.context.dev))
- "Points: 119 Comments: 86" ([HN post](https://news.ycombinator.com/item?id=48847562))

**Defensibility**

- "How did you find your differentiation in a highly commoditized space? It's probably one of the most crowded spaces." ([HN comment by jackienotchan](https://news.ycombinator.com/item?id=48847562))

</details>

## Team

Yahia, a solo founder with prior experience at Amazon and Sunrun, co-founded StockAlarm.io and essense.io (both acquired), built knifegeek.io, and previously built Brand.dev before expanding into Context.dev.

- "Before, I worked at Amazon and Sunrun, and co-founded StockAlarm.io & essense.io, both of which were acquired." ([HN post](https://news.ycombinator.com/item?id=48847562))
- "Just before Context.dev, I built Brand.dev. The idea was that your software product should automatically know about your customer" ([HN post](https://news.ycombinator.com/item?id=48847562))

## Product

Context.dev is an API providing web data extraction, rendering clean markdown, screenshots, brand data, and structured extraction via JSON schema for software applications and AI agents.

- "Hi Hacker News, I’m Yahia. I built Context.dev ( https://www.context.dev/ ) to make it really easy to integrate web data into your products and agents." ([HN post](https://news.ycombinator.com/item?id=48847562))
- "You can send us a URL and get back clean Markdown, rendered HTML, screenshots, extracted images, etc.." ([HN post](https://news.ycombinator.com/item?id=48847562))

## Market

**Size:** The market encompasses developers building AI agents, chatbots, and onboarding workflows requiring live web context and company enrichment data, with enterprise plans handling high-volume traffic exceeding 2M credits per month.
- "Talk to sales if you need high-volume pricing beyond 2M credits/month, custom rate limits, SSO / SAML, SCIM provisioning, an uptime SLA" ([HN comments](https://news.ycombinator.com/item?id=48847562))
- "One API, every piece of web context your agent needs." ([website](https://www.context.dev))

**Competitors:** Firecrawl, BrowserUse, Browserbase, CloudCruise, NotteLabs, Intuned, Expand.ai, Reworkd, Parallel, Exa, Cloudflare, Zyte, Tavily, Intercept. Named competitors in the crowded web scraping and retrieval space include Firecrawl, BrowserUse, Browserbase, CloudCruise, NotteLabs, Intuned, Expand.ai, Reworkd, Parallel, Exa, Cloudflare, Zyte, Tavily, and Intercept.
- "Unclear what difference exists against Firecrawl - their team has been shipping great features extremely quickly lately" ([HN comment by m_w_](https://news.ycombinator.com/item?id=48847562))
- "- Firecrawl - BrowserUse - Browserbase - CloudCruise - NotteLabs - Intuned - Expand.ai - Reworkd" ([HN comment by jackienotchan](https://news.ycombinator.com/item?id=48847562))

**Why now:** AI agents and LLM applications require real-time web context, structured extraction, and fresh retrieval augmented generation (RAG) data rather than static model cutoffs.
- "Agents need clean/current context from the web, and this is the best way I’ve found to give it to them." ([HN comment by modo_](https://news.ycombinator.com/item?id=48847562))
- "Feeding agents knowledge frozen at the model's cutoff" ([website](https://www.context.dev))

## Risks

- Extremely crowded and commoditized market with many direct competitors and well-funded alternatives.
  - "How did you find your differentiation in a highly commoditized space? It's probably one of the most crowded spaces." ([HN comment by jackienotchan](https://news.ycombinator.com/item?id=48847562))
- Website blocking, scraping restrictions, and friction around crawling infrastructure without robust rotating residential proxies.
  - "Seems wildly expensive, furthermore not a single mention of "ip" on homepage? Not using rotating ip's, residential proxies? AKA unusable for high value data." ([HN comment by seper8](https://news.ycombinator.com/item?id=48847562))

## What would change the call

- Demonstrating proprietary proxy or extraction infrastructure that outperforms standard headless browser clusters sustainably.
- Proving net-negative churn and rapid ARR growth from high-volume enterprise contracts.
- Significant defensibility via unique data assets that cannot be replicated by open-source scrapers or model providers.

## Data gaps

- Exact current ARR or paying user count metrics.
- GitHub repository metrics and open-source contributions.
- Detailed breakdown of margin per scrape operation.

---

*Generated by src/memo.py from data/analyses.jsonl. Analysis model: gemini-3.5-flash-lite.*
