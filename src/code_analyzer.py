import json
import re
from typing import Dict, List, Any, Optional
from openai import OpenAI
import google.generativeai as genai
from src.config import Config
from src.utils import CodeMetrics, generate_improvement_priority
import time

class CodeAnalyzer:
    """Enhanced AI-powered code analyzer using OpenAI GPT or Google Gemini models"""
    
    def __init__(self, config: Config):
        self.config = config
        self.cache = {}  # Simple cache for repeated analyses
        
        # Initialize the appropriate API client
        if config.api_provider == "gemini":
            genai.configure(api_key=config.api_key)
            self.client = None
            self.gemini_model = genai.GenerativeModel(config.model)
        else:
            self.client = OpenAI(api_key=config.api_key)
            self.gemini_model = None
        
    def analyze_code(
        self,
        code: str,
        filename: str = "code.py",
        include_security: bool = True,
        include_performance: bool = True,
        include_style: bool = True,
        include_metrics: bool = True
    ) -> Dict[str, Any]:
        """
        Enhanced code analysis with metrics and caching
        
        Args:
            code: The source code to analyze
            filename: Name of the file being analyzed
            include_security: Whether to include security analysis
            include_performance: Whether to include performance analysis
            include_style: Whether to include style analysis
            include_metrics: Whether to include code metrics
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        
        # Check cache
        cache_key = hash(code + filename)
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Determine programming language
        language = self.config.get_file_extension_language(filename) or "python"
        
        # Calculate code metrics if enabled
        metrics = None
        if include_metrics and language == "python":
            metrics = CodeMetrics.calculate_complexity(code)
        
        # Build analysis prompt
        prompt = self._build_enhanced_analysis_prompt(
            code, language, filename,
            include_security, include_performance, include_style, metrics
        )
        
        try:
            start_time = time.time()
            
            # Call appropriate API based on provider
            if self.config.api_provider == "gemini":
                # Use Google Gemini API
                full_prompt = f"{self._get_enhanced_system_prompt()}\n\n{prompt}"
                
                response = self.gemini_model.generate_content(
                    full_prompt,
                    generation_config=genai.GenerationConfig(
                        max_output_tokens=self.config.max_tokens,
                        temperature=self.config.temperature,
                    )
                )
                
                result_text = response.text
                
            else:
                # Use OpenAI API
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {
                            "role": "system",
                            "content": self._get_enhanced_system_prompt()
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    response_format={"type": "json_object"}
                )
                
                result_text = response.choices[0].message.content
            
            analysis_time = time.time() - start_time
            
            # Parse response - extract JSON if wrapped in markdown
            result_text = result_text.strip()
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            analysis_result = json.loads(result_text)
            
            # Post-process and validate results
            processed_result = self._process_enhanced_analysis_result(
                analysis_result, metrics, analysis_time
            )
            
            # Cache result
            self.cache[cache_key] = processed_result
            
            return processed_result
            
        except json.JSONDecodeError as e:
            return self._create_error_result(f"Failed to parse AI response: {str(e)}")
        except Exception as e:
            return self._create_error_result(f"Analysis failed: {str(e)}")
    
    def _get_enhanced_system_prompt(self) -> str:
        """Get the enhanced system prompt for the AI model"""
        return """You are an elite code reviewer and security analyst with expertise in software engineering best practices. Your analysis should be:

**COMPREHENSIVE**: Cover all aspects of code quality, security, and performance
**ACTIONABLE**: Provide specific, implementable recommendations
**PRIORITIZED**: Focus on the most impactful issues first
**CONSTRUCTIVE**: Be thorough but encouraging

Analyze code for:

1. **CODE QUALITY**: 
   - Readability and maintainability
   - Design patterns and architecture
   - Best practices adherence
   - Documentation and comments
   - Error handling
   - Code duplication

2. **SECURITY**: 
   - Vulnerabilities (SQL injection, XSS, CSRF, etc.)
   - Authentication and authorization flaws
   - Data exposure risks
   - Input validation issues
   - Cryptography misuse
   - Dependency vulnerabilities

