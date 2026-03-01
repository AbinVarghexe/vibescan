"""
VibeScan - Streamlit Web Interface
A minimal, Google-like UI for scanning dependencies
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
    page_title="VibeScan - AI Dependency Scanner",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Google-like minimal design
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Clean minimal design */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 800px;
    }
    
    /* Title styling */
    h1 {
        color: white !important;
        text-align: center;
        font-weight: 300 !important;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Card style */
    .card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader */
    .stFileUploader {
        border: 3px dashed #667eea;
        border-radius: 10px;
        padding: 2rem;
        background: #f8f9ff;
    }
    
    /* Success/Warning/Error boxes */
    .stAlert {
        border-radius: 10px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 10px 10px 0 0;
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

# Main app
def main():
    # Header
    st.markdown('<h1>🔍 VibeScan</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI Dependency Security Scanner</p>', unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Tabs for different input methods
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
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('<div class="card">', unsafe_allow_html=True)
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
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('<div class="card">', unsafe_allow_html=True)
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: white; opacity: 0.8;">Built with ❤️ to protect developers from AI hallucinations</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()