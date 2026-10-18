<div align="center">

# 💰 Expensify $250 Bounty Sniper Kit

**Real USD open-source bounty monitor** · first to see it, first to earn it

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)
![launchd](https://img.shields.io/badge/launchd-autostart-30A3DC?logo=apple&logoColor=white)

![GitHub stars](https://img.shields.io/github/stars/sudorm-rf0/expensify-bounty-watcher)
![GitHub license](https://img.shields.io/github/license/sudorm-rf0/expensify-bounty-watcher)
![GitHub last commit](https://img.shields.io/github/last-commit/sudorm-rf0/expensify-bounty-watcher)

</div>

---

> Verified on 2026-08-10. Expensify/App is currently the only open-source bounty source that **pays real USD ($250 per issue)** and updates daily.
> Harsh reality: every open Help Wanted job is usually **claimed within minutes** (86 of 86 were already claimed today).
> So the game is not "can you do it" — it is **who sees it first and who writes the better proposal**.

## 🚀 Quick start

```bash
# Run in the foreground (keep the terminal open)
python3 watch_expensify.py

# Run a single pass
python3 watch_expensify.py --once

# Run in the background (optional, see below)
nohup python3 watch_expensify.py > watcher.log 2>&1 &
```

- Polls GitHub every 120 seconds
- On a **newly posted and unclaimed** $250 issue → prints to the terminal, appends to `new_bounties.log`, fires a macOS notification, and **opens the browser automatically**
- Issues already seen are recorded in `.seen.json`, so they are never reported twice

## ⚡ What to do within 30 minutes of an alert (every second counts)

1. Open the issue, read the body, and comment **in English** to claim it and hold your place (template: `claim-comment.md`)
2. Write the **P/S proposal** from `proposal-template.md` (root cause + approach, **never paste a code diff**)
   - Note: Expensify's AI assistant MelvinBot now posts a proposal first; **your proposal must be materially different from Melvin's** to be considered (see CONTRIBUTING)
3. Wait for approval from a C+ (community reviewer) and a CME (Expensify staff) — **do not open a PR before approval** (it will be ignored or closed)
4. After approval: follow repo conventions — clone → fix → write tests → open PR → wait for merge → get paid

## 💳 Getting paid (key point for contributors in China)

- Expensify pays external contributors through **Upwork**
- Standard approach in China: register **Payoneer** (a mainland Chinese ID is enough, approved in 1-3 business days) → link Payoneer as the payout method on Upwork → withdraw to a domestic bank card
- ⚠️ Upwork carries regional-restriction risk for new accounts (mainland policy shifts over time), so **register Payoneer and confirm you can create an Upwork account before investing time in sniping bounties**

## ✅ Hard requirements (do not apply if you cannot meet them)

- A Mac is mandatory (iOS/macOS/Web/mWeb/Android must all be tested) ✅ you have one
- The repo is 2.7GB and must run locally (npm plus per-platform emulators)
- Every fix needs reproduction steps plus screenshots
- Language: communicate entirely in English
- Never test with a corporate or client account (register a test account with a test+ email)

## 📂 Files

- `watch_expensify.py` — bounty monitor (main tool)
- `claim-comment.md` — claim comment template
- `proposal-template.md` — proposal template (fill in the blanks)
- `new_bounties.log` — historical alert log

## 🛡 Background daemon (launchd) — already configured

- Actual run location: `~/expensify-bounty-watcher/` (the old "side gig" path is a symlink to it)
- Service name: `com.<user>.expensify-bounty-watcher`
- Configured for: start at login + auto-restart on crash (KeepAlive)
- Why it lives there: macOS TCC privacy protection blocks launchd from accessing `~/Documents`, so the program itself was moved to the `~` home root

Common commands:
```bash
# Check whether it is running (column 2 is the PID, column 3 is the exit code, 0 = healthy)
launchctl list | grep expensify

# Watch logs live
tail -f ~/expensify-bounty-watcher/watcher.log

# Stop
launchctl bootout gui/501/com.<user>.expensify-bounty-watcher

# Start again
launchctl load -w ~/Library/LaunchAgents/com.<user>.expensify-bounty-watcher.plist
```
