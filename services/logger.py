import streamlit as st
import pandas as pd
from datetime import datetime

class LiveLogger:
    def __init__(self, table_placeholder):
        if "log_entries" not in st.session_state:
            st.session_state.log_entries = []
        self.placeholder = table_placeholder

    def log(self, step, tool, status="STARTED"):
        entry = {
            "Timestamp": datetime.now().strftime("%H:%M:%S"),
            "Order": len(st.session_state.log_entries) + 1,
            "Step Description": step,
            "Tool/App/URL/EXE": tool,
            "Status": status
        }
        
        # If we are updating a previous "STARTED" step to "SUCCESS"
        if status in ["SUCCESS", "FAILED", "RETRIED"]:
            for item in reversed(st.session_state.log_entries):
                if item["Step Description"] == step and item["Status"] == "STARTED":
                    item["Status"] = status
                    break
            else: st.session_state.log_entries.append(entry)
        else:
            st.session_state.log_entries.append(entry)
            
        self.placeholder.dataframe(pd.DataFrame(st.session_state.log_entries), use_container_width=True)