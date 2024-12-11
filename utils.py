import streamlit as st

def update_produce_data(analysis):
    table_row = {
        "Sl No": len(st.session_state.produce_data) + 1,
        "Timestamp": analysis["timestamp"],
        "Produce": analysis["Produce"],
        "Freshness": analysis["Freshness"],
        "Expected Lifespan (Days)": analysis["Expected Lifespan (Days)"]
    }
    st.session_state.produce_data.append(table_row)
