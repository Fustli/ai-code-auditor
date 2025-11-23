# 🚀 Quick Reference Card

## 🐳 Docker Commands (Recommended)

### First Time Setup
```bash
git clone https://github.com/Fustli/ai-code-auditor.git
cd ai-code-auditor
cp .env.example .env
# Add your OPENAI_API_KEY to .env
./docker-start.sh
```

### Daily Usage
```bash
# Start
docker-compose up -d
# or
make up

# Stop
docker-compose down
# or
make down

# View logs
docker-compose logs -f
# or
make logs

# Restart
docker-compose restart
# or
make restart
```

### Maintenance
```bash
# Update application
git pull
docker-compose up -d --build

# Clean everything
docker-compose down -v
make clean
```

---

## 🐍 Python Commands (Manual Setup)

### First Time Setup
```bash
git clone https://github.com/Fustli/ai-code-auditor.git
cd ai-code-auditor
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

### Daily Usage
```bash
# Activate environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Start application
streamlit run app.py

# Or use the script
./start.sh
```

### Maintenance
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Update application
git pull
```

---

## 📝 Environment Variables

Required in `.env`:
```bash
OPENAI_API_KEY=sk-your-key-here
```

Optional:
```bash
OPENAI_MODEL=gpt-4o          # gpt-4o, gpt-4-turbo, gpt-3.5-turbo
MAX_TOKENS=4000              # Max response tokens
TEMPERATURE=0.1              # 0.0-1.0, lower = more focused
```

---

## 🌐 Access URLs

- **Local:** http://localhost:8501
- **Health Check:** http://localhost:8501/_stcore/health

---

## 🎯 Quick Features

### In the Application
- **🌙 Toggle Dark Mode** - Sidebar > Dark Mode switch
- **📁 Upload Files** - Upload Files tab
- **✏️ Code Editor** - Code Editor tab with syntax highlighting
- **📊 View Results** - Results tab with detailed analysis
- **📈 Track History** - History & Trends tab

### Analysis Options (Sidebar)
- ✅ Security Analysis
- ✅ Performance Analysis  
- ✅ Style Analysis
- ✅ Code Metrics

### Advanced Features (Sidebar)
- 📊 Comparison Mode - Compare versions
- 📁 Batch Analysis - Multiple files
- 📥 Export Format - MD/JSON/HTML

---

## 🐛 Quick Troubleshooting

### Docker Issues
```bash
# Won't start
docker-compose logs
docker-compose down -v
docker-compose up --build

# Port in use
# Edit docker-compose.yml, change "8501:8501" to "8502:8501"
```

### Python Issues
```bash
# Import errors
pip install -r requirements.txt

# Streamlit not found
pip install streamlit

# Permission errors
chmod +x start.sh
```

### API Issues
```bash
# Check API key
cat .env | grep OPENAI_API_KEY

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY"
```

---

## 📚 Documentation

- **README.md** - Complete documentation
- **DOCKER.md** - Docker deployment guide
- **CHANGELOG.md** - Version history
- **Examples** - `examples/` directory

---

## 🆘 Getting Help

- **GitHub Issues:** https://github.com/Fustli/ai-code-auditor/issues
- **Documentation:** Read README.md and DOCKER.md
- **OpenAI Help:** https://help.openai.com/

---

## 🎓 Example Workflow

### Analyze a File
1. Start the application
2. Navigate to "Upload Files"
3. Upload your code file
4. Click "Analyze"
5. View results in "Results" tab
6. Export report if needed

### Compare Versions
1. Enable "Comparison Mode" in sidebar
2. Analyze version 1
3. Analyze version 2
4. View comparison metrics

### Batch Analysis
1. Enable "Batch Analysis" in sidebar
2. Upload multiple files
3. Click "Analyze All"
4. View aggregated results

---

**Made with ❤️ | Powered by OpenAI GPT-4o**