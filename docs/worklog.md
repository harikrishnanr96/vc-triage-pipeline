## Sat Sep 12,evening

Thesis: seed-stage AI infra and dev tools with technical founders shipping in public. For this category the engineering trail is a
better early signal than the pitch, because the buyers are engineers.

Source: HN via the Algolia API. Free, no auth, and points/comments
give me a traction signal without extra work. Skipping Product Hunt
(OAuth), Crunchbase (paid), YC directory (JS-rendered).

Open question: does Show HN give me real companies or mostly weekend
projects? Checking before I build on top of it.

LLM: Gemini free tier so the reviewer can run this.


## Sat Sep 12 , night

**Decided**

I checked with show HN first it showed mostly weekend projects, not companies. then switched the query to launch HackerNews instead (YC only) 34 results - real companies. 


Sorted the companies by points and 4 were off thesis. Keeping them so that there are some companies to reject


When checking I found that a third of the Launc HN posts are text-only . Url points back at HN thread . This thread text is richer so decided to keep it.

Founders aren't in the candidate records yet. Deferred to the analysis
stage - the founders introduce themselves in the first paragraph of
every Launch HN post, so it comes free when I fetch the thread text.

Claude Code wrote both scripts from a single prompt each, worked first
try. My changes were to the query params after seeing the Show HN
output was junk. Prompt saved in docs/sessions/01-fetch-hn.md.