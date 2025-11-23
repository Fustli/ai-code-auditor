"""
AI Code Auditor - Enhanced Main Application
Professional AI-powered code analysis with dark mode and advanced features
"""
import streamlit as st
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from streamlit_ace import st_ace
import pandas as pd
import json

from src.config import Config
from src.code_analyzer import CodeAnalyzer
from src.ui_components import (
    ThemeManager, render_header, render_score_badge, 
    render_severity_badge, render_stats, render_footer, show_loading_animation
)
from src.utils import (
    AnalysisHistory, CodeMetrics, calculate_overall_grade,
    ComparisonEngine, CodeFormatter
)

# Page configuration
st.set_page_config(
    page_title="🧠 AI Code Auditor Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Fustli/ai-code-auditor',
        'Report a bug': 'https://github.com/Fustli/ai-code-auditor/issues',
        'About': '# AI Code Auditor\nProfessional AI-powered code analysis'
    }
)

def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'analysis_results': None,
        'analysis_history': AnalysisHistory(),
        'dark_mode': True,
        'comparison_mode': False,
        'previous_analysis': None,
        'batch_results': [],
        'chat_history': [],
        'selected_file': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def render_sidebar():
    """Render enhanced sidebar with all configuration options"""
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        
        # Dark mode toggle
        dark_mode = st.toggle(
            "🌙 Dark Mode", 
            value=st.session_state.dark_mode,
            help="Toggle between dark and light themes"
        )
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        st.markdown("---")
        
        # API Configuration
        st.markdown("### 🔑 API Configuration")
        
        # API Provider Selection
        api_provider = st.selectbox(
            "AI Provider",
            ["OpenAI", "Google Gemini"],
            help="Choose your AI API provider"
        )
        
        # Map display name to internal key
        provider_map = {
            "openai": "openai",
            "google gemini": "gemini"
        }
        provider_key = provider_map[api_provider.lower()]
        
        if provider_key == "openai":
            api_key = st.text_input(
                "OpenAI API Key", 
                type="password", 
                help="Get from: https://platform.openai.com/api-keys",
                label_visibility="collapsed",
                placeholder="sk-..."
            )
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                os.environ["API_PROVIDER"] = "openai"
                st.success("✅ OpenAI API Key configured")
            else:
                st.warning("⚠️ API Key required")
                st.info("🔗 Get key at [platform.openai.com](https://platform.openai.com/api-keys)")
        else:  # Google Gemini
            api_key = st.text_input(
                "Gemini API Key", 
                type="password", 
                help="Get from: https://makersuite.google.com/app/apikey",
                label_visibility="collapsed",
                placeholder="AIza..."
            )
            if api_key:
                os.environ["GEMINI_API_KEY"] = api_key
                os.environ["API_PROVIDER"] = "gemini"
                st.success("✅ Gemini API Key configured")
            else:
                st.warning("⚠️ API Key required")
                st.info("🔗 Get key at [makersuite.google.com](https://makersuite.google.com/app/apikey)")
        
        st.markdown("---")
        
        # Analysis Options
        st.markdown("### 🎯 Analysis Options")
        
        col1, col2 = st.columns(2)
        with col1:
            include_security = st.checkbox("🔒 Security", value=True)
            include_style = st.checkbox("🎨 Style", value=True)
        with col2:
            include_performance = st.checkbox("⚡ Performance", value=True)
            include_metrics = st.checkbox("📊 Metrics", value=True)
        
        st.markdown("---")
        
        # Model Selection
        st.markdown("### 🤖 AI Model")
        
        if provider_key == "openai":
            model = st.selectbox(
                "Select Model",
                ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
                help="Choose the OpenAI model for analysis",
                label_visibility="collapsed"
            )
        else:  # Gemini
            model = st.selectbox(
                "Select Model",
                [
                    "models/gemini-2.0-flash",  # Latest fast model
                    "models/gemini-2.5-flash",
                    "models/gemini-2.5-pro",
                    "models/gemini-flash-latest",
                    "models/gemini-pro-latest",
                ],
                help="Choose the Gemini model for analysis (use models/ prefix for v1beta API)",
                label_visibility="collapsed"
            )
        
        st.markdown("---")
        
        # Advanced Features
        st.markdown("### 🚀 Advanced Features")
        
        comparison_mode = st.checkbox(
            "📊 Comparison Mode",
            value=st.session_state.comparison_mode,
            help="Compare with previous analysis"
        )
        st.session_state.comparison_mode = comparison_mode
        
        batch_mode = st.checkbox(
            "📁 Batch Analysis",
            help="Analyze multiple files at once"
        )
        
        export_format = st.selectbox(
            "Export Format",
            ["Markdown", "JSON", "PDF", "HTML"],
            help="Choose export format for reports"
        )
        
        st.markdown("---")
        
        # Statistics
        if st.session_state.analysis_history.history:
            st.markdown("### 📈 Statistics")
            stats = st.session_state.analysis_history.get_statistics()
            
            st.metric("Total Analyses", stats['total_analyses'])
            st.metric("Average Score", f"{stats['average_score']}/10")
            st.metric("Total Issues", stats['total_issues'])
            
            # Clear history button
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.analysis_history = AnalysisHistory()
                st.session_state.analysis_results = None
                st.rerun()
        
        return {
            'api_key': api_key,
            'model': model,
            'api_provider': provider_key,
            'include_security': include_security,
            'include_performance': include_performance,
            'include_style': include_style,
            'include_metrics': include_metrics,
            'batch_mode': batch_mode,
            'export_format': export_format
        }

