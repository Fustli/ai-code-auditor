"""
Utilities for code analysis, metrics, and processing
"""
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class CodeMetrics:
    """Calculate various code metrics"""
    
    @staticmethod
    def calculate_complexity(code: str) -> Dict[str, Any]:
        """Calculate cyclomatic complexity and other metrics"""
        lines = code.split('\n')
        total_lines = len(lines)
        code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        comment_lines = len([l for l in lines if l.strip().startswith('#')])
        blank_lines = total_lines - code_lines - comment_lines
        
        # Count control structures for complexity
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'and', 'or']
        complexity = 1  # Base complexity
        
        for line in lines:
            for keyword in complexity_keywords:
                if re.search(rf'\b{keyword}\b', line):
                    complexity += 1
        
        # Count functions and classes
        functions = len(re.findall(r'^\s*def\s+\w+', code, re.MULTILINE))
        classes = len(re.findall(r'^\s*class\s+\w+', code, re.MULTILINE))
        
        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines,
            'complexity': complexity,
            'functions': functions,
            'classes': classes,
            'comment_ratio': round(comment_lines / max(code_lines, 1) * 100, 2)
        }
    
    @staticmethod
    def analyze_imports(code: str) -> Dict[str, List[str]]:
        """Analyze import statements"""
        import_pattern = r'^(?:from\s+(\S+)\s+)?import\s+(.+?)(?:\s+as\s+\S+)?$'
        imports = {'standard': [], 'third_party': [], 'local': []}
        
        for line in code.split('\n'):
            line = line.strip()
            match = re.match(import_pattern, line)
            if match:
                module = match.group(1) or match.group(2).split(',')[0].strip()
                # Simplified categorization
                if '.' in module or module.startswith('.'):
                    imports['local'].append(line)
                elif module in ['os', 'sys', 'json', 're', 'datetime', 'time']:
                    imports['standard'].append(line)
                else:
                    imports['third_party'].append(line)
        
        return imports
    
    @staticmethod
    def detect_code_smells(code: str) -> List[Dict[str, Any]]:
        """Detect common code smells"""
        smells = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Long line
            if len(line) > 120:
                smells.append({
                    'line': i,
                    'type': 'Long Line',
                    'description': f'Line exceeds 120 characters ({len(line)} chars)',
                    'severity': 'Low'
                })
            
            # Too many arguments (simplified check)
            if 'def ' in line:
                params = re.search(r'def\s+\w+\((.*?)\)', line)
                if params and len(params.group(1).split(',')) > 5:
                    smells.append({
                        'line': i,
                        'type': 'Too Many Parameters',
                        'description': 'Function has more than 5 parameters',
                        'severity': 'Medium'
                    })
            
            # Global variables
            if re.match(r'^[A-Z_]+\s*=', line):
                smells.append({
                    'line': i,
                    'type': 'Global Variable',
                    'description': 'Potential global variable detected',
                    'severity': 'Low'
                })
            
            # Bare except
            if re.match(r'^\s*except\s*:', line):
                smells.append({
                    'line': i,
                    'type': 'Bare Except',
                    'description': 'Catching all exceptions without specification',
                    'severity': 'Medium'
                })
        
        return smells

class AnalysisHistory:
    """Enhanced analysis history with statistics"""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
    
    def add_analysis(self, filename: str, results: Dict[str, Any]) -> None:
        """Add an analysis result to history"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'filename': filename,
            'results': results
        })
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics from history"""
        if not self.history:
            return {
                'total_analyses': 0,
                'average_score': 0,
                'total_issues': 0
            }
        
        total = len(self.history)
        avg_score = sum(r['results']['overall_score'] for r in self.history) / total
        total_issues = sum(len(r['results']['issues']) for r in self.history)
        
        # Score distribution
        excellent = sum(1 for r in self.history if r['results']['overall_score'] >= 8)
        good = sum(1 for r in self.history if 6 <= r['results']['overall_score'] < 8)
        fair = sum(1 for r in self.history if 4 <= r['results']['overall_score'] < 6)
        poor = sum(1 for r in self.history if r['results']['overall_score'] < 4)
        
        return {
            'total_analyses': total,
            'average_score': round(avg_score, 1),
            'total_issues': total_issues,
            'latest_analysis': self.history[-1]['timestamp'],
            'distribution': {
                'excellent': excellent,
                'good': good,
                'fair': fair,
                'poor': poor
            }
        }
    
    def get_trend_data(self) -> List[Dict[str, Any]]:
        """Get trend data for visualization"""
        return [
            {
                'timestamp': h['timestamp'],
                'score': h['results']['overall_score'],
                'filename': h['filename']
            }
            for h in self.history
        ]
    
    def export_to_json(self) -> str:
        """Export history to JSON"""
        return json.dumps(self.history, indent=2)