3. **PERFORMANCE**: 
   - Algorithm efficiency and complexity
   - Resource usage optimization
   - Database query efficiency
   - Caching opportunities
   - Memory leaks
   - Asynchronous operations

You must respond with a valid JSON object:
{
    "overall_score": <number 1-10>,
    "grade": "<letter grade A-F>",
    "scores": {
        "Quality": <number 1-10>,
        "Security": <number 1-10>,
        "Performance": <number 1-10>,
        "Maintainability": <number 1-10>
    },
    "issues": [
        {
            "type": "Quality|Security|Performance",
            "severity": "Low|Medium|High|Critical",
            "title": "Brief title of the issue",
            "description": "Clear description of the issue",
            "line": <line number or null>,
            "code": "problematic code snippet or null",
            "recommendation": "How to fix this specific issue"
        }
    ],
    "recommendations": [
        "High-level recommendation for improvement"
    ],
    "strengths": [
        "What the code does well"
    ],
    "summary": "Brief 2-3 sentence summary of the analysis",
    "complexity_assessment": "Assessment of code complexity",
    "best_practices_score": <number 1-10>
}

Be thorough, specific, and constructive in your feedback."""

    def _build_enhanced_analysis_prompt(
        self,
        code: str,
        language: str,
        filename: str,
        include_security: bool,
        include_performance: bool,
        include_style: bool,
        metrics: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build enhanced analysis prompt for the AI model"""
        
        analysis_aspects = []
        if include_style:
            analysis_aspects.append("code quality, style, and maintainability")
        if include_security:
            analysis_aspects.append("security vulnerabilities and risks")
        if include_performance:
            analysis_aspects.append("performance optimization opportunities")
        
        aspects_text = ", ".join(analysis_aspects)
        
        metrics_text = ""
        if metrics:
            metrics_text = f"""

**Code Metrics**:
- Total lines: {metrics['total_lines']}
- Code lines: {metrics['code_lines']}
- Comment ratio: {metrics['comment_ratio']}%
- Cyclomatic complexity: {metrics['complexity']}
- Functions: {metrics['functions']}
- Classes: {metrics['classes']}"""
        
        return f"""Please provide a comprehensive analysis of this {language} code file ({filename}) focusing on {aspects_text}.
{metrics_text}

**Code to analyze**:
```{language}
{code}
```

**Analysis Requirements**:
1. Evaluate code quality, readability, and maintainability
2. Identify security vulnerabilities and unsafe patterns
3. Assess performance and algorithmic efficiency
4. Detect code smells and anti-patterns
5. Provide specific line numbers for issues when possible
6. Give actionable, prioritized recommendations
7. Highlight strengths of the code
8. Assign appropriate severity levels to issues

**Scoring Criteria**:
- 9-10: Excellent code with minor or no issues
- 7-8: Good code with some improvement areas
- 5-6: Acceptable code with notable issues
- 3-4: Poor code needing significant refactoring
- 1-2: Severely flawed code with critical issues

Provide detailed, constructive feedback with specific examples and fix suggestions."""

    def _process_enhanced_analysis_result(
        self, 
        raw_result: Dict[str, Any],
        metrics: Optional[Dict[str, Any]] = None,
        analysis_time: float = 0
    ) -> Dict[str, Any]:
        """Process and enhance the raw analysis result"""
        
        # Ensure required fields exist
        processed = {
            "overall_score": raw_result.get("overall_score", 5),
            "grade": raw_result.get("grade", "C"),
            "scores": raw_result.get("scores", {}),
            "issues": raw_result.get("issues", []),
            "recommendations": raw_result.get("recommendations", []),
            "strengths": raw_result.get("strengths", []),
            "summary": raw_result.get("summary", "Analysis completed"),
            "complexity_assessment": raw_result.get("complexity_assessment", ""),
            "best_practices_score": raw_result.get("best_practices_score", 5),
            "metrics": metrics,
            "analysis_time": round(analysis_time, 2)
        }
        
        # Validate and normalize scores
        processed["scores"] = self._normalize_enhanced_scores(processed["scores"])
        
        # Calculate overall score if not provided
        if not processed["overall_score"] or processed["overall_score"] == 5:
            scores = processed["scores"]
            weights = self.config.score_weights
            processed["overall_score"] = round(
                scores.get("Quality", 5) * weights.get("quality", 0.4) +
                scores.get("Security", 5) * weights.get("security", 0.35) +
                scores.get("Performance", 5) * weights.get("performance", 0.25),
                1
            )
        
        # Validate and enhance issues
        processed["issues"] = self._validate_enhanced_issues(processed["issues"])
        
        # Prioritize issues
        processed["prioritized_issues"] = generate_improvement_priority(processed["issues"])
        
        # Generate statistics
        processed["statistics"] = self._generate_issue_statistics(processed["issues"])
        
        # Ensure recommendations is a list
        if isinstance(processed["recommendations"], str):
            processed["recommendations"] = [processed["recommendations"]]
        
        if isinstance(processed["strengths"], str):
            processed["strengths"] = [processed["strengths"]]
        
        return processed
    
    def _normalize_enhanced_scores(self, scores: Dict[str, Any]) -> Dict[str, int]:
        """Normalize and validate scores with additional categories"""
        normalized = {
            "Quality": 5,
            "Security": 5,
            "Performance": 5,
            "Maintainability": 5
        }
        
        for key, value in scores.items():
            if isinstance(value, (int, float)):
                normalized[key] = max(1, min(10, int(round(value))))
        
        return normalized
    
    def _validate_enhanced_issues(self, issues: List[Dict]) -> List[Dict]:
        """Validate and enhance issues format with additional fields"""
        valid_issues = []
        
        for issue in issues:
            if isinstance(issue, dict):
                validated_issue = {
                    "type": issue.get("type", "Quality"),
                    "severity": issue.get("severity", "Medium"),
                    "title": issue.get("title", "Issue detected"),
                    "description": str(issue.get("description", "No description provided")),
                    "line": issue.get("line"),
                    "code": issue.get("code"),
                    "recommendation": issue.get("recommendation", "")
                }
                
                # Validate severity
                if validated_issue["severity"] not in ["Low", "Medium", "High", "Critical"]:
                    validated_issue["severity"] = "Medium"
                
                # Validate type
                if validated_issue["type"] not in ["Quality", "Security", "Performance"]:
                    validated_issue["type"] = "Quality"
                
                valid_issues.append(validated_issue)
        
        return valid_issues
    
    def _generate_issue_statistics(self, issues: List[Dict]) -> Dict[str, Any]:
        """Generate statistics about issues"""
        if not issues:
            return {
                "total": 0,
                "by_severity": {},
                "by_type": {}
            }
        
        by_severity = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
        by_type = {"Quality": 0, "Security": 0, "Performance": 0}
        
        for issue in issues:
            by_severity[issue["severity"]] = by_severity.get(issue["severity"], 0) + 1
            by_type[issue["type"]] = by_type.get(issue["type"], 0) + 1
        
        return {
            "total": len(issues),
            "by_severity": by_severity,
            "by_type": by_type
        }
    
    def batch_analyze(self, files: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Analyze multiple files in batch"""
        results = []
        for file_info in files:
            result = self.analyze_code(
                code=file_info['content'],
                filename=file_info['filename']
            )
            result['filename'] = file_info['filename']
            results.append(result)
        return results
    
    def clear_cache(self):
        """Clear the analysis cache"""
        self.cache.clear()
    
    def _create_error_result(self, error_message: str) -> Dict[str, Any]:
        """Create an error result when analysis fails"""
        return {
            "overall_score": 0,
            "scores": {
                "Quality": 0,
                "Security": 0,
                "Performance": 0
            },
            "issues": [
                {
                    "type": "Quality",
                    "severity": "High",
                    "description": f"Analysis failed: {error_message}",
                    "line": None,
                    "code": None
                }
            ],
            "recommendations": [
                "Please check your code syntax and try again",
                "Ensure your OpenAI API key is valid and has sufficient credits"
            ],
            "summary": f"Analysis failed due to: {error_message}"
        }