# Changelog

All notable changes to the AI Code Auditor project will be documented in this file.

## [2.2.0] - 2025-11-23

### 🤖 Google Gemini API Support Added

#### New Features
- **🟠 Dual AI Provider Support** - Choose between OpenAI and Google Gemini
- **🎛️ Provider Selection UI** - Easy dropdown in sidebar to switch providers
- **💰 Cost-Effective Option** - Gemini offers generous free tier
- **⚡ Fast Processing** - Gemini 1.5 Flash for quick analyses

#### Technical Changes
- **src/config.py** - Added `api_provider` field with support for "openai" and "gemini"
- **src/code_analyzer.py** - Conditional initialization based on provider
  - Added `google.generativeai` import and integration
  - Dual API call support with provider-specific formatting
  - JSON extraction logic for Gemini responses (handles markdown wrapping)
- **app.py** - Enhanced sidebar with provider selection dropdown
  - Dynamic API key input based on selected provider
  - Model dropdown changes based on provider
  - Provider-specific help links and configuration
- **requirements.txt** - Added `google-generativeai>=0.3.0`
- **.env.example** - Added `API_PROVIDER` and `GEMINI_API_KEY` configuration

#### Available Models
**OpenAI:**
- gpt-4o (default)
- gpt-4-turbo
- gpt-4
- gpt-3.5-turbo

**Google Gemini:**
- gemini-1.5-pro (default)
- gemini-1.5-flash (fastest, free tier)
- gemini-pro

#### Configuration
Two ways to configure provider:
1. **Sidebar UI** - Select provider and enter API key directly
2. **Environment File** - Set `API_PROVIDER=gemini` or `API_PROVIDER=openai` in `.env`

