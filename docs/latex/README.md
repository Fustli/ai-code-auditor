# LaTeX Documentation

This directory contains the LaTeX documentation for the AI Code Auditor Pro project.

## Files

- `main.tex` - Main documentation file with complete project description

## Building the PDF

### Prerequisites

Install LaTeX distribution:
- **Linux (Ubuntu/Debian):** `sudo apt-get install texlive-full`
- **macOS:** Install MacTeX from https://www.tug.org/mactex/
- **Windows:** Install MiKTeX from https://miktex.org/

### Compile Commands

```bash
cd docs/latex

# Compile PDF (run twice for table of contents)
pdflatex main.tex
pdflatex main.tex

# Or use latexmk for automatic compilation
latexmk -pdf main.tex

# Clean auxiliary files
latexmk -c
```

### VS Code LaTeX Extension

If you have the LaTeX Workshop extension installed in VS Code:
1. Open `main.tex`
2. Press `Ctrl+Alt+B` (or `Cmd+Option+B` on Mac) to build
3. Press `Ctrl+Alt+V` (or `Cmd+Option+V` on Mac) to view PDF

## Document Structure

The documentation includes:

1. **Introduction** - Project overview and motivation
2. **Technical Architecture** - Technology stack and structure
3. **Functional Requirements** - Features and capabilities
4. **AI Integration** - Prompt engineering and provider support
5. **Scoring System** - Grade calculation and severity levels
6. **Implementation Details** - Installation and configuration
7. **Usage Examples** - Workflows and use cases
8. **Results and Testing** - Performance metrics
9. **Future Enhancements** - Planned features
10. **Conclusion** - Summary and lessons learned
11. **Appendix** - Code snippets and examples

## Customization

To customize the document:
- Update author name and university in the title section
- Modify the abstract to match your specific focus
- Add screenshots in the `images/` directory (create if needed)
- Adjust sections based on your requirements
- Update references with additional sources

## Output

The compiled PDF will be named `main.pdf` and will be generated in this directory.
