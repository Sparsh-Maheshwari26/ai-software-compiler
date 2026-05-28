import streamlit as st
import time
from pipeline import run_auto_repair_pipeline

# 1. Page Configuration
st.set_page_config(page_title="AI Software Compiler", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for professional look
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 16px; border-radius: 8px; }
    .main-header { font-size: 32px; font-weight: bold; color: #2ea44f; }
    .metric-box { background-color: #f0f2f6; padding: 10px; border-radius: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">⚡ Autonomous Software Architect</p>', unsafe_allow_html=True)
st.markdown("Compiler System: **Natural Language → Validated Executable Schema**")

input_col, output_col = st.columns([1, 2], gap="large")

with input_col:
    st.write("### 📥 System Input")
    user_input = st.text_area(
        "Application Specifications:", 
        height=250, 
        placeholder="e.g., Build a CRM with login, dashboard, and role-based access..."
    )
    compile_btn = st.button("🚀 Compile Architecture", use_container_width=True)

with output_col:
    st.write("### 📤 Compiler Output")
    
    if compile_btn:
        if len(user_input.strip()) < 10:
            st.warning("⚠️ Specifications are too vague for compilation.")
        else:
            # TRACKING METRICS (Task Req #8)
            start_time = time.time()
            
            with st.spinner("Executing Multi-Stage Pipeline (Extraction → Design → Validation)..."):
                # RUN REAL PIPELINE
                config, is_valid = run_auto_repair_pipeline(user_input)
                
                latency = round(time.time() - start_time, 2)
            
            # Display Metrics
            m1, m2, m3 = st.columns(3)
            m1.metric("Latency", f"{latency}s")
            m2.metric("Status", "Validated" if is_valid else "Conflict")
            m3.metric("Model", "Gemini 2.0 Flash")

            if is_valid:
                st.success("✅ Schema Verified: Cross-layer consistency guaranteed.")
                
                tab1, tab2, tab3 = st.tabs(["💻 Full JSON Contract", "🗄️ DB Architecture", "🔌 API Schema"])
                
                with tab1:
                    st.json(config.model_dump())
                    
                with tab2:
                    for table in config.database:
                        with st.expander(f"TABLE: {table.name.upper()}"):
                            for col in table.columns:
                                st.code(f"{col.name}: {col.type}")
                                    
                with tab3:
                    for api in config.api:
                        st.info(f"**{api.method}** `{api.path}` — {api.description}")
            else:
                st.error("❌ Logical Inconsistency Detected: Auto-repair failed to resolve conflicts.")
                st.json(config.model_dump())