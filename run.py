"""Run the whole pipeline with one command.

    python run.py                      replay the committed run from cache (no API key needed)
    python run.py --topic "voice AI"   search Launch HN posts on a topic and write memos to runs/<topic>/
    python run.py --refresh            fetch the Launch HN list again instead of reusing the cached one

A run reuses its cached Launch HN list when one exists, for topics too, so rerunning
the same command gives the same companies and needs no new Gemini calls.

Stages, each a plain script that reads the previous stage's output:
    fetch_hn -> source -> enrich -> analyze -> memo
"""

import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "topic"


def run_stage(script, env):
    print("\n=== {} ===".format(script), flush=True)
    result = subprocess.run([sys.executable, "-u", "-W", "ignore", os.path.join("src", script)],
                            cwd=ROOT, env=env)
    if result.returncode != 0:
        sys.exit("\nStopped: {} failed (exit code {}). Later stages were not run.".format(
            script, result.returncode))


def main():
    parser = argparse.ArgumentParser(description="VC triage pipeline: Launch HN -> memos.")
    parser.add_argument("--topic", help='topic to search Launch HN posts for, e.g. "voice AI"')
    parser.add_argument("--days", type=int, help="how far back to search (default 365 with a topic, 90 without)")
    parser.add_argument("--top", type=int, default=10, help="how many candidates to analyse (default 10)")
    parser.add_argument("--refresh", action="store_true",
                        help="fetch the Launch HN list again instead of reusing the cached one")
    args = parser.parse_args()

    env = dict(os.environ)
    env["TOP_N"] = str(args.top)
    if args.days:
        env["DAYS"] = str(args.days)

    run_dir = os.path.join("runs", slug(args.topic)) if args.topic else "."
    if args.topic:
        env["TOPIC"] = args.topic
    env["RUN_DIR"] = run_dir

    # Launch HN search only covers a rolling window, so fetching again returns a
    # different set of companies. Reusing the cached list keeps a run reproducible;
    # --refresh or a new --days window fetches again.
    cached_list = os.path.join(ROOT, run_dir, "cache", "hn_raw.json")
    if args.refresh or args.days or not os.path.exists(cached_list):
        run_stage("fetch_hn.py", env)
    else:
        print("Reusing the cached Launch HN list in {} (pass --refresh to fetch again).".format(
            os.path.relpath(cached_list, ROOT)))
    run_stage("source.py", env)
    with open(os.path.join(ROOT, run_dir, "data", "candidates.jsonl"), encoding="utf-8") as handle:
        if not any(line.strip() for line in handle):
            print("\nNo candidates matched, so there is nothing to analyse. No memos were written.")
            return
    for script in ("enrich.py", "analyze.py", "memo.py"):
        run_stage(script, env)

    print("\nDone. Start with {}".format(os.path.join(run_dir, "memos", "README.md")))


if __name__ == "__main__":
    main()
