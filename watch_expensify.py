#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Expensify $250 bounty 抢单监控
- 轮询 Expensify/App 的 open Help Wanted 且无人认领的 issue
- 新出现 → 终端打印 + 存日志 + macOS 通知 + 自动打开浏览器
用法:
    python3 watch_expensify.py            # 前台循环运行
    python3 watch_expensify.py --once     # 只跑一轮（测试）
依赖: gh CLI 已登录 (gh auth status)
"""
import argparse, json, subprocess, sys, time, os
from datetime import datetime

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".seen.json")
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new_bounties.log")
POLL_SECONDS = 120  # GitHub API 未认证限流 10/min；gh 已认证更宽松，120s 足够

QUERY = 'repo:Expensify/App is:issue state:open label:"Help Wanted" no:assignee'

def gh_search():
    out = subprocess.run(
        ["gh", "api", "-X", "GET", "search/issues",
         "-f", f"q={QUERY}", "-f", "sort=created", "-f", "order=desc",
         "-f", "per_page=15", "--jq", ".items[] | {number, title, created_at, html_url, labels: [.labels[].name]}"],
        capture_output=True, text=True)
    if out.returncode != 0:
        print(f"[{now()}] gh api 出错: {out.stderr.strip()[:300]}", file=sys.stderr)
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
    # macOS 通知
    subprocess.run(["osascript", "-e",
        f'display notification "{msg}" with title "{title[:40]}"'], capture_output=True)
    subprocess.run(["open", url], capture_output=True)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="只跑一轮")
    ap.add_argument("--poll", type=int, default=POLL_SECONDS)
    args = ap.parse_args()

    seen = load_seen()
    print(f"[{now()}] 启动 Expensify 抢单监控 (轮询 {args.poll}s)。已跟踪 {len(seen)} 个已知 issue")
    while True:
        items = gh_search()
        print(f"[{now()}] 当前无人认领的 open Help Wanted: {len(items)} 个")
        for it in items:
            num = str(it["number"])
            if num in seen:
                continue
            seen.add(num)
            # 只对"刚发布不久"的提醒（>7 天说明大概率难做/被盯漏，仍提醒但标注）
            age_note = ""
            notify(f"[$250] Expensify #{num}", it["title"][:60], it["html_url"])
        save_seen(seen)
        if args.once:
            break
        time.sleep(args.poll)

if __name__ == "__main__":
    main()
