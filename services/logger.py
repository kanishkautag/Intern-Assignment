import streamlit as st
import pandas as pd
from datetime import datetime

class LiveLogger:
    def __init__(self, placeholder):
        self.placeholder = placeholder
        if 'logs' not in st.session_state:
            st.session_state.logs = []

    def log(self, step: str, tool: str, status: str):
        entry = {
            "Timestamp": datetime.now().strftime("%H:%M:%S"),
            "Order": len(st.session_state.logs) + 1,
            "Step Description": step,
            "Tool/App/URL/EXE": tool,
            "Status": status
        }
        
        # Color coding logic
        color_map = {
            "STARTED": "blue",
            "SUCCESS": "green",
            "FAILED": "red",
            "RETRIED": "orange"
        }
        color = color_map.get(status, "black")
        
        # Update logic: if SUCCESS/FAILED/RETRIED, update the last matching STARTED
        updated = False
        if status != "STARTED":
            for item in reversed(st.session_state.logs):
                if item["Step Description"] == step and item["Status"] == "STARTED":
                    item["Status"] = status
                    item["Timestamp"] = entry["Timestamp"] # Update time to completion
                    updated = True
                    break
        
        if not updated:
            st.session_state.logs.append(entry)

        # Rendering with HTML/CSS for color
        df = pd.DataFrame(st.session_state.logs)
        
        # Display the table and auto-scroll (handled by st.dataframe internally)
        self.placeholder.dataframe(
            df.style.applymap(lambda x: f"color: {color_map.get(x, 'black')}", subset=['Status']),
            use_container_width=True,
            hide_index=True
        )