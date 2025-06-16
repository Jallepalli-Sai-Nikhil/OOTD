import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Outfit Guide", layout="wide")
st.title("🧵 Outfit Ideas by Category")

DATA_DIR = Path("data")
STATIC_DIR = "static"  # Folder visible to streamlit

json_files = sorted(DATA_DIR.glob("*.json"))

for json_file in json_files:
    with open(json_file) as f:
        data = json.load(f)

    category = data.get("category", "Unknown Category")
    folder = data.get("folder", "")

    st.header(f"📌 {category}")

    for outfit in data["outfits"]:
        st.markdown("---")
        cols = st.columns([2, 3, 5])

        image_url = f"{STATIC_DIR}/{folder}/{outfit['image']}"

        with cols[0]:
            st.image(image_url, use_container_width=True)  # ✅ Load as URL, not PIL

        with cols[1]:
            st.subheader(outfit["title"])

        with cols[2]:
            btns = st.columns(len(outfit["brands"]))
            for i, brand in enumerate(outfit["brands"]):
                with btns[i]:
                    st.link_button(brand["label"], brand["link"])
