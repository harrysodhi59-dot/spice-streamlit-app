import streamlit as st
import pandas as pd

st.title("SPICE Solar Analytics Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="main_uploader")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # save in session
    st.session_state["df"] = df
    st.session_state["uploaded_data"] = df

    # save bytes too
    st.session_state["uploaded_file_bytes"] = uploaded_file.getvalue()
    st.session_state["uploaded_file_name"] = uploaded_file.name

    # optional preview
    st.success("Dataset uploaded successfully.")
    st.dataframe(df.head(10), use_container_width=True)

    st.write("Session keys now:", list(st.session_state.keys()))
else:
    st.info("Please upload a CSV file.")
