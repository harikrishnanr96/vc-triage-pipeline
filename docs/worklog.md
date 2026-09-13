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



## Sun Sep 13

- Correction to last night's entry: not everything worked first try. The first Launch HN query matched "launch" anywhere, so only 8 of 50 results were real Launch HN posts. Claude caught it and restricted the search to exact phrase in titles. enrich.py also crashed on a failed GitHub lookup, which only showed up when Claude fed it bad URLs on purpose.
- analyze.py is written but hasn't run for real, since I don't have a Gemini key set up yet. Claude tested the retry and cache logic with a fake model. Next: record my own verdicts on the 10 before running it.



- Free tier only allows 5 calls a minute, so 9 of 10 failed. Switched to gemini-3.5-flash-lite and put a 13s gap between calls. All 10 ran in ~2 min.
-  The prompt never says what's in or out of thesis, and the verdict isn't tied to the score. Committing this as the baseline before I fix it.

- Didn't write down my own verdicts before running it, so I've got nothing to check the model against.

# evening
- Discovered Materials: on-thesis. Their core is the AI agent harness and the benchmark they published, which counts as AI infra even though they sell into materials science.

- Adam: on-thesis. Dev tools covers tools for any kind of enginees, not only software developers, and they ship in public (open-source repo, 5k+ GitHub stars)

## memo stage
- Worked on the memo generation stage of pipeline. few issues found like verdicts are changing with prompt versions. There is no take meeting observed
Proven metal creates circuit boards and still is on thesis. I think gemini sees free plugins for software engineers and gets confused.


- I observed that Flash lite kept on calling Proven Metal "software" even while quoting the per orfer margin. Tested with 3.5 Flash and 3.8 Flash and worked for other tricky companies.

