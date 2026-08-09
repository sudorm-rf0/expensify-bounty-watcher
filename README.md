# Expensify $250 赏金抢单作战包

> 实测日期：2026-08-10。Expensify/App 是当前唯一**真实发美元（$250/单）**、每天更新的开源赏金源。
> 残酷现实：全部 open 的 Help Wanted job 通常**几分钟内就被认领**（今天 86 个全部已认领）。
> 所以核心不是"会做"，而是**比谁先看到 + 比谁 proposal 更好**。

## 1. 快速开始

```bash
# 前台跑（保持终端开着）
python3 watch_expensify.py

# 测试一轮
python3 watch_expensify.py --once

# 后台跑（可选，见下方说明）
nohup python3 watch_expensify.py > watcher.log 2>&1 &
```

- 每 120 秒轮询一次 GitHub
- 发现「新发布 + 无人认领」的 $250 issue → 终端打印 + 写 `new_bounties.log` + macOS 通知 + **自动打开浏览器**
- 已见过的 issue 记录在 `.seen.json`，不会重复提醒

## 2. 收到提醒后 30 分钟内要做的事（争分夺秒）

1. 打开 issue，读完正文，**用英文**评论，表明要接并抢位（模板见 `claim-comment.md`）
2. 按 `proposal-template.md` 写 **P/S proposal**（root cause + 方案，**严禁贴代码 diff**）
   - 注意：Expensify 现在有 AI 助手 MelvinBot 会先发一个 proposal；**你必须给出"与 Melvin 有实质不同"的方案**才会被考虑（详见 CONTRIBUTING）
3. 等 C+（社区审阅人）和 CME（官方）批准 proposal —— **没批准前禁止开 PR**（开了会被无视/关闭）
4. 批准后：按仓库规范 clone → 修 → 写测试 → 开 PR → 等 merge → 收款

## 3. 收款通道（国内用户关键点）

- Expensify 通过 **Upwork** 支付给外部贡献者
- 国内标准做法：注册 **Payoneer**（中国大陆身份证即可，1-3 个工作日审批）→ 在 Upwork 绑定 Payoneer 收款 → 提现到国内银行卡
- ⚠️ Upwork 对新注册用户有地区限制风险（大陆政策时松时紧），**建议先注册 Payoneer 并确认 Upwork 能注册成功，再投入时间抢单**

## 4. 硬性要求（做不到就别接）

- 必须有 Mac（要测 iOS/macOS/Web/mWeb/Android 全平台）✅ 你有
- 仓库 2.7GB，本地要能跑起来（npm + 各平台模拟器）
- 每次修复要提供测试步骤 + 截图
- 语言：全英文沟通
- 不要用企业/客户账号测试（用 test+ 邮箱注册测试号）

## 5. 文件清单

- `watch_expensify.py` — 抢单监控（主工具）
- `claim-comment.md` — 抢位评论模板
- `proposal-template.md` — proposal 模板（照抄填空）
- `new_bounties.log` — 历史提醒记录

## 6. 后台守护（launchd）——已配置好

- 实际运行位置：`~/expensify-bounty-watcher/`（原"外快"路径是指向这里的软链接）
- 服务名：`com.<user>.expensify-bounty-watcher`
- 已设置为：开机自启 + 崩溃自动重启（KeepAlive）
- 为什么放这里：macOS TCC 隐私保护不允许 launchd 访问 `~/Documents`，所以程序本体移到 `~` 根目录

常用命令：
```bash
# 查看是否在跑（第2列是 PID，第3列是退出码，0=正常）
launchctl list | grep expensify

# 看实时日志
tail -f ~/expensify-bounty-watcher/watcher.log

# 停止
launchctl bootout gui/501/com.<user>.expensify-bounty-watcher

# 重新启动
launchctl load -w ~/Library/LaunchAgents/com.<user>.expensify-bounty-watcher.plist
```
