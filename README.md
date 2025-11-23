# 🧠 AI Code Auditor Pro

**AI Code Auditor Pro** is a professional, AI-powered code analysis platform that provides comprehensive quality, security, and performance assessments. Built with a beautiful dark mode interface and powered by OpenAI GPT-4o or Google Gemini. 🚀

![AI Code Auditor](https://img.shields.io/badge/AI-Powered-blue) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green) ![Gemini](https://img.shields.io/badge/Google-Gemini-orange) ![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red) ![Python](https://img.shields.io/badge/Python-3.8+-yellow)

---

## ✨ Key Features

### 🎨 Modern UI/UX
- **🌙 Dark Mode** - Toggle between beautiful dark and light themes
- **📱 Responsive Design** - Works seamlessly on all devices
- **🎭 Animated Interface** - Smooth transitions and loading animations
- **📊 Interactive Charts** - Radar charts, bar graphs, and trend visualizations

### 🧠 Advanced Analysis
- **🔍 Deep Code Analysis** - Quality, security, performance, and maintainability scoring
- **📈 Code Metrics** - Cyclomatic complexity, comment ratios, and more
- **🏆 Letter Grades** - A-F grading system with detailed breakdowns
- **🎯 Priority System** - Issues ranked by severity and impact
- **💡 Smart Recommendations** - Actionable fixes with code examples

### 🚀 Powerful Features
- **📁 Batch Analysis** - Analyze multiple files simultaneously
- **📊 Comparison Mode** - Compare code versions and track improvements
- **📈 Trend Tracking** - Visualize quality trends over time
- **💾 History Management** - Keep track of all analyses with statistics
- **📥 Multiple Export Formats** - Markdown, JSON, HTML, and PDF reports
- **⚡ Smart Caching** - Faster repeated analyses

### 🛡️ Comprehensive Security
- Vulnerability detection (SQL injection, XSS, CSRF)
- Authentication and authorization flaw identification
- Data exposure risk assessment
- Cryptography misuse detection
- Input validation issue identification

### ⚡ Performance Optimization
- Algorithm complexity analysis
- Resource usage optimization suggestions
- Database query efficiency checks
- Memory leak detection
- Asynchronous operation recommendations

---

## 🧩 Tech Stack

- **Python 3.8+** – Core application language
- **OpenAI GPT-4o / Google Gemini** – Advanced AI analysis engines (choose your provider!)
- **Streamlit** – Modern web framework with rich components
- **Plotly** – Interactive data visualizations and charts
- **Pydantic** – Data validation and settings management
- **Streamlit-Ace** – Advanced code editor with syntax highlighting
- **Pandas** – Data analysis and trend tracking

---

## 🚀 Quick Start

### 🐳 Docker (Recommended - Easiest Setup)

**Prerequisites:** Docker and Docker Compose installed

```bash
# Clone the repository
git clone https://github.com/Fustli/ai-code-auditor.git
cd ai-code-auditor

# Copy and configure environment
cp config/.env.example .env
# Edit .env and add your API key

# Start with one command!
./scripts/docker-start.sh

# OR use Docker Compose directly
cd scripts && docker-compose up -d

# OR use Make
cd scripts && make build && make up
```

**Access at:** `http://localhost:8501`

---

### 🐍 Manual Setup (Python)

**Prerequisites:** Python 3.8+ installed

#### 1. Clone the Repository
```bash
git clone https://github.com/Fustli/ai-code-auditor.git
cd ai-code-auditor
```

#### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure AI API (OpenAI or Gemini)
```bash
# Copy the example environment file from config folder
cp config/.env.example .env

# Edit .env and add your API key
# Option 1 - OpenAI: Get your key from: https://platform.openai.com/api-keys
# Option 2 - Gemini: Get your key from: https://makersuite.google.com/app/apikey
```

Example `.env` file for **OpenAI**:
```bash
API_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
AI_MODEL=gpt-4o
MAX_TOKENS=4000
TEMPERATURE=0.1
```

Example `.env` file for **Google Gemini**:
```bash
API_PROVIDER=gemini
GEMINI_API_KEY=AIza-your-api-key-here
AI_MODEL=gemini-1.5-pro
MAX_TOKENS=4000
TEMPERATURE=0.1
```

> **💡 Tip:** You can switch between providers anytime by changing `API_PROVIDER` in your `.env` file or selecting the provider in the sidebar UI!

#### 4. Run the Application
```bash
# Using the startup script (Linux/Mac)
./start.sh

# Or manually
streamlit run app.py
```

🎉 **Done!** Open your browser to `http://localhost:8501`

---

## 🤖 AI Provider Options

AI Code Auditor Pro supports **two powerful AI providers** - choose the one that works best for you!

### 🟢 OpenAI GPT-4o
**Best for:** Advanced reasoning, comprehensive analysis, enterprise use

- **Models Available:** gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo
- **API Key:** Get from [platform.openai.com](https://platform.openai.com/api-keys)
- **Pricing:** Pay-as-you-go (typically ~$0.01-0.03 per analysis)
- **Strengths:** Superior code understanding, detailed recommendations, excellent multi-language support

### 🟠 Google Gemini
**Best for:** Cost-effective analysis, fast responses, Google ecosystem integration

- **Models Available:** gemini-1.5-pro, gemini-1.5-flash, gemini-pro
- **API Key:** Get from [makersuite.google.com](https://makersuite.google.com/app/apikey)
- **Pricing:** Free tier available! (60 requests/min with gemini-1.5-flash)
- **Strengths:** Generous free tier, fast processing, multimodal capabilities

### 🔄 Switching Providers
You can easily switch between providers in the sidebar UI or by changing the `.env` file:
```bash
# In .env file
API_PROVIDER=gemini  # or "openai"
```

---

## 📖 How to Use

### 🎨 Theme Selection
- Toggle **Dark Mode** in the sidebar for a comfortable viewing experience
- Switch between light and dark themes instantly

### 📁 Upload Files
1. Navigate to the **"Upload Files"** tab
2. Drag and drop or select your code files
3. Enable **Batch Mode** for multiple files
4. Click **"Analyze"** to start the analysis

### ✏️ Code Editor
1. Go to the **"Code Editor"** tab
2. Select your programming language
3. Paste or type your code directly
4. Click **"Analyze Code"** for instant feedback

### 📊 View Results
1. Check the **"Results"** tab for detailed analysis
2. Navigate through multiple sub-tabs:
   - **Overview**: Summary, scores, and strengths
   - **Issues**: Detailed issue list with filters
   - **Recommendations**: Actionable improvement suggestions
   - **Metrics**: Code complexity and statistics

### 📈 Track Progress
1. Visit the **"History & Trends"** tab
2. View analysis history and statistics
3. See score distribution and trends over time
4. Export history data for external analysis

---

## 🎯 Analysis Categories

### 📊 Code Quality (Weight: 40%)
- Readability and maintainability
- Best practices adherence
- Design patterns usage
- Documentation quality
- Error handling completeness
- Code duplication detection

### 🔒 Security (Weight: 35%)
- Vulnerability identification
- Authentication/authorization issues
- Data exposure risks
- Input validation problems
- Cryptography implementation
- Dependency security

### ⚡ Performance (Weight: 25%)
- Algorithm efficiency
- Resource optimization
- Database query performance
- Memory management
- Caching opportunities
- Async operation potential

### 🔧 Maintainability
- Code structure quality
- Naming conventions
- Module organization
- Test coverage indicators
- Technical debt assessment

---

## 📊 Scoring System

### Overall Grade Scale
- **A+ (9.5-10):** 🟢 Exceptional code - Production ready
- **A (9.0-9.4):** 🟢 Excellent code - Minor polish needed
- **A- (8.5-8.9):** 🟢 Very good code - Few improvements
- **B+ (8.0-8.4):** 🔵 Good code - Some enhancements recommended
- **B (7.0-7.9):** 🔵 Decent code - Notable improvements needed
- **C (5.0-6.9):** 🟡 Fair code - Significant refactoring suggested
- **D (3.0-4.9):** 🟠 Poor code - Major issues present
- **F (0-2.9):** 🔴 Critical - Immediate attention required

### Issue Severity Levels
- **Critical:** Immediate security threats or system failures
- **High:** Significant problems affecting functionality
- **Medium:** Important issues impacting code quality
- **Low:** Minor improvements and style suggestions

---

## 🛠️ Configuration Options

### Sidebar Settings

**Analysis Options:**
- 🔒 Security Analysis (on/off)
- ⚡ Performance Analysis (on/off)
- 🎨 Style Analysis (on/off)
- 📊 Code Metrics (on/off)

**AI Model Selection:**
- GPT-4o (Recommended)
- GPT-4-Turbo
- GPT-4
- GPT-3.5-Turbo

**Advanced Features:**
- 📊 Comparison Mode - Compare with previous analysis
- 📁 Batch Analysis - Analyze multiple files at once
- 📥 Export Format - Choose report format (MD/JSON/HTML/PDF)

---

## 🌍 Supported Languages

| Language | Extensions | Status |
|----------|-----------|--------|
| Python | `.py` | ✅ Full Support |
| JavaScript | `.js` | ✅ Full Support |
| TypeScript | `.ts`, `.tsx` | ✅ Full Support |
| Java | `.java` | ✅ Full Support |
| C/C++ | `.c`, `.cpp`, `.h`, `.hpp` | ✅ Full Support |
| Go | `.go` | ✅ Full Support |
| Rust | `.rs` | ✅ Full Support |
| PHP | `.php` | ✅ Full Support |
| Ruby | `.rb` | ✅ Full Support |
| Swift | `.swift` | ✅ Full Support |
| Kotlin | `.kt` | ✅ Full Support |
| Scala | `.scala` | ✅ Full Support |

---

## 📥 Export Options

### Markdown Reports
Clean, readable reports perfect for documentation and sharing

### JSON Export
Structured data for integration with other tools and CI/CD pipelines

### HTML Reports
Beautiful, styled reports that can be viewed in any browser

### History Export
Export complete analysis history for long-term tracking

---

## 🎓 Example Workflow

### Basic Analysis
```bash
1. Upload your Python file
2. Click "Analyze"
3. Review the results in the Results tab
4. Export the report for documentation
```

### Batch Analysis
```bash
1. Enable "Batch Analysis" in sidebar
2. Upload multiple files
3. Click "Analyze All Files"
4. Review individual file results
5. Check aggregated statistics
```

### Tracking Improvements
```bash
1. Analyze your initial code
2. Make improvements based on recommendations
3. Enable "Comparison Mode"
4. Re-analyze the improved code
5. View the improvement metrics
```

---

## 🔍 Example Analysis Output

```
# Code Audit Report

Overall Score: 8.5/10
Grade: A-

## Scores
- Quality: 9/10
- Security: 8/10
- Performance: 8/10
- Maintainability: 9/10

## Summary
Well-structured code with good practices. Minor security
improvements recommended for input validation.

## Strengths
✓ Excellent code organization
✓ Comprehensive error handling
✓ Good documentation coverage
✓ Efficient algorithm implementation

## Issues (3 found)
1. [Medium] Input Validation
   - Missing validation for user input in function handle_request()
   - Line 45: Potential SQL injection vector
   - Fix: Use parameterized queries

2. [Low] Code Style
   - Line 78: Function exceeds 50 lines
   - Fix: Consider breaking into smaller functions

3. [Low] Performance
   - Line 112: Nested loop could be optimized
   - Fix: Use hash map for O(1) lookup
```

---

## 🚀 Advanced Features

### Comparison Mode
Track code improvements over time by comparing analyses:
- Score changes visualization
- Issue trend analysis
- Improvement/regression detection
- Side-by-side metrics comparison

### Batch Processing
Analyze entire project directories:
- Multi-file analysis support
- Aggregated statistics
- Per-file detailed reports
- Project-wide issue summary

### History & Trends
Comprehensive analysis tracking:
- Score distribution charts
- Quality trends over time
- Issue type breakdown
- Export capabilities

---

## 🐳 Docker Deployment

### Quick Docker Commands

```bash
# Using the interactive script (easiest)
cd scripts && ./docker-start.sh

# Using Docker Compose
cd scripts
docker-compose up -d          # Start
docker-compose down           # Stop
docker-compose logs -f        # View logs
docker-compose restart        # Restart

# Using Makefile
cd scripts
make build                    # Build image
make up                       # Start application
make down                     # Stop application
make logs                     # View logs
make restart                  # Restart
make clean                    # Clean up everything
```

### Docker Benefits

✅ **Zero Configuration** - No Python setup needed  
✅ **Consistent Environment** - Works the same everywhere  
✅ **Easy Updates** - Pull and rebuild in seconds  
✅ **Isolated** - Doesn't interfere with your system  
✅ **Portable** - Deploy anywhere Docker runs  

### Docker Troubleshooting

**Container won't start:**
```bash
cd scripts
docker-compose logs          # Check logs
docker-compose down -v       # Clean slate
docker-compose up --build    # Rebuild
```

**Port already in use:**
```bash
# Edit scripts/docker-compose.yml and change port
ports:
  - "8502:8501"  # Use 8502 instead
```

---

## 🐛 Troubleshooting

### API Key Issues
- Ensure your OpenAI API key is valid
- Check that you have sufficient API credits
- Verify the key is correctly set in the sidebar

### Analysis Errors
- Check code syntax is valid
- Ensure file size is reasonable (< 5MB)
- Verify file encoding is UTF-8

### Performance Issues
- Clear analysis cache if needed
- Reduce max_tokens for faster responses
- Use GPT-3.5-Turbo for quicker analysis

---

## 📝 Development

### Project Structure
```
ai-code-auditor/
├── app.py                    # Main application entry point
├── start.sh                  # Quick startup script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
├── .env                      # Environment variables (create from config/.env.example)
├── .gitignore               # Git ignore patterns
├── src/                     # Source code modules
│   ├── __init__.py          # Package initializer
│   ├── config.py            # Configuration management
│   ├── code_analyzer.py     # AI analysis engine
│   ├── ui_components.py     # UI theme and components
│   └── utils.py             # Utility functions
├── config/                  # Configuration files
│   └── .env.example         # Environment template
├── scripts/                 # Deployment & utility scripts
│   ├── docker-compose.yml   # Docker Compose configuration
│   ├── Dockerfile           # Docker image definition
│   ├── .dockerignore        # Docker ignore patterns
│   ├── docker-start.sh      # Docker startup script
│   └── Makefile             # Make commands for Docker
└── examples/                # Code examples for testing
    ├── bad_code.py          # Python with issues
    ├── good_code.py         # Clean Python code
    └── bad_code.js          # JavaScript example
```

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT-4o API
- **Streamlit** for the amazing web framework
- **Plotly** for interactive visualizations
- The open-source community for inspiration

---

## 📞 Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/Fustli/ai-code-auditor/issues)
- **GitHub Discussions:** [Ask questions and share ideas](https://github.com/Fustli/ai-code-auditor/discussions)
- **Documentation:** Check this README for detailed information

<div align="center">

**Made with ❤️ by [Fustli](https://github.com/Fustli)**

**Powered by OpenAI GPT-4o | Built with Streamlit**

⭐ Star this repo if you find it useful!

</div>