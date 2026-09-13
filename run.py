"""Run the whole pipeline with one command.

    python run.py                      replay the committed run from cache (no API key needed)
    python run.py --topic "voice AI"   fetch Launch HN posts on a topic and write memos to runs/<topic>/
    python run.py --refresh            refetch the default Launch HN list instead of using the cached one

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
                        help="refetch the default Launch HN list instead of replaying the cached one")
    args = parser.parse_args()

    env = dict(os.environ)
    env["TOP_N"] = str(args.top)
    if args.days:
        env["DAYS"] = str(args.days)

    if args.topic:
        run_dir = os.path.join("runs", slug(args.topic))
        env["TOPIC"] = args.topic
        fetch = True
    else:
        run_dir = "."
        # Launch HN search only covers a rolling window, so a refetch returns a
        # different set of companies. Replaying the cached list keeps the
        # committed results reproducible.
        fetch = args.refresh
        if not fetch and not os.path.exists(os.path.join(ROOT, "cache", "hn_raw.json")):
            print("No cached Launch HN list found, fetching a fresh one.")
            fetch = True
    env["RUN_DIR"] = run_dir

    if fetch:
        run_stage("fetch_hn.py", env)
    for script in ("source.py", "enrich.py", "analyze.py", "memo.py"):
        run_stage(script, env)

    print("\nDone. Start with {}".format(os.path.join(run_dir, "memos", "README.md")))


if __name__ == "__main__":
    main()