def create_enhanced_score_chart(results: dict) -> go.Figure:
    """Create an enhanced radar chart with all score categories"""
    scores = results['scores']
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current',
        line_color='rgb(102, 126, 234)',
        fillcolor='rgba(102, 126, 234, 0.3)',
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(size=12),
                gridcolor='rgba(128, 128, 128, 0.2)'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, weight='bold')
            )
        ),
        showlegend=False,
        height=450,
        title={
            'text': "Code Quality Scores",
            'font': {'size': 20, 'weight': 'bold'},
            'x': 0.5,
            'xanchor': 'center'
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_issue_distribution_chart(statistics: dict) -> go.Figure:
    """Create a chart showing issue distribution"""
    by_severity = statistics['by_severity']
    
    colors = {
        'Critical': '#ef4444',
        'High': '#f59e0b',
        'Medium': '#3b82f6',
        'Low': '#10b981'
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(by_severity.keys()),
            y=list(by_severity.values()),
            marker_color=[colors[k] for k in by_severity.keys()],
            text=list(by_severity.values()),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Issues by Severity",
        xaxis_title="Severity",
        yaxis_title="Count",
        height=300,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def display_enhanced_results(results: dict):
    """Display comprehensive analysis results"""
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    
    # Overall score and grade
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        grade = results.get('grade', calculate_overall_grade(results['overall_score']))
        st.markdown(f"### Grade: **{grade}**")
        st.markdown(render_score_badge(results['overall_score'], "Overall"), unsafe_allow_html=True)
    
    with col2:
        st.metric(
            "📊 Quality",
            f"{results['scores']['Quality']}/10",
            delta=None
        )
    
    with col3:
        st.metric(
            "🔒 Security",
            f"{results['scores']['Security']}/10",
            delta=None
        )
    
    with col4:
        st.metric(
            "⚡ Performance",
            f"{results['scores']['Performance']}/10",
            delta=None
        )
    
    # Progress bar
    st.progress(results['overall_score'] / 10)
    
    # Analysis time
    if 'analysis_time' in results:
        st.caption(f"⏱️ Analysis completed in {results['analysis_time']}s")
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔍 Issues", "💡 Recommendations", "📈 Metrics"])
    
    with tab1:
        # Summary
        st.markdown("### 📝 Summary")
        st.info(results['summary'])
        
        # Strengths
        if results.get('strengths'):
            st.markdown("### ✅ Strengths")
            for strength in results['strengths']:
                st.success(f"✓ {strength}")
        
        # Radar chart
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = create_enhanced_score_chart(results)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'statistics' in results:
                st.markdown("### 📊 Issue Summary")
                stats = results['statistics']
                render_stats({
                    'Total Issues': stats['total'],
                    'Critical': stats['by_severity'].get('Critical', 0),
                    'High': stats['by_severity'].get('High', 0),
                    'Medium': stats['by_severity'].get('Medium', 0),
                    'Low': stats['by_severity'].get('Low', 0)
                })
    
    with tab2:
        st.markdown("### 🔍 Issues Found")
        
        if results['issues']:
            # Filter options
            severity_filter = st.multiselect(
                "Filter by Severity",
                ['Critical', 'High', 'Medium', 'Low'],
                default=['Critical', 'High', 'Medium', 'Low']
            )
            
            type_filter = st.multiselect(
                "Filter by Type",
                ['Security', 'Performance', 'Quality'],
                default=['Security', 'Performance', 'Quality']
            )
            
            # Use prioritized issues if available
            issues_to_display = results.get('prioritized_issues', results['issues'])
            
            filtered_issues = [
                issue for issue in issues_to_display
                if issue['severity'] in severity_filter and issue['type'] in type_filter
            ]
            
            for i, issue in enumerate(filtered_issues, 1):
                with st.expander(
                    f"Issue {i}: {issue.get('title', issue['type'])} - {render_severity_badge(issue['severity'])}",
                    expanded=(i <= 3)
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Type:** {issue['type']}")
                        st.markdown(f"**Description:** {issue['description']}")
                        
                        if issue.get('line'):
                            st.markdown(f"**Line:** {issue['line']}")
                        
                        if issue.get('code'):
                            st.code(issue['code'], language='python')
                        
                        if issue.get('recommendation'):
                            st.markdown(f"**Fix:** {issue['recommendation']}")
                    
                    with col2:
                        # Priority score if available
                        if 'priority_score' in issue:
                            st.metric("Priority", issue['priority_score'])
        else:
            st.success("🎉 No issues found! Your code looks great!")
    
    with tab3:
        st.markdown("### 💡 Recommendations")
        
        if results['recommendations']:
            for i, rec in enumerate(results['recommendations'], 1):
                st.markdown(f"**{i}.** {rec}")
        else:
            st.info("No specific recommendations at this time.")
        
        # Complexity assessment
        if results.get('complexity_assessment'):
            st.markdown("### 🧩 Complexity Assessment")
            st.write(results['complexity_assessment'])
    
    with tab4:
        if results.get('metrics'):
            st.markdown("### 📈 Code Metrics")
            metrics = results['metrics']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                render_stats({
                    'Total Lines': metrics['total_lines'],
                    'Code Lines': metrics['code_lines'],
                    'Comment Lines': metrics['comment_lines'],
                    'Blank Lines': metrics['blank_lines']
                })
            
            with col2:
                render_stats({
                    'Functions': metrics['functions'],
                    'Classes': metrics['classes'],
                    'Complexity': metrics['complexity']
                })
            
            with col3:
                render_stats({
                    'Comment Ratio': f"{metrics['comment_ratio']}%",
                    'Best Practices': f"{results.get('best_practices_score', 5)}/10"
                })
            
            # Issue distribution chart
            if 'statistics' in results:
                st.plotly_chart(
                    create_issue_distribution_chart(results['statistics']),
                    use_container_width=True
                )
        else:
            st.info("Enable metrics in the sidebar to see detailed code statistics.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def perform_analysis(code: str, filename: str, config: dict) -> dict:
    """Perform code analysis with the given configuration"""
    if not config['api_key']:
        provider_name = config.get('api_provider', 'openai').upper()
        st.error(f"❌ Please enter your {provider_name} API key in the sidebar!")
        return None
    
    with show_loading_animation("Analyzing your code..."):
        try:
            # Validate API key format based on provider
            provider = config.get('api_provider', 'openai')
            api_key = config['api_key']
            
            if provider == 'gemini' and not api_key.startswith('AIza'):
                st.error("❌ Invalid Gemini API key format. Gemini keys should start with 'AIza'")
                st.info("Get your key at: https://makersuite.google.com/app/apikey")
                return None
            elif provider == 'openai' and not api_key.startswith('sk-'):
                st.error("❌ Invalid OpenAI API key format. OpenAI keys should start with 'sk-'")
                st.info("Get your key at: https://platform.openai.com/api-keys")
                return None
            
            analyzer_config = Config(
                api_key=api_key,
                model=config['model'],
                api_provider=provider
            )
            analyzer = CodeAnalyzer(analyzer_config)
            
            results = analyzer.analyze_code(
                code,
                filename=filename,
                include_security=config['include_security'],
                include_performance=config['include_performance'],
                include_style=config['include_style'],
                include_metrics=config['include_metrics']
            )
            
            # Store in history
            st.session_state.analysis_history.add_analysis(filename, results)
            
            # Store for comparison
            if st.session_state.comparison_mode and st.session_state.analysis_results:
                st.session_state.previous_analysis = st.session_state.analysis_results
            
            st.session_state.analysis_results = results
            
            return results
            
        except ValueError as e:
            st.error(f"❌ Configuration Error: {str(e)}")
            return None
        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ Analysis failed: {error_msg}")
            
            # Provide helpful hints based on error
            if "API key not valid" in error_msg or "API_KEY_INVALID" in error_msg:
                st.warning("⚠️ **API Key Issue Detected**")
                if provider == 'gemini':
                    st.info("""
                    **Gemini API Key Checklist:**
                    1. ✓ Key starts with 'AIza'
                    2. ✓ Key copied correctly (no extra spaces)
                    3. ✓ API enabled at [Google AI Studio](https://makersuite.google.com/app/apikey)
                    4. ✓ Try creating a new API key if issue persists
                    """)
                else:
                    st.info("""
                    **OpenAI API Key Checklist:**
                    1. ✓ Key starts with 'sk-'
                    2. ✓ Key copied correctly (no extra spaces)
                    3. ✓ Account has available credits
                    4. ✓ Key has proper permissions
                    """)
            
            return None

def main():
    """Main application function"""
    initialize_session_state()
    
    # Apply theme
    st.markdown(
        ThemeManager.get_css(st.session_state.dark_mode),
        unsafe_allow_html=True
    )
    
    # Header
    render_header(st.session_state.dark_mode)
    
    # Sidebar configuration
    config = render_sidebar()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Upload Files",
        "✏️ Code Editor",
        "📊 Results",
        "📈 History & Trends"
    ])
    
    with tab1:
        st.markdown("### 📁 Upload Code Files")
        
        uploaded_files = st.file_uploader(
            "Choose code files to analyze",
            accept_multiple_files=True,
            type=['py', 'js', 'ts', 'tsx', 'jsx', 'java', 'cpp', 'c', 'go', 'rs', 'php', 'rb', 'swift', 'kt'],
            help="Upload one or more code files for analysis"
        )
        
        if uploaded_files:
            if config['batch_mode'] and len(uploaded_files) > 1:
                # Batch analysis
                st.info(f"📦 Batch mode: Analyzing {len(uploaded_files)} files...")
                
                if st.button("🔍 Analyze All Files", type="primary", use_container_width=True):
                    batch_results = []
                    
                    progress_bar = st.progress(0)
                    for i, file in enumerate(uploaded_files):
                        content = file.read().decode('utf-8')
                        result = perform_analysis(content, file.name, config)
                        if result:
                            batch_results.append({'filename': file.name, 'result': result})
                        progress_bar.progress((i + 1) / len(uploaded_files))
                    
                    st.session_state.batch_results = batch_results
                    st.success(f"✅ Analyzed {len(batch_results)} files!")
                    st.rerun()
                    
            else:
                # Single file analysis
                for file in uploaded_files:
                    with st.expander(f"📄 {file.name}", expanded=True):
                        content = file.read().decode('utf-8')
                        
                        # Show preview
                        st.code(content[:500] + ("..." if len(content) > 500 else ""), language='python')
                        st.caption(f"File size: {file.size} bytes")
                        
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if st.button(f"🔍 Analyze {file.name}", key=f"analyze_{file.name}", use_container_width=True):
                                result = perform_analysis(content, file.name, config)
                                if result:
                                    st.success("✅ Analysis complete! Check the Results tab.")
                                    st.rerun()
    
    with tab2:
        st.markdown("### ✏️ Code Editor")
        st.info("💡 Paste your code below or start typing to analyze it directly")
        
        # Language selector
        language = st.selectbox(
            "Programming Language",
            ["python", "javascript", "typescript", "java", "cpp", "go", "rust"],
            help="Select the programming language"
        )
        
        # Code editor
        code_content = st_ace(
            placeholder="Paste your code here...",
            language=language,
            theme='monokai' if st.session_state.dark_mode else 'github',
            height=450,
            auto_update=True,
            font_size=14,
            key="code_editor",
            show_gutter=True,
            show_print_margin=False,
            wrap=True
        )
        
        if code_content:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
                    result = perform_analysis(code_content, f"editor.{language}", config)
                    if result:
                        st.success("✅ Analysis complete! Check the Results tab.")
                        st.rerun()
    
    with tab3:
        st.markdown("### 📊 Analysis Results")
        
        # Show comparison if enabled
        if st.session_state.comparison_mode and st.session_state.previous_analysis and st.session_state.analysis_results:
            st.markdown("#### 📊 Comparison with Previous Analysis")
            comparison = ComparisonEngine.compare_analyses(
                st.session_state.previous_analysis,
                st.session_state.analysis_results
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                delta = comparison['score_change']
                st.metric(
                    "Score Change",
                    f"{delta:+.1f}",
                    delta=f"{delta:+.1f} points"
                )
            with col2:
                st.metric(
                    "Issues Change",
                    comparison['issues_change'],
                    delta=f"{comparison['issues_change']:+d} issues"
                )
            with col3:
                status_emoji = {"improved": "📈", "regressed": "📉", "unchanged": "➡️"}
                st.metric(
                    "Status",
                    comparison['overall_status'].title(),
                    delta=status_emoji[comparison['overall_status']]
                )
            
            st.markdown(ComparisonEngine.generate_diff_summary(comparison))
            st.markdown("---")
        
        # Display current results
        if st.session_state.analysis_results:
            display_enhanced_results(st.session_state.analysis_results)
            
            # Export options
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("📥 Export Report", use_container_width=True):
                    report_data = generate_report(
                        st.session_state.analysis_results,
                        config['export_format']
                    )
                    
                    st.download_button(
                        label=f"📄 Download {config['export_format']} Report",
                        data=report_data,
                        file_name=f"code_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{config['export_format'].lower()}",
                        mime=get_mime_type(config['export_format']),
                        use_container_width=True
                    )
            
            with col2:
                if st.button("🔄 Clear Results", use_container_width=True):
                    st.session_state.analysis_results = None
                    st.rerun()
            
            with col3:
                if st.button("💾 Save to History", use_container_width=True):
                    st.success("✅ Results saved to history!")
        
        elif st.session_state.batch_results:
            st.markdown("### 📦 Batch Analysis Results")
            
            # Summary statistics
            avg_score = sum(r['result']['overall_score'] for r in st.session_state.batch_results) / len(st.session_state.batch_results)
            total_issues = sum(len(r['result']['issues']) for r in st.session_state.batch_results)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Files Analyzed", len(st.session_state.batch_results))
            with col2:
                st.metric("Average Score", f"{avg_score:.1f}/10")
            with col3:
                st.metric("Total Issues", total_issues)
            
            st.markdown("---")
            
            # Individual results
            for batch_result in st.session_state.batch_results:
                with st.expander(f"📄 {batch_result['filename']} - Score: {batch_result['result']['overall_score']}/10"):
                    display_enhanced_results(batch_result['result'])
        
        else:
            st.info("🔍 No analysis results yet. Upload a file or paste code to get started!")
    
    with tab4:
        st.markdown("### 📈 Analysis History & Trends")
        
        if st.session_state.analysis_history.history:
            stats = st.session_state.analysis_history.get_statistics()
            
            # Statistics overview
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Analyses", stats['total_analyses'])
            with col2:
                st.metric("Average Score", f"{stats['average_score']}/10")
            with col3:
                st.metric("Total Issues", stats['total_issues'])
            with col4:
                st.metric("Latest", datetime.fromisoformat(stats['latest_analysis']).strftime('%H:%M'))
            
            # Score distribution
            st.markdown("#### 📊 Score Distribution")
            dist = stats['distribution']
            
            fig = go.Figure(data=[
                go.Bar(
                    x=['Excellent (8-10)', 'Good (6-8)', 'Fair (4-6)', 'Poor (0-4)'],
                    y=[dist['excellent'], dist['good'], dist['fair'], dist['poor']],
                    marker_color=['#10b981', '#3b82f6', '#f59e0b', '#ef4444']
                )
            ])
            
            fig.update_layout(
                title="Analysis Results Distribution",
                xaxis_title="Score Range",
                yaxis_title="Count",
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Trend chart
            trend_data = st.session_state.analysis_history.get_trend_data()
            if len(trend_data) > 1:
                st.markdown("#### 📈 Score Trend")
                
                df = pd.DataFrame(trend_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                fig = px.line(
                    df,
                    x='timestamp',
                    y='score',
                    markers=True,
                    title='Code Quality Over Time'
                )
                
                fig.update_layout(
                    xaxis_title="Time",
                    yaxis_title="Score",
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Export history
            if st.button("📥 Export History", use_container_width=True):
                history_json = st.session_state.analysis_history.export_to_json()
                st.download_button(
                    label="📄 Download History (JSON)",
                    data=history_json,
                    file_name=f"analysis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("📊 No history yet. Start analyzing code to build your history!")
    
    # Footer
    render_footer()

def generate_report(results: dict, format: str) -> str:
    """Generate analysis report in specified format"""
    if format == "Markdown":
        return generate_markdown_report(results)
    elif format == "JSON":
        return json.dumps(results, indent=2)
    elif format == "HTML":
        return generate_html_report(results)
    else:
        return generate_markdown_report(results)

def generate_markdown_report(results: dict) -> str:
    """Generate markdown report"""
    report = f"""# AI Code Audit Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Overall Score:** {results['overall_score']}/10
**Grade:** {results.get('grade', 'N/A')}

## Summary
{results['summary']}

## Scores
- **Quality:** {results['scores']['Quality']}/10
- **Security:** {results['scores']['Security']}/10
- **Performance:** {results['scores']['Performance']}/10
- **Maintainability:** {results['scores'].get('Maintainability', 'N/A')}/10

## Strengths
"""
    
    for strength in results.get('strengths', []):
        report += f"- {strength}\n"
    
    report += "\n## Issues Found\n"
    for i, issue in enumerate(results['issues'], 1):
        report += f"\n### Issue {i}: {issue.get('title', issue['type'])}\n"
        report += f"- **Type:** {issue['type']}\n"
        report += f"- **Severity:** {issue['severity']}\n"
        report += f"- **Description:** {issue['description']}\n"
        if issue.get('line'):
            report += f"- **Line:** {issue['line']}\n"
        if issue.get('recommendation'):
            report += f"- **Fix:** {issue['recommendation']}\n"
    
    report += "\n## Recommendations\n"
    for i, rec in enumerate(results['recommendations'], 1):
        report += f"{i}. {rec}\n"
    
    if results.get('metrics'):
        metrics = results['metrics']
        report += f"\n## Code Metrics\n"
        report += f"- Total Lines: {metrics['total_lines']}\n"
        report += f"- Code Lines: {metrics['code_lines']}\n"
        report += f"- Comment Ratio: {metrics['comment_ratio']}%\n"
        report += f"- Complexity: {metrics['complexity']}\n"
        report += f"- Functions: {metrics['functions']}\n"
        report += f"- Classes: {metrics['classes']}\n"
    
    report += "\n---\n*Generated by AI Code Auditor - Powered by OpenAI GPT-4o*\n"
    
    return report

def generate_html_report(results: dict) -> str:
    """Generate HTML report"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AI Code Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #667eea; }}
        .score {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .issue {{ background: #f5f5f5; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; }}
        .critical {{ border-left-color: #ef4444; }}
        .high {{ border-left-color: #f59e0b; }}
        .medium {{ border-left-color: #3b82f6; }}
        .low {{ border-left-color: #10b981; }}
    </style>
</head>
<body>
    <h1>🧠 AI Code Audit Report</h1>
    <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <p class="score">Overall Score: {results['overall_score']}/10</p>
    <p><strong>Grade:</strong> {results.get('grade', 'N/A')}</p>
    
    <h2>Summary</h2>
    <p>{results['summary']}</p>
    
    <h2>Issues Found ({len(results['issues'])})</h2>
"""
    
    for issue in results['issues']:
        severity_class = issue['severity'].lower()
        html += f"""
    <div class="issue {severity_class}">
        <h3>{issue.get('title', issue['type'])}</h3>
        <p><strong>Type:</strong> {issue['type']} | <strong>Severity:</strong> {issue['severity']}</p>
        <p>{issue['description']}</p>
        {f"<p><strong>Fix:</strong> {issue['recommendation']}</p>" if issue.get('recommendation') else ""}
    </div>
"""
    
    html += """
</body>
</html>
"""
    return html

def get_mime_type(format: str) -> str:
    """Get MIME type for export format"""
    mime_types = {
        'Markdown': 'text/markdown',
        'JSON': 'application/json',
        'HTML': 'text/html',
        'PDF': 'application/pdf'
    }
    return mime_types.get(format, 'text/plain')

if __name__ == "__main__":
    main()