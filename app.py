import streamlit as st

st.title("My First SPICE App")

st.write("Hello 👋 This is my solar dashboard")

system_size = st.slider("System Size (kW)", 1, 100, 10)

st.write("You selected:", system_size)
