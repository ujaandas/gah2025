# Visual Guide: LLM Analysis on Test Page

## 🎨 What You'll See

### Before Execution

```
┌─────────────────────────────────────────────────────────┐
│  Test Page                           [Execute] ────┐    │
│                                                     │    │
│  ┌───────────────────────────────────────────┐     │    │
│  │                                           │     │    │
│  │         Your Graph Canvas                 │     │    │
│  │                                           │     │    │
│  │    [Node 1] ──→ [Node 2] ──→ [Node 3]   │     │    │
│  │                                           │     │    │
│  └───────────────────────────────────────────┘     │    │
│                                                     │    │
│  [Logs Panel]                                      │    │
│                                                     │    │
└─────────────────────────────────────────────────────────┘
```

### During Execution

```
┌─────────────────────────────────────────────────────────┐
│  Test Page                      [Running...] ─────┐     │
│                                            ⏳     │     │
│  ┌───────────────────────────────────────────┐     │    │
│  │                                           │     │    │
│  │         Your Graph Canvas                 │     │    │
│  │                                           │     │    │
│  │    🟦Node 1  ──→ [Node 2] ──→ [Node 3]   │     │    │
│  │    (executing)                            │     │    │
│  └───────────────────────────────────────────┘     │    │
│                                                     │    │
│  [Logs Panel]                                      │    │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━     │    │
│  🚀 GRAPH EXECUTION STARTED                        │    │
│  ┌─ Layer 1 ────────────────────                  │    │
│  │  ▶️  Running: Node 1                           │    │
│                                                     │    │
└─────────────────────────────────────────────────────────┘
```

### After Execution - Analysis Opens Automatically! 🎉

```
┌──────────────────────────┬──────────────────────────────┐
│  Test Page               │  🤖 AI Security Analysis     │
│              [Execute]   │                              │
│   [View Analysis] ──────┤                              │
│         👆 NEW!          │  📊 Risk Assessment          │
│                          │  ┌────────────────────────┐  │
│  ┌─────────────────┐     │  │ Risk Score: 35/100    │  │
│  │                 │     │  │ [████████░░░░░░░]     │  │
│  │  Your Graph     │     │  │ Medium Risk           │  │
│  │  (completed)    │     │  └────────────────────────┘  │
│  │                 │     │                              │
│  │  ✅Node 1       │     │  📝 Summary                  │
│  │  ✅Node 2       │     │  The graph executed success- │
│  │  ✅Node 3       │     │  fully with no critical...   │
│  │                 │     │                              │
│  └─────────────────┘     │  ⚠️ Vulnerabilities (2)      │
│                          │  • Unvalidated user input    │
│  [Logs Panel]            │  • Potential data exposure   │
│  ✅ Execution Complete   │                              │
│  ✅ AI Analysis: 35/100  │  💡 Recommendations (3)      │
│                          │  • Add input sanitization    │
│                          │  • Implement rate limiting   │
│                          │  ...                         │
│                          │                              │
│                          │  [Regenerate Analysis]       │
│                          │            [Close X]         │
└──────────────────────────┴──────────────────────────────┘
```

## 🎬 Step-by-Step Walkthrough

### Step 1: Start Your Session
```
Navigate to: http://localhost:3000/test

You see:
┌────────────────────────────────────┐
│  Upload an Agent                   │
│  ┌──────────────────────────────┐  │
│  │  Drag & drop your agent file │  │
│  │  or click to browse          │  │
│  └──────────────────────────────┘  │
│                                    │
│  [Unlock Graph Editor]             │
└────────────────────────────────────┘
```

### Step 2: Upload File
```
After uploading:
┌────────────────────────────────────┐
│  📄 my-agent.py                    │
│  ┌──────────────────────────────┐  │
│  │  ✓ my-agent.py    [ready]   │  │
│  └──────────────────────────────┘  │
│                                    │
│  [Unlock Graph Editor] ←── Click! │
└────────────────────────────────────┘
```

### Step 3: Graph Loads
```
Graph Editor appears with your graph:

     [Execute] ← Click to run!

  ┌─────────────────────────────┐
  │  __start__                  │
  │      ↓                       │
  │  [supervisor]               │
  │      ↓                       │
  │  [agent_1]  [agent_2]      │
  │      ↓                       │
  │  __end__                    │
  └─────────────────────────────┘
```

### Step 4: Execution Begins
```
Top Bar changes:
  [Running...] ⏳  ← Button disabled

Logs show:
  🚀 GRAPH EXECUTION STARTED
  ┌─ Layer 1 ──────────
  │  ▶️  Running: __start__
  │  ✓ __start__ • 45ms
  └─────────────────────

Nodes light up in blue as they execute
```

### Step 5: Execution Completes
```
Top Bar shows:
  [Execute]  [View Analysis] ← NEW!
                    ✨

Logs show:
  ✅ GRAPH EXECUTION COMPLETED
  ⏱️  Total Time: 2345ms
  ━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 6: Analysis Panel Appears! 🎉
```
Slides in from right side automatically:

