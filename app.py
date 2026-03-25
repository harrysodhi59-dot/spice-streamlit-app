import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SPICE Solar Analytics", layout="wide")

st.title("SPICE Solar Analytics Dashboard")
st.write("Upload your CSV dataset to explore solar, financial, and environmental insights.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Save dataframe in session state
    st.session_state["df"] = df
    st.session_state["uploaded_data"] = df

    # Save file locally so other pages can reload it
    save_path = "uploaded_dataset.csv"
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.session_state["uploaded_file_path"] = save_path

    st.success("Dataset uploaded successfully and is now available across pages.")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Dataset Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))
else:
    st.info("Please upload a CSV file to continue.")

import streamlit as st

st.set_page_config(page_title="SPICE Solar Impact Dashboard", layout="wide")

st.title("SPICE Solar Impact Dashboard")
st.write("Use the sidebar to open the project pages.")
st.success("Start with the Home page in the sidebar.")
