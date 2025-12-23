import streamlit as st
import os
import time
import pandas as pd
from datetime import datetime
from services.logger import LiveLogger
from services.gmail_service import GmailService

st.set_page_config(page_title="WorkCortex AI Engine", layout="wide")

# UI State Management
if 'paused' not in st.session_state: st.session_state.paused = False
if 'abort' not in st.session_state: st.session_state.abort = False

# Sidebar Config
with st.sidebar:
    st.header("Configuration")
    sender = st.text_input("Sender Email", "newsletter@github.com")
    out_dir = st.text_input("Output Folder", os.getcwd())
    filename = st.text_input("Filename", "recipients.xlsx")
    limit = st.slider("Max Emails to Scan", 1, 500, 50)
    
    st.divider()
    # Controls
    col_a, col_b = st.columns(2)
    start_btn = col_a.button("🚀 Start", use_container_width=True)
    abort_btn = col_b.button("🛑 Abort", use_container_width=True)
    
    if st.button("⏸ Pause / ▶ Resume"):
        st.session_state.paused = not st.session_state.paused

if abort_btn: st.session_state.abort = True

st.title("WorkCortex Intelligence System")
log_space = st.empty()
logger = LiveLogger(log_space)

if start_btn:
    st.session_state.abort = False
    start_time = time.time()
    
    try:
        engine = GmailService(logger)
        
        # 1. Auth
        if not engine.authenticate():
            st.error("Authentication Failed.")
            st.stop()
            
        # 2. Fetch
        data = engine.fetch_distinct_recipients(sender, limit)
        
        # 3. Save
        logger.log("Saving to Excel", "Pandas", "STARTED")
        df = pd.DataFrame(data, columns=["Recipient Email IDs"])
        path = os.path.join(out_dir, f"{datetime.now().strftime('%H%M%S')}_{filename}")
        df.to_excel(path, index=False)
        logger.log("Saving to Excel", "Pandas", "SUCCESS")
        
        # Run Summary
        st.divider()
        st.subheader("Run Summary")
        c1, c2, c3 = st.columns(3)
        c1.metric("Unique Emails Found", len(data))
        c2.metric("Execution Time", f"{round(time.time() - start_time, 2)}s")
        c3.info(f"Saved to: {path}")
        
    except InterruptedError:
        st.warning("Process Aborted by User.")
    except Exception as e:
        st.error(f"Critical System Error: {e}")