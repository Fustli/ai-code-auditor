import streamlit as st
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from streamlit_ace import st_ace
from src.config import Config
from src.code_analyzer import CodeAnalyzer

# Page config
st.set_page_config(
    page_title="🧠 AI Code Auditor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .analysis-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .score-excellent { color: #28a745; font-weight: bold; }
    .score-good { color: #17a2b8; font-weight: bold; }
    .score-fair { color: #ffc107; font-weight: bold; }
    .score-poor { color: #dc3545; font-weight: bold; }
    
    .stProgress .st-bo {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

def get_score_class(score):
    """Get CSS class based on score"""
    if score >= 8: return "score-excellent"
    elif score >= 6: return "score-good"
    elif score >= 4: return "score-fair"
    else: return "score-poor"

def create_score_chart(scores):
    """Create a radar chart for scores"""
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Scores',
        line_color='rgb(102, 126, 234)',
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False,
        height=400,
        title="Code Quality Scores"
    )
    
    return fig

def display_analysis_results(results):
    """Display analysis results in a beautiful format"""
    st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
    
    # Overall score
    overall_score = results['overall_score']
    st.markdown(f"### 🎯 Overall Score: <span class='{get_score_class(overall_score)}'>{overall_score}/10</span>", unsafe_allow_html=True)
    
    # Progress bar for overall score
    st.progress(overall_score / 10)
    
    # Score breakdown
    col1, col2, col3 = st.columns(3)
    
    with col1:
        quality_score = results['scores']['Quality']
        st.metric("📊 Code Quality", f"{quality_score}/10", 
                 delta=f"{quality_score - 6:.1f}" if quality_score > 6 else f"{quality_score - 6:.1f}")
    
    with col2:
        security_score = results['scores']['Security']
        st.metric("🔒 Security", f"{security_score}/10",
                 delta=f"{security_score - 7:.1f}" if security_score > 7 else f"{security_score - 7:.1f}")
    
    with col3:
        performance_score = results['scores']['Performance']
        st.metric("⚡ Performance", f"{performance_score}/10",
                 delta=f"{performance_score - 6:.1f}" if performance_score > 6 else f"{performance_score - 6:.1f}")
    
    # Radar chart
    st.plotly_chart(create_score_chart(results['scores']), use_container_width=True)
    
    # Detailed analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔍 Issues Found")
        if results['issues']:
            for i, issue in enumerate(results['issues'], 1):
                with st.expander(f"Issue {i}: {issue['type']} - {issue['severity']}"):
                    st.write(f"**Description:** {issue['description']}")
                    st.write(f"**Line:** {issue.get('line', 'N/A')}")
                    if issue.get('code'):
                        st.code(issue['code'], language='python')
        else:
            st.success("🎉 No issues found!")
    
    with col2:
        st.markdown("### 💡 Recommendations")
        if results['recommendations']:
            for i, rec in enumerate(results['recommendations'], 1):
                st.markdown(f"**{i}.** {rec}")
        else:
            st.info("No specific recommendations at this time.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧠 AI Code Auditor</h1>
        <p>Upload your code and get instant AI-powered quality, security, and performance analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input("🔑 OpenAI API Key", type="password", help="Enter your OpenAI API key")
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.success("✅ API Key set!")
        else:
            st.warning("⚠️ Please enter your OpenAI API key")
        
        st.markdown("---")
        
        # Analysis options
        st.markdown("### 🎯 Analysis Options")
        include_security = st.checkbox("🔒 Security Analysis", value=True)
        include_performance = st.checkbox("⚡ Performance Analysis", value=True)
        include_style = st.checkbox("🎨 Style Analysis", value=True)
        
        st.markdown("---")
        
        # Model selection
        model = st.selectbox("🤖 AI Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"])
        
        st.markdown("---")
        
        # History
        if st.session_state.analysis_history:
            st.markdown("### 📊 Analysis History")
            for i, analysis in enumerate(reversed(st.session_state.analysis_history[-5:])):
                st.write(f"{i+1}. {analysis['timestamp']}: {analysis['overall_score']}/10")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📁 Upload Code", "✏️ Code Editor", "📊 Analysis Results"])
    
    with tab1:
        st.markdown("### 📁 Upload Code Files")
        uploaded_files = st.file_uploader(
            "Choose code files to analyze",
            accept_multiple_files=True,
            type=['py', 'js', 'ts', 'java', 'cpp', 'c', 'go', 'rs', 'php', 'rb']
        )
        
        if uploaded_files:
            for file in uploaded_files:
                st.write(f"📄 **{file.name}** ({file.size} bytes)")
                
                # Show file content
                content = file.read().decode('utf-8')
                st.code(content, language='python')
                
                # Analyze button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button(f"🔍 Analyze {file.name}", key=f"analyze_{file.name}", use_container_width=True):
                        if api_key:
                            with st.spinner("🧠 AI is analyzing your code..."):
                                try:
                                    config = Config(api_key=api_key, model=model)
                                    analyzer = CodeAnalyzer(config)
                                    
                                    results = analyzer.analyze_code(
                                        content, 
                                        filename=file.name,
                                        include_security=include_security,
                                        include_performance=include_performance,
                                        include_style=include_style
                                    )
                                    
                                    # Store results
                                    st.session_state.analysis_results = results
                                    st.session_state.analysis_history.append({
                                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        'filename': file.name,
                                        'overall_score': results['overall_score']
                                    })
                                    
                                    st.success("✅ Analysis complete! Check the 'Analysis Results' tab.")
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"❌ Analysis failed: {str(e)}")
                        else:
                            st.error("❌ Please enter your OpenAI API key in the sidebar first!")
    
    with tab2:
        st.markdown("### ✏️ Code Editor")
        st.info("💡 Paste your code below or start typing to analyze it directly")
        
        # Code editor
        code_content = st_ace(
            placeholder="Paste your code here...",
            language='python',
            theme='monokai',
            height=400,
            auto_update=True,
            font_size=14,
            key="code_editor"
        )
        
        if code_content:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔍 Analyze Code", use_container_width=True):
                    if api_key:
                        with st.spinner("🧠 AI is analyzing your code..."):
                            try:
                                config = Config(api_key=api_key, model=model)
                                analyzer = CodeAnalyzer(config)
                                
                                results = analyzer.analyze_code(
                                    code_content,
                                    filename="editor.py",
                                    include_security=include_security,
                                    include_performance=include_performance,
                                    include_style=include_style
                                )
                                
                                # Store results
                                st.session_state.analysis_results = results
                                st.session_state.analysis_history.append({
                                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    'filename': 'Code Editor',
                                    'overall_score': results['overall_score']
                                })
                                
                                st.success("✅ Analysis complete! Check the 'Analysis Results' tab.")
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Analysis failed: {str(e)}")
                    else:
                        st.error("❌ Please enter your OpenAI API key in the sidebar first!")
    
    with tab3:
        st.markdown("### 📊 Analysis Results")
        
        if st.session_state.analysis_results:
            display_analysis_results(st.session_state.analysis_results)
            
            # Export results
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📥 Export Results", use_container_width=True):
                    # Create downloadable report
                    report = f"""
# AI Code Audit Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Overall Score:** {st.session_state.analysis_results['overall_score']}/10

## Scores
- Quality: {st.session_state.analysis_results['scores']['Quality']}/10
- Security: {st.session_state.analysis_results['scores']['Security']}/10
- Performance: {st.session_state.analysis_results['scores']['Performance']}/10

## Issues Found
{chr(10).join([f"- {issue['type']}: {issue['description']}" for issue in st.session_state.analysis_results['issues']])}

## Recommendations
{chr(10).join([f"- {rec}" for rec in st.session_state.analysis_results['recommendations']])}
"""
                    
                    st.download_button(
                        label="📄 Download Report",
                        data=report,
                        file_name=f"code_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
        else:
            st.info("🔍 No analysis results yet. Upload a file or paste code to get started!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        🧠 AI Code Auditor - Powered by OpenAI GPT-4o | Made with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()