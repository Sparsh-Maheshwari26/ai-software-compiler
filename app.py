import streamlit as st
from pipeline import run_auto_repair_pipeline

# 1. Turn on Wide Mode for a professional dashboard look
st.set_page_config(page_title="AI Software Compiler", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to make it look a bit more sleek (Dark mode friendly)
st.markdown("""
    <style>
    .stTextArea textarea { font-size: 16px; border-radius: 8px; }
    .success-text { color: #00ff00; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Autonomous Software Architect")
st.markdown("Enter your product requirements below. The system will compile a strict, deterministic schema.")

# Create two columns: Left for input, Right for output
input_col, output_col = st.columns([1, 2], gap="large")

with input_col:
    st.write("### System Input")
    user_input = st.text_area(
        "Application Specifications:", 
        height=200, 
        placeholder="e.g., Build a CRM with a dashboard, role-based access, and a PostgreSQL database..."
    )
    compile_btn = st.button("🚀 Compile Architecture", use_container_width=True)

with output_col:
    st.write("### Compiler Output")
    
    if compile_btn:
        if len(user_input) < 10:
            st.warning("⚠️ Please provide more detailed specifications.")
        else:
            with st.spinner("Analyzing intent, generating schema, and running auto-repair validation..."):
                config, is_valid = run_auto_repair_pipeline(user_input)
                
                if is_valid:
                    st.success("✅ Compilation Successful! Zero schema violations detected.")
                    
                    # 2. Use TABS to organize the output like a real tool
                    tab1, tab2, tab3 = st.tabs(["💻 Raw JSON", "🗄️ Database Schema", "🔌 API Routes"])
                    
                    with tab1:
                        st.json(config.model_dump())
                        
                    with tab2:
                        st.write("#### Generated Tables")
                        for table in config.database:
                            with st.expander(f"Table: {table.name.upper()}", expanded=True):
                                for col in table.columns:
                                    st.markdown(f"- **{col.name}** (`{col.type}`)")
                                    
                    with tab3:
                        st.write("#### API Endpoints")
                        for api in config.api:
                            st.info(f"**{api.method}** `{api.path}`  \n_{api.description}_")
                else:
                    st.error("❌ System failed to resolve schema conflicts.")
                    st.json(config.model_dump())