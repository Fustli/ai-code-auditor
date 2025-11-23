"""
UI Components and styling utilities for AI Code Auditor
"""
import streamlit as st
from typing import Dict, Any, Optional

class ThemeManager:
    """Manages dark/light theme styling"""
    
    DARK_THEME = {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'background': '#1a1a2e',
        'surface': '#16213e',
        'card': '#0f3460',
        'text': '#e4e4e4',
        'text_secondary': '#b0b0b0',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'info': '#3b82f6',
        'border': '#334155',
        'hover': '#1e293b'
    }
    
    LIGHT_THEME = {
        'primary': '#667eea',
        'secondary': '#764ba2',
        'background': '#f8fafc',
        'surface': '#ffffff',
        'card': '#f1f5f9',
        'text': '#1e293b',
        'text_secondary': '#64748b',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'info': '#3b82f6',
        'border': '#e2e8f0',
        'hover': '#f1f5f9'
    }
    
    @staticmethod
    def get_theme(dark_mode: bool = False) -> Dict[str, str]:
        """Get theme colors based on mode"""
        return ThemeManager.DARK_THEME if dark_mode else ThemeManager.LIGHT_THEME
    
    @staticmethod
    def get_css(dark_mode: bool = False) -> str:
        """Generate CSS for the current theme"""
        theme = ThemeManager.get_theme(dark_mode)
        
        return f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Global Styles */
            .stApp {{
                font-family: 'Inter', sans-serif;
                background: {theme['background']};
                color: {theme['text']};
            }}
            
            /* Override Streamlit default text colors */
            .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, span, div, label, li, ul, ol {{
                color: {theme['text']} !important;
            }}
            
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
                color: {theme['text']} !important;
            }}
            
            /* Input fields */
            input, textarea, select {{
                background-color: {theme['surface']} !important;
                color: {theme['text']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            /* Override Streamlit's input backgrounds */
            input[type="text"],
            input[type="password"],
            input[type="number"],
            input[type="email"],
            textarea {{
                background-color: {theme['surface']} !important;
                color: {theme['text']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            /* Force all input wrapper divs to use theme background */
            .stTextInput > div,
            .stTextInput > div > div,
            .stNumberInput > div,
            .stNumberInput > div > div,
            .stTextArea > div,
            .stTextArea > div > div {{
                background-color: transparent !important;
            }}
            
            /* Selectbox, multiselect */
            [data-baseweb="select"] {{
                background-color: {theme['surface']} !important;
                color: {theme['text']} !important;
            }}
            
            [data-baseweb="select"] * {{
                color: {theme['text']} !important;
                background-color: {theme['surface']} !important;
            }}
            
            [data-baseweb="select"] > div {{
                background-color: {theme['surface']} !important;
            }}
            
            /* Text input */
            .stTextInput input {{
                background-color: {theme['surface']} !important;
                color: {theme['text']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            .stTextInput > div > div {{
                background-color: {theme['surface']} !important;
            }}
            
            .stTextInput input:focus {{
                border-color: {theme['primary']} !important;
                box-shadow: 0 0 0 1px {theme['primary']} !important;
            }}
            
            /* Text area */
            .stTextArea textarea {{
                background-color: {theme['surface']} !important;
                color: {theme['text']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            .stTextArea > div > div {{
                background-color: {theme['surface']} !important;
            }}
            
            .stTextArea textarea:focus {{
                border-color: {theme['primary']} !important;
                box-shadow: 0 0 0 1px {theme['primary']} !important;
            }}
            
            /* Number input */
            .stNumberInput input {{
                background-color: {theme['surface']} !important;
                color: {theme['text']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            .stNumberInput > div > div {{
                background-color: {theme['surface']} !important;
            }}
            
            /* Selectbox dropdown */
            [data-baseweb="popover"] {{
                background-color: {theme['surface']} !important;
            }}
            
            [data-baseweb="popover"] * {{
                background-color: {theme['surface']} !important;
            }}
            
            [data-baseweb="menu"] {{
                background-color: {theme['surface']} !important;
            }}
            
            [data-baseweb="menu"] li {{
                background-color: {theme['surface']} !important;
                color: {theme['text']} !important;
            }}
            
            [data-baseweb="menu"] li:hover {{
                background-color: {theme['hover']} !important;
            }}
            
            /* Checkbox */
            .stCheckbox {{
                color: {theme['text']} !important;
            }}
            
            .stCheckbox label {{
                color: {theme['text']} !important;
            }}
            
            .stCheckbox > label > div {{
                background-color: {theme['surface']} !important;
            }}
            
            .stCheckbox span {{
                color: {theme['text']} !important;
            }}
            
            /* Checkbox input box */
            .stCheckbox input[type="checkbox"] {{
                background-color: {theme['surface']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            .stCheckbox label {{
                color: {theme['text']} !important;
            }}
            
            .stCheckbox > label > div {{
                background-color: {theme['surface']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            .stCheckbox input:checked ~ div {{
                background-color: {theme['primary']} !important;
            }}
            
            /* Sidebar checkboxes specifically */
            [data-testid="stSidebar"] .stCheckbox {{
                color: {theme['text']} !important;
            }}
            
            [data-testid="stSidebar"] .stCheckbox label {{
                color: {theme['text']} !important;
            }}
            
            [data-testid="stSidebar"] .stCheckbox span {{
                color: {theme['text']} !important;
            }}
            
            [data-testid="stSidebar"] .stCheckbox > label > div {{
                background-color: {theme['surface']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            /* Radio */
            .stRadio {{
                color: {theme['text']} !important;
            }}
            
            .stRadio label {{
                color: {theme['text']} !important;
            }}
            
            .stRadio > label > div {{
                background-color: {theme['surface']} !important;
            }}
            
            .stRadio span {{
                color: {theme['text']} !important;
            }}
            
            /* Success/Info/Warning/Error boxes */
            .stAlert {{
                color: {theme['text']} !important;
            }}
            
            /* Main Header */
            .main-header {{
                background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
                padding: 2.5rem;
                border-radius: 16px;
                color: white !important;
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                animation: slideDown 0.5s ease-out;
            }}
            
            .main-header h1 {{
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
                color: white !important;
            }}
            
            .main-header p {{
                font-size: 1.1rem;
                opacity: 0.95;
                font-weight: 300;
                color: white !important;
            }}
            
            /* Cards */
            .metric-card {{
                background: {theme['card']};
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 4px solid {theme['primary']};
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
                color: {theme['text']};
            }}
            
            .metric-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 15px rgba(0,0,0,0.15);
            }}
            
            .analysis-section {{
                background: {theme['surface']};
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                margin-bottom: 2rem;
                border: 1px solid {theme['border']};
                animation: fadeIn 0.5s ease-in;
                color: {theme['text']};
            }}
            
            /* Score Badges */
            .score-badge {{
                display: inline-block;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-weight: 600;
                font-size: 1.1rem;
                margin: 0.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            
            .score-excellent {{ 
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white !important;
            }}
            
            .score-good {{ 
                background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                color: white !important;
            }}
            
            .score-fair {{ 
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white !important;
            }}
            
            .score-poor {{ 
                background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                color: white !important;
            }}
            
            /* Buttons */
            .stButton>button {{
                background: linear-gradient(135deg, {theme['primary']} 0%, {theme['secondary']} 100%);
                color: white !important;
                border: none;
                border-radius: 10px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
            }}
            
            .stButton>button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }}
            
            /* Progress bars */
            .stProgress > div > div {{
                background: linear-gradient(90deg, {theme['primary']}, {theme['secondary']});
                border-radius: 10px;
            }}
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 1rem;
                background: {theme['surface']};
                padding: 0.5rem;
                border-radius: 10px;
            }}
            
            .stTabs [data-baseweb="tab"] {{
                border-radius: 8px;
                padding: 0.75rem 1.5rem;
                font-weight: 600;
                transition: all 0.3s;
                color: {theme['text']} !important;
            }}
            
            .stTabs [aria-selected="true"] {{
                background: linear-gradient(135deg, {theme['primary']}, {theme['secondary']});
                color: white !important;
            }}
            
            /* Expander */
            .streamlit-expanderHeader {{
                background: {theme['card']};
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.2s;
                color: {theme['text']} !important;
            }}
            
            .streamlit-expanderHeader:hover {{
                background: {theme['hover']};
            }}
            
            .streamlit-expanderContent {{
                color: {theme['text']} !important;
            }}
            
            /* Sidebar */
            .css-1d391kg, [data-testid="stSidebar"] {{
                background: {theme['surface']};
                border-right: 1px solid {theme['border']};
            }}
            
            [data-testid="stSidebar"] * {{
                color: {theme['text']} !important;
            }}
            
            [data-testid="stSidebar"] .stMarkdown {{
                color: {theme['text']} !important;
            }}
            
            /* File uploader */
            .stFileUploader {{
                background-color: {theme['surface']} !important;
                border-radius: 12px;
                padding: 1.5rem;
                border: 2px dashed {theme['border']};
                transition: all 0.3s;
                color: {theme['text']} !important;
            }}
            
            .stFileUploader * {{
                color: {theme['text']} !important;
            }}
            
            .stFileUploader section {{
                background-color: {theme['surface']} !important;
            }}
            
            .stFileUploader > div {{
                background-color: {theme['surface']} !important;
            }}
            
            .stFileUploader [data-testid="stFileUploadDropzone"] {{
                background-color: {theme['surface']} !important;
                color: {theme['text']} !important;
            }}
            
            .stFileUploader button {{
                background-color: {theme['card']} !important;
                color: {theme['text']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            .stFileUploader label {{
                color: {theme['text']} !important;
            }}
            
            .stFileUploader:hover {{
                border-color: {theme['primary']};
                background-color: {theme['hover']} !important;
            }}
            
            /* Metrics */
            [data-testid="stMetricValue"] {{
                font-size: 2rem;
                font-weight: 700;
                color: {theme['primary']};
            }}
            
            [data-testid="stMetricLabel"] {{
                color: {theme['text']} !important;
            }}
            
            [data-testid="stMetricDelta"] {{
                color: {theme['text']} !important;
            }}
            
            /* Animations */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @keyframes slideDown {{
                from {{ opacity: 0; transform: translateY(-20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; }}
                50% {{ opacity: 0.8; }}
            }}
            
            /* Loading spinner */
            .loading-spinner {{
                animation: pulse 2s ease-in-out infinite;
            }}
            
            /* Code blocks */
            .stCodeBlock {{
                border-radius: 10px;
                border: 1px solid {theme['border']};
                background: {theme['surface']} !important;
            }}
            
            .stCodeBlock code {{
                color: {theme['text']} !important;
            }}
            
            /* DataFrames */
            .stDataFrame {{
                color: {theme['text']} !important;
            }}
            
            .stDataFrame table {{
                color: {theme['text']} !important;
            }}
            
            /* Info boxes */
            .stAlert {{
                border-radius: 10px;
                border-left: 4px solid;
                background: {theme['card']} !important;
                color: {theme['text']} !important;
            }}
            
            .stAlert * {{
                color: {theme['text']} !important;
            }}
            
            /* Toggle/Switch components */
            [data-testid="stToggle"] {{
                color: {theme['text']} !important;
            }}
            
            [data-testid="stToggle"] label {{
                color: {theme['text']} !important;
            }}
            
            [data-testid="stToggle"] span {{
                color: {theme['text']} !important;
            }}
            
            /* Dark mode toggle */
            .theme-toggle {{
                position: fixed;
                top: 1rem;
                right: 1rem;
                z-index: 999;
                background-color: {theme['surface']} !important;
                border-radius: 25px;
                padding: 0.5rem 1rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                border: 1px solid {theme['border']};
                color: {theme['text']} !important;
            }}
            
            .theme-toggle button {{
                background-color: {theme['card']} !important;
                color: {theme['text']} !important;
                border: 1px solid {theme['border']} !important;
            }}
            
            .theme-toggle * {{
                color: {theme['text']} !important;
            }}
            
            /* Feature cards */
            .feature-card {{
                background: {theme['card']};
                padding: 1.5rem;
                border-radius: 12px;
                border: 1px solid {theme['border']};
                transition: all 0.3s;
                cursor: pointer;
                color: {theme['text']};
            }}
            
            .feature-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
                border-color: {theme['primary']};
            }}
            
            /* Stats display */
            .stats-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin: 1rem 0;
            }}
            
            .stat-box {{
                background: {theme['card']};
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                border: 1px solid {theme['border']};
                color: {theme['text']};
            }}
            
            .stat-number {{
                font-size: 2.5rem;
                font-weight: 700;
                color: {theme['primary']};
                margin-bottom: 0.5rem;
            }}
            
            .stat-label {{
                color: {theme['text_secondary']};
                font-size: 0.9rem;
                font-weight: 500;
            }}
            
            /* Issue severity badges */
            .severity-critical {{
                background: {theme['error']};
                color: white !important;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.85rem;
            }}
            
            .severity-high {{
                background: {theme['warning']};
                color: white !important;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.85rem;
            }}
            
            .severity-medium {{
                background: {theme['info']};
                color: white !important;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.85rem;
            }}
            
            .severity-low {{
                background: {theme['success']};
                color: white !important;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.85rem;
            }}
        </style>
        """

def render_header(dark_mode: bool = False):
    """Render the main application header"""
    st.markdown(f"""
    <div class="main-header">
        <h1>🧠 AI Code Auditor</h1>
        <p>Professional AI-powered code analysis for quality, security, and performance</p>
    </div>
    """, unsafe_allow_html=True)

def render_score_badge(score: float, label: str = "") -> str:
    """Generate HTML for a score badge"""
    if score >= 8:
        css_class = "score-excellent"
        emoji = "🟢"
    elif score >= 6:
        css_class = "score-good"
        emoji = "🔵"
    elif score >= 4:
        css_class = "score-fair"
        emoji = "🟡"
    else:
        css_class = "score-poor"
        emoji = "🔴"
    
    return f'<span class="score-badge {css_class}">{emoji} {label} {score:.1f}/10</span>'

def render_severity_badge(severity: str) -> str:
    """Generate HTML for severity badge"""
    severity_lower = severity.lower()
    return f'<span class="severity-{severity_lower}">{severity.upper()}</span>'

def render_feature_card(icon: str, title: str, description: str):
    """Render a feature card"""
    st.markdown(f"""
    <div class="feature-card">
        <h3 style="margin-bottom: 0.5rem;">{icon} {title}</h3>
        <p style="color: var(--text-secondary); margin: 0;">{description}</p>
    </div>
    """, unsafe_allow_html=True)

def render_stats(stats: Dict[str, Any]):
    """Render statistics dashboard"""
    html = '<div class="stats-container">'
    for key, value in stats.items():
        html += f"""
        <div class="stat-box">
            <div class="stat-number">{value}</div>
            <div class="stat-label">{key}</div>
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def show_loading_animation(message: str = "Analyzing code..."):
    """Display a loading animation"""
    return st.spinner(f"🧠 {message}")

def render_footer():
    """Render application footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: var(--text-secondary);">
        <p style="margin-bottom: 0.5rem;">
            🧠 <strong>AI Code Auditor</strong> - Powered by OpenAI GPT-4o
        </p>
        <p style="font-size: 0.9rem; margin: 0;">
            Made with ❤️ using Streamlit | 
            <a href="https://github.com/Fustli/ai-code-auditor" target="_blank" style="color: var(--primary); text-decoration: none;">
                GitHub
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)