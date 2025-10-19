# 🧠 AI Code Auditor

**AI Code Auditor** is an LLM-powered tool that reviews your source code for **quality**, **security**, and **performance** issues.  
Upload your code files and get instant, structured feedback with clear improvement suggestions — all driven by AI. 🚀

---

## ✨ Features
- 🔍 **Code Review:** Detect readability, maintainability, and performance issues  
- 🔒 **Security Scan:** Identify potential vulnerabilities or unsafe patterns  
- ⚡ **Optimization Tips:** Get AI-powered suggestions for faster and cleaner code  
- 📊 **Scoring System:** Quality, performance, and security ratings  
- 💬 **Simple UI:** Upload and analyze code directly from a Streamlit/Gradio interface  

---

## 🧩 Tech Stack
- **Python 3.10+**
- **OpenAI GPT-4o / Ollama (Code Llama)** – for analysis  
- **Streamlit** or **Gradio** – for the web interface  
- **LangChain** (optional) – for structured prompt chains  

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-code-auditor.git
cd ai-code-auditor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
