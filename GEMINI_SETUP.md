# 🟠 Google Gemini Setup Guide

## Quick Start with Gemini API

### Why Use Gemini?
- **🆓 Free Tier** - 60 requests per minute with gemini-1.5-flash (no credit card required!)
- **⚡ Fast** - Quick response times for code analysis
- **🎯 Accurate** - Google's latest multimodal AI with excellent code understanding
- **💰 Cost-Effective** - Lower pricing than OpenAI for production use

---

## 📋 Step-by-Step Setup

### 1. Get Your Gemini API Key

1. Visit **[Google AI Studio](https://makersuite.google.com/app/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key (starts with `AIza...`)

> **💡 Tip:** The API key is free to generate and comes with a generous free tier!

### 2. Configure the Application

#### Option A: Using Environment File (Recommended)

1. Edit your `.env` file:
```bash
# Choose provider
API_PROVIDER=gemini

# Add your Gemini API key
GEMINI_API_KEY=AIza-your-actual-api-key-here

# Select model (optional)
AI_MODEL=gemini-1.5-pro
```

2. Save and restart the application

#### Option B: Using the UI

1. Start the application: `streamlit run app.py`
2. In the sidebar, select **"Google Gemini"** from the AI Provider dropdown
3. Paste your API key in the text field
4. Select your preferred model (gemini-1.5-pro recommended)

---

## 🤖 Available Gemini Models

### gemini-1.5-pro (Recommended)
- **Best for:** Comprehensive analysis, detailed recommendations
- **Context:** 1 million token context window
- **Speed:** Moderate
- **Free Tier:** 2 requests per minute
- **Pricing:** $1.25 per 1M tokens (input), $5 per 1M tokens (output)

### gemini-1.5-flash (Fastest)
- **Best for:** Quick analysis, batch processing, development
- **Context:** 1 million token context window  
- **Speed:** Very fast
- **Free Tier:** 60 requests per minute ⚡
- **Pricing:** $0.075 per 1M tokens (input), $0.30 per 1M tokens (output)

### gemini-pro (Legacy)
- **Best for:** Backward compatibility
- **Context:** 30K tokens
- **Speed:** Moderate
- **Note:** Consider upgrading to 1.5 models for better performance

> **💡 Recommendation:** Start with `gemini-1.5-flash` for fast development, switch to `gemini-1.5-pro` for production.

---

## 🔄 Switching Between Providers

You can easily switch between OpenAI and Gemini:

### Method 1: Environment Variable
```bash
# In .env file
API_PROVIDER=gemini  # or "openai"
```

### Method 2: Sidebar UI
Simply select your preferred provider from the dropdown - no restart needed!

---

## 📊 Comparison: OpenAI vs Gemini

| Feature | OpenAI GPT-4o | Google Gemini 1.5 Pro |
|---------|--------------|----------------------|
| **Free Tier** | ❌ No | ✅ Yes (2 req/min) |
| **Context Window** | 128K tokens | 1M tokens |
| **Speed** | Fast | Fast |
| **Code Quality** | Excellent | Excellent |
| **Pricing** | $5/$15 per 1M tokens | $1.25/$5 per 1M tokens |
| **Best For** | Enterprise, critical | Development, cost-saving |

---

## 🎯 Usage Examples

### Example 1: Quick Analysis with Gemini Flash
```bash
# .env configuration
API_PROVIDER=gemini
GEMINI_API_KEY=AIza...
AI_MODEL=gemini-1.5-flash
```

Perfect for:
- Rapid iteration during development
- Batch analysis of multiple files
- Quick code checks

### Example 2: Comprehensive Analysis with Gemini Pro
```bash
# .env configuration
API_PROVIDER=gemini
GEMINI_API_KEY=AIza...
AI_MODEL=gemini-1.5-pro
```

Perfect for:
- Production code reviews
- Security-critical analysis
- Detailed recommendations

### Example 3: Switching from OpenAI (Quota Exceeded)
If you hit OpenAI quota limits:
1. Get Gemini API key from [makersuite.google.com](https://makersuite.google.com/app/apikey)
2. Change sidebar to "Google Gemini"
3. Paste your key
4. Continue analyzing! 🚀

---

## ⚠️ Troubleshooting

### Error: "Module 'google.generativeai' not found"
**Solution:**
```bash
pip install google-generativeai>=0.3.0
# or
pip install -r requirements.txt
```

### Error: "API key not valid"
**Solution:**
1. Verify your API key at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Check for extra spaces or quotes in `.env` file
3. Ensure key starts with `AIza`

### Error: "Resource exhausted"
**Solution:**
- You've exceeded the free tier rate limit
- Wait 1 minute and try again
- Consider upgrading to paid tier
- Switch to a different model (e.g., gemini-1.5-flash has higher limits)

### Slow responses with Gemini Pro 1.5
**Solution:**
- Switch to `gemini-1.5-flash` for faster results
- Gemini Flash is 3-5x faster than Pro while maintaining quality

---

## 📈 Free Tier Limits

### Gemini 1.5 Flash (Free)
- **Rate Limit:** 60 requests per minute
- **Daily Limit:** 1,500 requests per day
- **Perfect for:** Individual developers, small projects

### Gemini 1.5 Pro (Free)
- **Rate Limit:** 2 requests per minute
- **Daily Limit:** 50 requests per day
- **Perfect for:** Occasional analysis, testing

> **💡 Tip:** The free tier is more than enough for most development workflows!

---

## 🚀 Best Practices

### 1. Model Selection Strategy
```
Development → gemini-1.5-flash (fast, free)
Production  → gemini-1.5-pro (quality, accuracy)
Testing     → gemini-1.5-flash (high rate limits)
```

### 2. Cost Optimization
- Use Gemini Flash for batch analysis (saves 15-20x on costs)
- Reserve GPT-4o/Gemini Pro for critical reviews
- Take advantage of Gemini's free tier for development

### 3. Performance Tips
- Gemini 1.5 Flash: Best for files < 1000 lines
- Gemini 1.5 Pro: Best for complex code with many dependencies
- Both models handle 1M token context (very large files)

---

## 🔗 Useful Links

- **Get API Key:** [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- **Pricing:** [ai.google.dev/pricing](https://ai.google.dev/pricing)
- **Documentation:** [ai.google.dev/docs](https://ai.google.dev/docs)
- **Model Comparison:** [ai.google.dev/models](https://ai.google.dev/models/gemini)

---

## 💬 Need Help?

Having issues with Gemini setup? Check:
1. [Main README](README.md) - General setup instructions
2. [CHANGELOG](CHANGELOG.md) - Recent changes
3. [GitHub Issues](https://github.com/Fustli/ai-code-auditor/issues) - Report bugs

---

**🎉 Happy Analyzing with Gemini!** 🟠