┌─────────────────────────────────┐
│ 🤖 AI Security Analysis         │
│─────────────────────────────────│
│                                 │
│ 📊 Risk Assessment              │
│ ┌─────────────────────────────┐ │
│ │ Risk Score: 35/100          │ │
│ │ [████████░░░░░░░░░░]        │ │
│ │ Medium                      │ │
│ └─────────────────────────────┘ │
│                                 │
│ 📝 Summary                      │
│ The graph executed successfully │
│ with 3 nodes. The supervisor   │
│ coordinated between agents.     │
│                                 │
│ ⚠️ Vulnerabilities (2)          │
│ • Unvalidated user input        │
│ • Potential data exposure       │
│                                 │
│ 🛡️ Security Issues (1)          │
│ • No rate limiting              │
│                                 │
│ 💡 Recommendations (3)          │
│ ✓ Add input sanitization        │
│ ✓ Implement rate limiting       │
│ ✓ Use structured errors         │
│                                 │
│ 📄 Detailed Analysis ▼          │
│ (click to expand)               │
│                                 │
│ [Regenerate Analysis]           │
└─────────────────────────────────┘
```

## 🎨 Color Guide

### Risk Scores

```
Low Risk (0-24):
┌────────────────────┐
│ Score: 15/100      │
│ [███░░░░░░░░░░]    │  ← Green
│ Low                │
└────────────────────┘

Medium Risk (25-49):
┌────────────────────┐
│ Score: 35/100      │
│ [████████░░░░░]    │  ← Yellow
│ Medium             │
└────────────────────┘

High Risk (50-74):
┌────────────────────┐
│ Score: 65/100      │
│ [████████████░░]   │  ← Orange
│ High               │
└────────────────────┘

Critical Risk (75-100):
┌────────────────────┐
│ Score: 85/100      │
│ [█████████████████]│  ← Red
│ Critical           │
└────────────────────┘
```

### Node States During Execution

```
Normal:      [Node Name]
Executing:   🟦 [Node Name]  ← Blue pulsing
Completed:   ✅ [Node Name]  ← Green
Error:       ❌ [Node Name]  ← Red (if failed)
```

### Analysis Sections

```
📊 Risk Assessment     (Blue/Purple gradient header)
📝 Summary            (Gray background)
⚠️ Vulnerabilities     (Red background)
🛡️ Security Issues     (Orange background)
💡 Recommendations    (Green background)
📄 Detailed Analysis  (Gray, collapsible)
```

## 🖱️ Interactive Elements

### Buttons You Can Click

```
Top Bar:
  [Execute]         ← Run the graph
  [View Analysis]   ← Reopen analysis panel

Analysis Panel:
  [Close X]              ← Top right corner
  [Detailed Analysis ▼]  ← Expand/collapse
  [Regenerate Analysis]  ← Get fresh insights
```

### What Opens When

```
Automatically:
✅ Analysis panel after execution completes

Manually:
✅ Analysis panel via "View Analysis" button
✅ Detailed analysis via expand button
✅ Node data panel via clicking nodes
✅ Logs panel via toggle button
```

## 📱 Responsive Design

### Desktop (Wide Screen)
```
┌────────────────┬─────────────────┐
│                │                 │
│   Graph        │   Analysis      │
│   Canvas       │   Panel         │
│                │                 │
└────────────────┴─────────────────┘
```

### Tablet/Small Desktop
```
┌────────────────────────────────┐
│        Graph Canvas            │
│                                │
└────────────────────────────────┘
                   ↓ Swipes over
┌────────────────────────────────┐
│    Analysis Panel (Full)       │
│                                │
└────────────────────────────────┘
```

## 🎓 Pro Tips

### Quick Actions
```
Keyboard:
  ESC              → Close analysis panel
  Backspace/Delete → Delete selected node

Mouse:
  Click node       → View node data
  Click background → Deselect
  Drag node        → Move/connect
```

### Getting Best Analysis
```
✅ DO:
- Run complete executions
- Use descriptive node names
- Check analysis after changes

❌ DON'T:
- Interrupt execution midway
- Skip reading recommendations
- Ignore high risk scores
```

## 📊 Reading the Analysis

### Risk Score Interpretation

```
0-24:  🟢 Safe to deploy
       Minor issues, if any

25-49: 🟡 Review before deploy
       Some concerns to address

50-74: 🟠 Needs attention
       Significant security issues

75-100: 🔴 DO NOT DEPLOY
        Critical vulnerabilities
```

### Priority Order

```
1. 🔴 Vulnerabilities    ← Fix FIRST
2. 🟠 Security Issues    ← Address SOON
3. 🟡 Recommendations    ← Implement when possible
```

## 🎯 Example Sessions

### Clean Execution
```
Graph runs → All green → Low risk (15) → 
"No critical issues detected" ✅
```

### Issues Found
```
Graph runs → Warning logs → Medium risk (55) → 
"2 vulnerabilities detected" ⚠️ → 
Review recommendations → Fix issues → 
Re-run → Improved score (25) ✅
```

### Critical Issues
```
Graph runs → Errors → High risk (85) → 
"Critical: prompt injection successful" 🔴 → 
STOP → Review detailed analysis → 
Implement all recommendations → 
Re-test thoroughly
```

## 🎉 Success Indicators

You know it's working when you see:

✅ "View Analysis" button appears after execution
✅ Analysis panel slides in automatically
✅ Risk score displays with colored bar
✅ Sections show vulnerabilities/recommendations
✅ Log panel shows "AI Analysis complete" message

---

**Now you're ready!** Just run a graph and watch the magic happen! ✨