class CodeFormatter:
    """Code formatting utilities"""
    
    @staticmethod
    def format_python_code(code: str) -> str:
        """Basic Python code formatting"""
        lines = code.split('\n')
        formatted = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted.append('')
                continue
            
            # Decrease indent for closing brackets
            if stripped.startswith(('}', ']', ')')):
                indent_level = max(0, indent_level - 1)
            
            # Add line with proper indentation
            formatted.append('    ' * indent_level + stripped)
            
            # Increase indent after opening brackets or colons
            if stripped.endswith((':' , '{', '[', '(')):
                indent_level += 1
        
        return '\n'.join(formatted)
    
    @staticmethod
    def highlight_issues(code: str, issues: List[Dict[str, Any]]) -> str:
        """Add comments highlighting issues in code"""
        lines = code.split('\n')
        issue_lines = {issue.get('line'): issue for issue in issues if issue.get('line')}
        
        result = []
        for i, line in enumerate(lines, 1):
            result.append(line)
            if i in issue_lines:
                issue = issue_lines[i]
                result.append(f"# ⚠️ {issue['type']}: {issue['description']}")
        
        return '\n'.join(result)

class ComparisonEngine:
    """Compare code versions and analyze differences"""
    
    @staticmethod
    def compare_analyses(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two analysis results"""
        score_diff = new['overall_score'] - old['overall_score']
        issues_diff = len(new['issues']) - len(old['issues'])
        
        improvements = []
        regressions = []
        
        # Compare individual scores
        for category in ['Quality', 'Security', 'Performance']:
            old_score = old['scores'].get(category, 0)
            new_score = new['scores'].get(category, 0)
            diff = new_score - old_score
            
            if diff > 0:
                improvements.append(f"{category} improved by {diff:.1f} points")
            elif diff < 0:
                regressions.append(f"{category} decreased by {abs(diff):.1f} points")
        
        return {
            'score_change': score_diff,
            'issues_change': issues_diff,
            'improvements': improvements,
            'regressions': regressions,
            'overall_status': 'improved' if score_diff > 0 else 'regressed' if score_diff < 0 else 'unchanged'
        }
    
    @staticmethod
    def generate_diff_summary(comparison: Dict[str, Any]) -> str:
        """Generate a human-readable diff summary"""
        status = comparison['overall_status']
        score_change = comparison['score_change']
        
        if status == 'improved':
            emoji = "📈"
            message = f"Code quality improved by {score_change:.1f} points!"
        elif status == 'regressed':
            emoji = "📉"
            message = f"Code quality decreased by {abs(score_change):.1f} points"
        else:
            emoji = "➡️"
            message = "Code quality remained unchanged"
        
        summary = f"{emoji} {message}\n\n"
        
        if comparison['improvements']:
            summary += "✅ Improvements:\n"
            for imp in comparison['improvements']:
                summary += f"  • {imp}\n"
        
        if comparison['regressions']:
            summary += "\n⚠️ Regressions:\n"
            for reg in comparison['regressions']:
                summary += f"  • {reg}\n"
        
        return summary

def calculate_overall_grade(score: float) -> str:
    """Convert numerical score to letter grade"""
    if score >= 9:
        return "A+"
    elif score >= 8:
        return "A"
    elif score >= 7:
        return "B+"
    elif score >= 6:
        return "B"
    elif score >= 5:
        return "C+"
    elif score >= 4:
        return "C"
    else:
        return "D"

def generate_improvement_priority(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Prioritize issues based on severity and type"""
    severity_weight = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
    type_weight = {'Security': 3, 'Performance': 2, 'Quality': 1}
    
    prioritized = []
    for issue in issues:
        priority_score = (
            severity_weight.get(issue['severity'], 1) * 10 +
            type_weight.get(issue['type'], 1)
        )
        prioritized.append({
            **issue,
            'priority_score': priority_score
        })
    
    return sorted(prioritized, key=lambda x: x['priority_score'], reverse=True)