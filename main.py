import streamlit as st
import os
import pandas as pd
from datetime import datetime
from services.logger import LiveLogger
from services.gmail_service import GmailService

st.set_page_config(page_title="WorkCortex Intelligence Tool", layout="wide")

st.title("📧 AI Gmail Intelligence Tool")
st.markdown("Extract cleaned, distinct recipient IDs from any sender.")

# Configuration Sidebar
with st.sidebar:
    st.header("Settings")
    sender = st.text_input("Sender Email Address", value="newsletter@example.com")
    local_path = st.text_input("Save Folder Path", value=os.getcwd())
    st.info("Ensure credentials.json is in the root directory.")

# Log Table Area
st.subheader("Live Execution Logs")
log_container = st.empty()
logger = LiveLogger(log_container)

if st.button("🚀 Start Extraction"):
    try:
        # 1. Initialize & Auth
        engine = GmailService(logger)
        engine.authenticate()
        
        # 2. Fetch & Clean
        emails = engine.fetch_emails(sender)
        
        if not emails:
            st.warning("No emails found from that sender.")
        else:
            # 3. Save to Excel
            logger.log("Saving to Excel", "Pandas/Openpyxl", "STARTED")
            
            df = pd.DataFrame(emails, columns=["Recipient Email IDs"])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"recipients_{timestamp}.xlsx"
            full_save_path = os.path.join(local_path, file_name)
            
            df.to_excel(full_save_path, index=False)
            
            logger.log("Saving to Excel", "Pandas/Openpyxl", "SUCCESS")
            st.success(f"Done! {len(emails)} unique IDs saved to: {full_save_path}")
            st.balloons()
            
    except Exception as e:
        logger.log(f"Failure: {str(e)}", "System", "FAILED")
        st.error(f"Error during execution: {e}")