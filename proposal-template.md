# Expensify Proposal 模板（照抄这个结构，用英文）

```
## Proposal

### What is the root cause of that problem?
<写清楚根因。要能证明你读懂了代码路径，而不是猜。>

### What changes do you think we should make in order to solve the problem?
<写方案思路。可以贴伪代码/小片段，但【严禁贴大段代码 diff】。>

### What alternative solutions did you explore? (Optional)
<可选。列出你考虑过的其他方案和取舍。>
```

## 红线（审阅人会直接拒掉）

1. 没有根因分析 → 拒
2. 贴大段代码 diff → 拒
3. 跳过必答问题 → 拒
4. 与 MelvinBot 方案雷同、没有实质差异 → 基本不会被选
5. **没被 hire 就开 PR** → 直接无视/关闭

## 抢到后的 PR 描述要求（后续用）

- 链接对应 issue
- 测试步骤 + 各平台截图
- 勾选 Reviewer checklist
- 一次 PR 只修一个问题
