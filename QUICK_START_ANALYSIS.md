# Quick Start: Using LLM Analysis on Test Page

## 🚀 What's New

After running a graph on the test page, you now get **automatic AI-powered security analysis** powered by your team's LLM API.

## ⚡ Quick Setup (5 minutes)

### 1. Add Your LLM API Credentials

Create `/backend/.env` file:

```bash
TEAM_ID=your_team_id_here
API_TOKEN=your_api_token_here
```

> **Tip**: Get these from your team's LLM API portal

### 2. Start Both Servers

```bash
# Terminal 1 - API Server
cd api
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd client
npm run dev
```

### 3. Run a Graph and See Analysis

1. Open http://localhost:3000/test
2. Upload any file to enter demo mode
3. Click **Execute** button
4. Wait for execution to complete
5. **Analysis panel opens automatically!** 🎉

## 📊 What You Get

After each execution, you'll see:

### Risk Score (0-100)
- **0-24**: 🟢 Low Risk
- **25-49**: 🟡 Medium Risk  
- **50-74**: 🟠 High Risk
- **75-100**: 🔴 Critical Risk

### Analysis Sections
- **Summary**: Quick overview of execution
- **Vulnerabilities**: Specific security issues found
- **Security Issues**: Broader concerns
- **Recommendations**: Actionable fixes
- **Detailed Analysis**: Comprehensive review (expandable)

## 🎯 Usage Examples

### After Execution
Analysis panel automatically appears with AI insights about your graph execution.

### View Analysis Anytime
Click the **"View Analysis"** button in the top right corner (appears after first execution).

### Regenerate Analysis
Click **"Regenerate Analysis"** button at the bottom of the panel to get fresh insights.

## 🔍 What's Analyzed

The AI reviews:
- ✅ Graph structure and flow
- ✅ Each node's execution and output
- ✅ Error messages and failures
- ✅ Final execution state
- ✅ Security vulnerabilities
- ✅ Prompt injection attempts
- ✅ Data leakage risks

## 💡 Tips

### For Best Results
- Include descriptive node names in your graph
- Run complete executions (don't interrupt)
- Check analysis after each significant change

### Understanding Risk Scores
- Based on execution behavior, not just graph structure
- Higher scores indicate more security concerns
- Consider recommendations to reduce risk

### Saving Analysis
- Each analysis has a unique ID
- Analysis is cached in memory during session
- Export feature coming soon!

## 🐛 Troubleshooting

### "Missing graph ID or execution ID"
**Fix**: Make sure graph executes successfully first

### "Failed to generate analysis"
**Check**:
1. Is TEAM_ID and API_TOKEN set in `/backend/.env`?
2. Is the API server running?
3. Check backend logs for errors

### Analysis panel doesn't open
**Try**:
1. Check browser console for errors
2. Manually click "View Analysis" button
3. Refresh page and re-run execution

### Want to test without LLM API?
The mock mode will work without credentials, but you won't get analysis. Set up credentials to use the full feature.

## 📝 Example Analysis Output

```
Risk Score: 35/100 - Medium

Summary:
The graph executed successfully with 3 nodes. The supervisor coordinated 
between research and writing agents. No critical security issues detected.

Vulnerabilities:
• Potential data exposure in error messages

Security Issues:
• Unvalidated user input passed directly to LLM
• No rate limiting on API calls

Recommendations:
• Implement input sanitization for all user prompts
• Add rate limiting middleware
• Use structured error messages
```

## 🎓 Learn More

- **Full Documentation**: See `ANALYSIS_INTEGRATION.md`
- **LLM Setup**: See `backend/LLM_API_MIGRATION.md`
- **Attack Mode**: Also has analysis! Check `/attack` page

## ✨ Feature Summary

| Feature | Test Page | Attack Page |
|---------|-----------|-------------|
| Auto Analysis | ✅ Yes | ✅ Yes |
| Risk Score | ✅ Yes | ✅ Yes |
| Vulnerabilities | ✅ Yes | ✅ Yes |
| Recommendations | ✅ Yes | ✅ Yes |
| "View Analysis" Button | ✅ Yes | ✅ Yes |

Both pages now have identical analysis capabilities!

---

**Ready to try it?** Just run a graph on the test page! 🚀

