# 🧠 AI Code Auditor

**AI Code Auditor** is a beautiful, LLM-powered tool that reviews your source code for **quality**, **security**, and **performance** issues. Upload your code files or paste code directly and get instant, structured feedback with clear improvement suggestions — all driven by OpenAI GPT-4o. 🚀

![AI Code Auditor](https://img.shields.io/badge/AI-Powered-blue) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green) ![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)

---

## ✨ Features

- 🔍 **Smart Code Review:** Detect readability, maintainability, and best practice violations
- 🔒 **Security Analysis:** Identify vulnerabilities, unsafe patterns, and security risks  
- ⚡ **Performance Optimization:** Get AI suggestions for faster and more efficient code
- 📊 **Visual Scoring System:** Interactive radar charts and metrics for quality assessment
- 💻 **Multi-language Support:** Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
- 🎨 **Beautiful UI:** Modern, responsive interface with syntax highlighting
- 📥 **Export Reports:** Download detailed analysis reports in Markdown format
- � **File Upload + Code Editor:** Upload files or paste code directly with syntax highlighting

---

## 🧩 Tech Stack

- **Python 3.8+** – Core application
- **OpenAI GPT-4o** – AI analysis engine  
- **Streamlit** – Beautiful web interface  
- **Plotly** – Interactive data visualizations
- **Pydantic** – Data validation and settings
- **Streamlit-Ace** – Advanced code editor

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Fustli/ai-code-auditor.git
cd ai-code-auditor
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure OpenAI API
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get your key from: https://platform.openai.com/api-keys
```

### 4. Run the Application
```bash
streamlit run app.py
```

🎉 **That's it!** Your AI Code Auditor will be available at `http://localhost:8501`

---

## 📖 How to Use

### Option 1: Upload Files
1. Click the **"Upload Code"** tab
2. Drag and drop or select your code files
3. Click **"Analyze"** to get instant feedback

### Option 2: Code Editor  
1. Click the **"Code Editor"** tab
2. Paste your code into the editor
3. Click **"Analyze Code"** for real-time analysis

### Option 3: Example Files
Try the included example files in the `examples/` directory:
- `bad_code.py` - Contains various issues for testing
- `good_code.py` - Well-written code examples  
- `bad_code.js` - JavaScript with common problems

---

## 🎯 Analysis Features

### Quality Analysis
- Code readability and maintainability
- Best practices and design patterns
- Naming conventions and documentation
- Error handling and edge cases

### Security Analysis  
- Vulnerability detection
- Input validation issues
- Authentication and authorization flaws
- Data exposure risks

### Performance Analysis
- Algorithm complexity optimization
- Resource usage efficiency  
- Memory management
- Database query optimization

---

## 📊 Scoring System

Each analysis provides:
- **Overall Score (1-10):** Weighted average of all categories
- **Quality Score (1-10):** Code structure and maintainability  
- **Security Score (1-10):** Vulnerability and safety assessment
- **Performance Score (1-10):** Efficiency and optimization level

Score ranges:
- **8-10:** 🟢 Excellent
- **6-7:** 🔵 Good  
- **4-5:** 🟡 Fair
- **1-3:** 🔴 Needs Improvement

---

## 🛠️ Configuration

### Environment Variables
Create a `.env` file with:
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o  # Optional: gpt-4o, gpt-4-turbo, gpt-3.5-turbo
MAX_TOKENS=4000      # Optional: max response tokens
TEMPERATURE=0.1      # Optional: response creativity (0.0-1.0)
```

### Supported Languages
- Python (.py)
- JavaScript (.js) 
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .h, .hpp)
- Go (.go)
- Rust (.rs)
- PHP (.php)
- Ruby (.rb)
- Swift (.swift)
- Kotlin (.kt)
- Scala (.scala)

---

## 🚀 Advanced Usage

### Custom Analysis
Use the sidebar to customize your analysis:
- Toggle security analysis on/off
- Enable/disable performance checks  
- Include/exclude style analysis
- Select different AI models

### Export Reports
Click **"Export Results"** to download detailed reports in Markdown format with:
- Complete analysis summary
- Issue breakdown with severity levels
- Actionable recommendations  
- Score history and trends

---

## 📝 Example Analysis Output

```
# AI Code Audit Report

**Overall Score:** 6.8/10

## Scores  
- Quality: 7/10
- Security: 5/10  
- Performance: 8/10

## Issues Found
- Security: Plain text password storage (High)
- Performance: O(n) user lookup could use hash map (Medium) 
- Quality: Missing input validation (Medium)

## Recommendations
- Implement password hashing with salt
- Use dictionary for O(1) user lookups
- Add comprehensive input validation
- Include error handling for edge cases
```
