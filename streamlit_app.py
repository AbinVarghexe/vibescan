"""
VibeScan - Streamlit Web Interface
Modern landing page with installation guide and scanner
"""
import streamlit as st
import tempfile
import os
from vibescan.parsers import parse_package_json, parse_requirements_txt
from vibescan.checkers.registry_checker import check_npm_package, check_pypi_package
from vibescan.checkers.typosquat_checker import check_typosquatting
from vibescan.scorer import calculate_risk

# Page configuration
st.set_page_config(
    page_title="VibeScan - AI Dependency Security Scanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/AbinVarghexe/vibescan',
        'Report a bug': 'https://github.com/AbinVarghexe/vibescan/issues',
        'About': "VibeScan - AI Dependency Security Scanner"
    }
)

# Custom CSS for minimal light design
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Light theme background */
    .stApp {
        background-color: #ffffff;
        color: #111111;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1000px;
    }
    
    /* Hero section styling */
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 4rem !important;
        font-weight: 800 !important;
        color: #111111 !important;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        color: #444444;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Feature cards */
    .feature-card {
        background: #ffffff;
        border: 1px solid #eeeeee;
        border-radius: 12px;
        padding: 2.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0, 0, 0, 0.06);
        border-color: #e0e0e0;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: #333;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #111;
    }
    
    .feature-desc {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* Buttons - Primary (Black) */
    .stButton > button {
        background-color: #111111 !important;
        color: #ffffff !important;
        border: none;
        border-radius: 8px;
        padding: 0.8rem 2.5rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background-color: #333333 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(0,0,0,0.15);
    }
    
    /* Top Navbar Links */
    .nav-link {
        color: #444;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        margin: 0 15px;
        transition: color 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .nav-link:hover {
        color: #000;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background: #f8f9fa !important;
        border: 1px solid #eeeeee !important;
        border-radius: 8px !important;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #e0e0e0;
        border-radius: 10px;
        padding: 2rem;
        background: #fcfcfc;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: transparent;
        border-bottom: 1px solid #eee;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #666;
        padding: 10px 0;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #111;
        border-bottom: 2px solid #111;
    }
    
    /* Section headers */
    h1, h2, h3 {
        color: #111111 !important;
        font-family: 'Inter', sans-serif;
    }
    
    h2 {
        font-weight: 700;
        text-align: center;
        margin-top: 3rem;
        margin-bottom: 2rem;
        font-size: 2rem;
    }
    
    /* Text colors */
    p, li {
        color: #444444;
        line-height: 1.6;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 8px;
        border: 1px solid #eee;
    }
    
    /* Footer */
    .footer-link {
        color: #666;
        text-decoration: none;
        margin: 0 10px;
        font-size: 0.9rem;
    }
    .footer-link:hover {
        color: #111;
    }
</style>
""", unsafe_allow_html=True)

def scan_dependencies(deps):
    """Scan dependencies and return categorized results"""
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, dep in enumerate(deps):
        status_text.text(f"Scanning {dep['name']}...")
        
        registry_data = {}
        typo_data = {}
        
        name = dep['name']
        eco = dep['ecosystem']
        
        # Check Typosquat
        typo_data = check_typosquatting(name, eco)
        
        # Check Registry
        if eco == 'npm':
            registry_data = check_npm_package(name)
        elif eco == 'pypi':
            registry_data = check_pypi_package(name)
        
        score, reasons = calculate_risk(registry_data, typo_data)
        
        dep['score'] = score
        dep['reasons'] = reasons
        results.append(dep)
        
        progress_bar.progress((i + 1) / len(deps))
    
    status_text.empty()
    progress_bar.empty()
    
    # Categorize results
    safe = [r for r in results if r['score'] < 10]
    suspicious = [r for r in results if 10 <= r['score'] < 60]
    critical = [r for r in results if r['score'] >= 60]
    
    return safe, suspicious, critical

def display_results(safe, suspicious, critical):
    """Display scan results in a beautiful format"""
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total", len(safe) + len(suspicious) + len(critical))
    with col2:
        st.metric("✅ Safe", len(safe))
    with col3:
        st.metric("⚠️ Suspicious", len(suspicious))
    with col4:
        st.metric("❌ Critical", len(critical))
    
    # Overall status
    if critical:
        st.error("🚨 **CRITICAL RISKS DETECTED** - Immediate action required!")
    elif suspicious:
        st.warning("⚠️ **SUSPICIOUS PACKAGES** - Review recommended")
    else:
        st.success("✅ **ALL CLEAR** - No risks detected")
    
    st.markdown("---")
    
    # Critical packages
    if critical:
        st.markdown("### ❌ Critical Risk Dependencies")
        for pkg in critical:
            with st.expander(f"🚨 {pkg['name']} ({pkg['ecosystem']}) - Score: {pkg['score']}/100", expanded=True):
                for reason in pkg['reasons']:
                    st.markdown(f"- {reason}")
    
    # Suspicious packages
    if suspicious:
        st.markdown("### ⚠️ Suspicious Dependencies")
        for pkg in suspicious:
            with st.expander(f"⚠️ {pkg['name']} ({pkg['ecosystem']}) - Score: {pkg['score']}/100"):
                for reason in pkg['reasons']:
                    st.markdown(f"- {reason}")
    
    # Safe packages
    if safe:
        with st.expander(f"✅ {len(safe)} Safe Dependencies"):
            for pkg in safe:
                st.markdown(f"- **{pkg['name']}** ({pkg['ecosystem']})")

def show_landing_page():
    """Display the landing page with installation info"""
    
    # Navbar (Mockup using columns)
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown('<div style="font-weight: 800; font-size: 1.2rem; color: #111;">VibeScan</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(
            """
            <div style="text-align: right; display: flex; justify-content: flex-end; align-items: center;">
                <a href="https://github.com/AbinVarghexe/vibescan" target="_blank" class="nav-link">GitHub</a>
                <a href="https://github.com/AbinVarghexe/vibescan/blob/main/README.md" target="_blank" class="nav-link">Docs</a>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown('<h1 class="hero-title">VibeScan</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-weight: 600; font-size: 1.2rem; margin-bottom: 0.5rem; color: #111;">Works for you, secures with you</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Your Personal Dependency Security Assistant; easy to install, deploy on your own machine or on the cloud; supports multiple package managers with easily extensible capabilities.</p>', unsafe_allow_html=True)
    
    # Call to Action Button
    col1, col2, col3 = st.columns([1, 0.6, 1])
    with col2:
        if st.button("Start Scanning →", use_container_width=True, type="primary", key="start_scan_hero"):
            st.session_state.page = "scanner"
            st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Key Capabilities Section
    st.markdown('<h2>Key capabilities</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Every ecosystem</div>
            <div class="feature-desc">
                Supports npm (Node.js) and PyPI (Python) packages — one assistant, connect as you need.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Under your control</div>
            <div class="feature-desc">
                Privacy and security under your control. Deploy locally or in the cloud; detects hallucinations and typosquatting.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Speed</div>
            <div class="feature-desc">
                Built-in lightning fast scanner; custom checks in your workspace, auto-loaded results in under 1 second.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Installation Section (Simplified for Minimal Design)
    st.markdown('<h2>Get started</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 🐍 Python (pip)")
        st.code("pip install vibescan", language="bash")
        
    with col2:
        st.markdown("### 📦 Node.js (npm)")
        st.code("npm install -g vibescan-js", language="bash")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <a href="https://github.com/AbinVarghexe/vibescan" class="footer-link">GitHub</a>
        <a href="https://github.com/AbinVarghexe/vibescan/blob/main/LICENSE" class="footer-link">License</a>
        <a href="https://github.com/AbinVarghexe/vibescan#readme" class="footer-link">Documentation</a>
        <br><br>
        <span style="color: #999; font-size: 0.8rem;">© 2026 VibeScan. All rights reserved.</span>
    </div>
    """, unsafe_allow_html=True)

def show_scanner_page():
    """Display the scanner interface"""
    # Header with back button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("← Home"):
            st.session_state.page = "landing"
            st.rerun()
    with col2:
        st.markdown('<h1 style="text-align: center;">VibeScan Scanner</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">Upload or paste your dependency file to scan</p>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Scanner content
    tab1, tab2 = st.tabs(["📁 Upload File", "📝 Paste Content"])
    
    with tab1:
        st.markdown("### Upload your dependency file")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["json", "txt"],
            help="Upload package.json or requirements.txt",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Save to temp file
            with tempfile.NamedTemporaryFile(mode='w+', suffix=uploaded_file.name, delete=False, encoding='utf-8') as tmp:
                tmp.write(uploaded_file.getvalue().decode('utf-8'))
                tmp_path = tmp.name
            
            try:
                deps = []
                if uploaded_file.name.endswith('.json') or 'package' in uploaded_file.name:
                    deps = parse_package_json(tmp_path)
                elif uploaded_file.name.endswith('.txt') or 'requirements' in uploaded_file.name:
                    deps = parse_requirements_txt(tmp_path)
                
                if deps:
                    st.info(f"Found {len(deps)} dependencies. Scanning...")
                    safe, suspicious, critical = scan_dependencies(deps)
                    st.markdown("---")
                    st.markdown("## 📊 Scan Results")
                    display_results(safe, suspicious, critical)
                else:
                    st.error("No dependencies found in the file.")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
            finally:
                os.unlink(tmp_path)
    
    with tab2:
        st.markdown("### Paste your file content")
        file_type = st.radio(
            "Select file type:",
            ["package.json", "requirements.txt"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        content = st.text_area(
            "Paste content here",
            height=200,
            placeholder="Paste your package.json or requirements.txt content here...",
            label_visibility="collapsed"
        )
        
        if st.button("🔍 Scan Dependencies", use_container_width=True):
            if content.strip():
                # Save to temp file
                with tempfile.NamedTemporaryFile(mode='w+', suffix=f'.{file_type}', delete=False, encoding='utf-8') as tmp:
                    tmp.write(content)
                    tmp_path = tmp.name
                
                try:
                    deps = []
                    if file_type == "package.json":
                        deps = parse_package_json(tmp_path)
                    else:
                        deps = parse_requirements_txt(tmp_path)
                    
                    if deps:
                        st.info(f"Found {len(deps)} dependencies. Scanning...")
                        safe, suspicious, critical = scan_dependencies(deps)
                        st.markdown("---")
                        st.markdown("## 📊 Scan Results")
                        display_results(safe, suspicious, critical)
                    else:
                        st.error("No dependencies found.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                finally:
                    os.unlink(tmp_path)
            else:
                st.warning("Please paste some content to scan.")

# Main app
def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "landing"
    
    # Route to appropriate page
    if st.session_state.page == "landing":
        show_landing_page()
    else:
        show_scanner_page()

if __name__ == "__main__":
    main()
