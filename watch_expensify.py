#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expensify $250 bounty sniper monitor
- Polls Expensify/App for open "Help Wanted" issues with no assignee
- On a new one -> print to terminal + write log + macOS notification + open the browser
Usage:
    python3 watch_expensify.py            # run in a foreground loop
    python3 watch_expensify.py --once     # run a single pass (for testing)
Requires: gh CLI logged in (gh auth status)
"""
import argparse, json, subprocess, sys, time, os
from datetime import datetime

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".seen.json")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new_bounties.log")
POLL_SECONDS = 120  # unauthenticated GitHub API is rate-limited to 10/min; authenticated gh is more lenient, 120s is enough

QUERY = 'repo:Expensify/App is:issue state:open label:"Help Wanted" no:assignee'

def gh_search():
    out = subprocess.run(
        ["gh", "api", "-X", "GET", "search/issues",
         "-f", f"q={QUERY}", "-f", "sort=created", "-f", "order=desc",
         "-f", "per_page=15", "--jq", ".items[] | {number, title, created_at, html_url, labels: [.labels[].name]}"],
        capture_output=True, text=True)
    if out.returncode != 0:
        print(f"[{now()}] gh api error: {out.stderr.strip()[:300]}", file=sys.stderr)
        return []
    items = [json.loads(line) for line in out.stdout.strip().splitlines() if line.strip()]
    return items

def load_seen():
    try:
        with open(STATE_FILE) as f:
            return set(json.load(f))
    except Exception:
        return set()

def save_seen(seen):
    with open(STATE_FILE, "w") as f:
        json.dump(sorted(seen), f)

def notify(title, msg, url):
    print(f"[{now()}] 🔔 NEW: {title}\n    {url}", flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{now()}] {title} | {url}\n")
    # macOS notification
    subprocess.run(["osascript", "-e",
        f'display notification "{msg}" with title "{title[:40]}"'], capture_output=True)
    subprocess.run(["open", url], capture_output=True)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="run a single pass")
    ap.add_argument("--poll", type=int, default=POLL_SECONDS)
    args = ap.parse_args()

    seen = load_seen()
    print(f"[{now()}] Expensify bounty monitor started (polling every {args.poll}s). Tracking {len(seen)} known issue(s)")
    while True:
        items = gh_search()
        print(f"[{now()}] Unclaimed open Help Wanted issues right now: {len(items)}")
        for it in items:
            num = str(it["number"])
            if num in seen:
                continue
            seen.add(num)
            # Alert only for "recently posted" ones (>7 days usually means it is hard or already watched, still alert but flagged)
            age_note = ""
            notify(f"[$250] Expensify #{num}", it["title"][:60], it["html_url"])
        save_seen(seen)
        if args.once:
            break
        time.sleep(args.poll)

if __name__ == "__main__":
    main()