#### API Key Sources
- **OpenAI:** [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Gemini:** [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

#### Benefits
- **Flexibility** - Switch providers without code changes
- **Cost Optimization** - Use Gemini's free tier for development/testing
- **Reliability** - Fallback option if one provider has issues
- **Performance Options** - Choose speed vs quality based on needs

#### Documentation
- Updated README.md with dual provider information
- Added "AI Provider Options" section with comparison
- Updated setup instructions for both providers
- Added provider switching guide

---

## [2.1.0] - 2025-11-23

### 🐳 Docker Support Added

#### New Files
- **Dockerfile** - Optimized Docker image for the application
- **docker-compose.yml** - Complete Docker Compose configuration
- **.dockerignore** - Optimized Docker build context
- **docker-start.sh** - Interactive Docker management script
- **Makefile** - Quick commands for Docker operations
- **DOCKER.md** - Comprehensive Docker documentation

#### Docker Features
- **🚀 One-Command Setup** - Start with `./docker-start.sh`
- **🔧 Multiple Control Methods** - Script, Docker Compose, or Makefile
- **💾 Volume Persistence** - Data survives container restarts
- **🏥 Health Checks** - Automatic container health monitoring
- **🔄 Hot Reload** - Development mode with live code updates
- **📊 Resource Management** - Configurable memory and CPU limits
- **🌐 Network Isolation** - Secure container networking
- **📦 Easy Updates** - Simple rebuild and restart commands

#### Benefits
- No Python installation required
- Consistent environment across all systems
- Works on Linux, macOS, and Windows
- Production-ready deployment
- Easy CI/CD integration
- Simplified dependency management

#### Documentation
- Added Docker section to main README
- Created comprehensive DOCKER.md guide
- Added troubleshooting for Docker issues
- Included production deployment examples
- Added Kubernetes and Docker Swarm configs

### 📚 Updated Documentation
- Enhanced Quick Start section with Docker-first approach
- Added Docker troubleshooting section
- Included Docker benefits and use cases
- Updated prerequisites to mention Docker

---

## [2.0.0] - 2025-11-23

### 🎉 Major Refactor & Feature Release

This is a complete overhaul of the AI Code Auditor with numerous enhancements, new features, and improved architecture.

### ✨ New Features

#### UI/UX Enhancements
- **🌙 Dark Mode** - Beautiful dark theme with instant toggle
- **🎨 Modern Design** - Complete UI redesign with smooth animations
- **📱 Responsive Layout** - Improved mobile and tablet experience
- **🎭 Enhanced Animations** - Smooth transitions and loading states
- **📊 Interactive Charts** - Enhanced radar charts and visualizations

#### Analysis Improvements
- **📈 Code Metrics** - Cyclomatic complexity, comment ratios, line counts
- **🏆 Letter Grades** - A-F grading system for quick assessment
- **🎯 Priority System** - Issues ranked by severity and impact
- **📊 Enhanced Scoring** - Added Maintainability category
- **💡 Better Recommendations** - More actionable and specific fixes
- **⚡ Smart Caching** - Faster repeated analyses with result caching

#### New Capabilities
- **📁 Batch Analysis** - Analyze multiple files simultaneously
- **📊 Comparison Mode** - Compare code versions and track improvements
- **📈 Trend Tracking** - Visualize quality trends over time
- **💾 History Management** - Complete analysis history with statistics
- **📥 Multiple Export Formats** - Markdown, JSON, HTML report options
- **🔍 Advanced Filtering** - Filter issues by severity and type

#### Technical Improvements
- **🏗️ Modular Architecture** - Separated concerns into dedicated modules
- **🎨 UI Components** - Reusable component library (`ui_components.py`)
- **🛠️ Utility Functions** - Helper functions in `utils.py`
- **📊 Better Statistics** - Comprehensive metrics and analysis
- **⚡ Performance** - Optimized code analysis pipeline

### 🔄 Changed

#### Refactored Components
- **app.py** - Complete rewrite with modular design
  - Separated UI logic from business logic
  - Added session state management
  - Improved error handling
  - Better code organization

- **code_analyzer.py** - Enhanced analysis engine
  - Added caching mechanism
  - Improved prompt engineering
  - Better result processing
  - Batch analysis support
  - Extended metrics calculation

#### Enhanced Modules
- **config.py** - Improved configuration management
  - Better default values
  - Extended language support
  - More flexible settings

### 📦 Added Files

#### New Modules
- `src/ui_components.py` - Theme management and UI components
  - ThemeManager class with dark/light themes
  - Reusable UI component functions
  - Enhanced CSS styling
  - Animation definitions

- `src/utils.py` - Utility functions and helpers
  - CodeMetrics class for complexity calculation
  - AnalysisHistory with statistics
  - ComparisonEngine for version comparison
  - CodeFormatter for code beautification
  - Helper functions for grading and prioritization

### 📚 Documentation

- **README.md** - Completely rewritten documentation
  - Comprehensive feature list
  - Detailed setup instructions
  - Usage examples and workflows
  - Troubleshooting guide
  - Scoring system explanation
  - Roadmap for future features

- **CHANGELOG.md** - This file!
  - Document all changes
  - Version history
  - Migration guides

### 🐛 Bug Fixes

- Fixed issue with API key persistence
- Improved error handling for malformed code
- Fixed chart rendering in light mode
- Corrected score calculation weights
- Fixed file upload for large files
- Improved JSON parsing error handling

### ⚡ Performance

- Implemented analysis result caching
- Optimized code metrics calculation
- Reduced API calls with smart caching
- Improved chart rendering performance
- Faster UI updates with session state

### 🎯 Supported Languages

Extended support for:
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

### 📊 Analysis Categories

Enhanced scoring with 4 categories:
1. **Quality** (40% weight)
   - Readability and maintainability
   - Best practices adherence
   - Design patterns
   - Documentation

2. **Security** (35% weight)
   - Vulnerability detection
   - Authentication issues
   - Data exposure risks
   - Input validation

3. **Performance** (25% weight)
   - Algorithm efficiency
   - Resource optimization
   - Database queries
   - Memory management

4. **Maintainability** (New!)
   - Code structure
   - Naming conventions
   - Module organization
   - Technical debt

### 🔧 Configuration

New configuration options:
- Dark/Light theme toggle
- Analysis option toggles
- Model selection (GPT-4o, GPT-4-Turbo, GPT-3.5)
- Comparison mode
- Batch analysis mode
- Export format selection

### 📈 Statistics & History

New statistics features:
- Total analyses count
- Average score tracking
- Total issues found
- Score distribution charts
- Quality trend graphs
- History export (JSON)

### 💾 Export Options

Multiple export formats:
- **Markdown** - Clean, readable reports
- **JSON** - Structured data for CI/CD
- **HTML** - Styled web reports
- **History** - Complete analysis history

### 🎨 Theme System

Professional theming:
- **Dark Theme** - Eye-friendly dark mode
- **Light Theme** - Clean light mode
- Smooth transitions between themes
- Consistent color palette
- Custom CSS for all components

### 🚀 Advanced Features

#### Comparison Mode
- Track code improvements
- Score change visualization
- Issue trend analysis
- Improvement/regression detection

#### Batch Processing
- Multi-file analysis
- Aggregated statistics
- Per-file detailed reports
- Progress tracking

#### History Tracking
- Score distribution
- Quality trends over time
- Issue type breakdown
- Export capabilities

### 📦 Dependencies

Updated dependencies:
- streamlit>=1.28.0
- openai>=1.3.0
- pydantic>=2.0.0
- plotly>=5.17.0
- pandas>=2.0.0
- numpy>=1.24.0 (new)

### 🔐 Security

- Improved API key handling
- Better error messages (no sensitive data)
- Input sanitization
- Secure file handling

### 🎓 Examples

Updated example files:
- `examples/bad_code.py` - Common Python issues
- `examples/good_code.py` - Best practices
- `examples/bad_code.js` - JavaScript issues

### 🗺️ Future Roadmap

Planned features:
- VSCode extension integration
- GitHub Actions support
- GitLab CI/CD integration
- Real-time collaboration
- AI-powered refactoring
- Multi-language reports
- Custom rule definitions
- Team workspace features

---

## [1.0.0] - 2025-11-14

### Initial Release

- Basic code analysis functionality
- OpenAI GPT-4o integration
- File upload and code editor
- Basic scoring system
- Simple UI with Streamlit
- Example code files
- README documentation

---

## Migration Guide

### From 1.x to 2.0

#### Breaking Changes
- Session state structure has changed
- Analysis result format extended with new fields
- Export function signatures updated

#### New Requirements
- numpy>=1.24.0 (add to requirements)

#### Updated Configuration
- API key now configurable in sidebar (not just .env)
- New analysis options available
- Theme preference stored in session state

#### Migration Steps
1. Update requirements: `pip install -r requirements.txt`
2. Update .env file (optional, can use sidebar)
3. Clear browser cache for best experience
4. Check new documentation in README.md

#### Deprecated
- Old app.py saved as app_old.py
- Old README.md saved as README_old.md

---

**Note:** This is a major version update with significant architectural changes. All existing functionality is preserved and enhanced.