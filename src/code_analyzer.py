import json
import re
from typing import Dict, List, Any, Optional
from openai import OpenAI
from src.config import Config

class CodeAnalyzer:
    """AI-powered code analyzer using OpenAI GPT models"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key=config.api_key)
        
    def analyze_code(
        self,
        code: str,
        filename: str = "code.py",
        include_security: bool = True,
        include_performance: bool = True,
        include_style: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze code for quality, security, and performance issues
        
        Args:
            code: The source code to analyze
            filename: Name of the file being analyzed
            include_security: Whether to include security analysis
            include_performance: Whether to include performance analysis
            include_style: Whether to include style analysis
            
        Returns:
            Dictionary containing analysis results
        """
        
        # Determine programming language
        language = self.config.get_file_extension_language(filename) or "python"
        
        # Build analysis prompt
        prompt = self._build_analysis_prompt(
            code, language, filename,
            include_security, include_performance, include_style
        )
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
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
            
            # Parse response
            result_text = response.choices[0].message.content
            analysis_result = json.loads(result_text)
            
            # Post-process and validate results
            processed_result = self._process_analysis_result(analysis_result)
            
            return processed_result
            
        except json.JSONDecodeError as e:
            return self._create_error_result(f"Failed to parse AI response: {str(e)}")
        except Exception as e:
            return self._create_error_result(f"Analysis failed: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI model"""
        return """You are an expert code reviewer and security analyst. Your job is to analyze code for:

1. CODE QUALITY: Readability, maintainability, best practices, design patterns
2. SECURITY: Vulnerabilities, unsafe practices, potential exploits
3. PERFORMANCE: Efficiency, optimization opportunities, resource usage

You must respond with a valid JSON object containing:
{
    "overall_score": <number 1-10>,
    "scores": {
        "Quality": <number 1-10>,
        "Security": <number 1-10>,
        "Performance": <number 1-10>
    },
    "issues": [
        {
            "type": "Quality|Security|Performance",
            "severity": "Low|Medium|High|Critical",
            "description": "Clear description of the issue",
            "line": <line number or null>,
            "code": "problematic code snippet or null"
        }
    ],
    "recommendations": [
        "Specific actionable recommendation"
    ],
    "summary": "Brief summary of the analysis"
}

Be thorough but constructive. Focus on actionable feedback."""

    def _build_analysis_prompt(
        self,
        code: str,
        language: str,
        filename: str,
        include_security: bool,
        include_performance: bool,
        include_style: bool
    ) -> str:
        """Build the analysis prompt for the AI model"""
        
        analysis_aspects = []
        if include_style:
            analysis_aspects.append("code quality and style")
        if include_security:
            analysis_aspects.append("security vulnerabilities")
        if include_performance:
            analysis_aspects.append("performance optimization")
        
        aspects_text = ", ".join(analysis_aspects)
        
        return f"""Please analyze this {language} code file ({filename}) for {aspects_text}.

Code to analyze:
```{language}
{code}
```

Focus on:
- Code quality: readability, maintainability, best practices, naming conventions
- Security: potential vulnerabilities, unsafe operations, input validation
- Performance: efficiency, algorithm complexity, resource usage
- Specific issues with line numbers when possible
- Actionable recommendations for improvement

Provide scores from 1-10 (10 being excellent) and specific, actionable feedback."""

    def _process_analysis_result(self, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process and validate the raw analysis result"""
        
        # Ensure required fields exist
        processed = {
            "overall_score": raw_result.get("overall_score", 5),
            "scores": raw_result.get("scores", {}),
            "issues": raw_result.get("issues", []),
            "recommendations": raw_result.get("recommendations", []),
            "summary": raw_result.get("summary", "Analysis completed")
        }
        
        # Validate and normalize scores
        processed["scores"] = self._normalize_scores(processed["scores"])
        
        # Calculate overall score if not provided
        if not processed["overall_score"] or processed["overall_score"] == 5:
            scores = processed["scores"]
            weights = self.config.score_weights
            processed["overall_score"] = round(
                scores.get("Quality", 5) * weights["quality"] +
                scores.get("Security", 5) * weights["security"] +
                scores.get("Performance", 5) * weights["performance"],
                1
            )
        
        # Validate issues format
        processed["issues"] = self._validate_issues(processed["issues"])
        
        # Ensure recommendations is a list
        if isinstance(processed["recommendations"], str):
            processed["recommendations"] = [processed["recommendations"]]
        
        return processed
    
    def _normalize_scores(self, scores: Dict[str, Any]) -> Dict[str, int]:
        """Normalize and validate scores"""
        normalized = {
            "Quality": 5,
            "Security": 5,
            "Performance": 5
        }
        
        for key, value in scores.items():
            if isinstance(value, (int, float)):
                normalized[key] = max(1, min(10, int(round(value))))
        
        return normalized
    
    def _validate_issues(self, issues: List[Dict]) -> List[Dict]:
        """Validate and normalize issues format"""
        valid_issues = []
        
        for issue in issues:
            if isinstance(issue, dict):
                validated_issue = {
                    "type": issue.get("type", "Quality"),
                    "severity": issue.get("severity", "Medium"),
                    "description": str(issue.get("description", "No description provided")),
                    "line": issue.get("line"),
                    "code": issue.get("code")
                }
                
                # Validate severity
                if validated_issue["severity"] not in ["Low", "Medium", "High", "Critical"]:
                    validated_issue["severity"] = "Medium"
                
                # Validate type
                if validated_issue["type"] not in ["Quality", "Security", "Performance"]:
                    validated_issue["type"] = "Quality"
                
                valid_issues.append(validated_issue)
        
        return valid_issues
    
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

class AnalysisHistory:
    """Class to manage analysis history and statistics"""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
    
    def add_analysis(self, filename: str, results: Dict[str, Any]) -> None:
        """Add an analysis result to history"""
        self.history.append({
            "timestamp": self._get_timestamp(),
            "filename": filename,
            "results": results
        })
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics from analysis history"""
        if not self.history:
            return {"total_analyses": 0}
        
        total = len(self.history)
        avg_score = sum(r["results"]["overall_score"] for r in self.history) / total
        
        return {
            "total_analyses": total,
            "average_score": round(avg_score, 1),
            "latest_analysis": self.history[-1]["timestamp"]
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()