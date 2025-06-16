import streamlit as st
import os
import json

# App config
st.set_page_config(page_title="dressing guide", layout="wide")
st.title("👕 dressing guide")

# Secure password protection
password = st.secrets.get("app_password", "")  # from Streamlit Secrets UI

user_input = st.text_input("enter password", type="password")
if user_input != password:
    st.warning("🔒 enter the correct password to view outfits")
    st.stop()

# Load all category JSON files
data_dir = "data"
json_files = sorted([f for f in os.listdir(data_dir) if f.endswith(".json")])

for file in json_files:
    with open(os.path.join(data_dir, file)) as f:
        data = json.load(f)

    st.markdown(f"### 🧵 {data['category']}")
    for outfit in data["outfits"]:
        st.markdown("---")
        cols = st.columns([2, 3, 5])
        with cols[0]:
            st.image(outfit["image"], use_column_width=True)
        with cols[1]:
            st.subheader(outfit["title"])
        with cols[2]:
            btns = st.columns(len(outfit["brands"]))
            for i, brand in enumerate(outfit["brands"]):
                with btns[i]:
                    st.link_button(brand["label"], brand["link"])
