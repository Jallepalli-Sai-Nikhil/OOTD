import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="Outfit Guide", layout="wide")
st.title("🧵 Outfit Ideas by Category")

DATA_DIR = Path("data")
ASSETS_DIR = Path("assets")

# List all JSON files (1 per category)
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
        
        with cols[0]:
            image_path = ASSETS_DIR / folder / outfit["image"]
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
            else:
                st.error(f"Image not found: {image_path}")

        with cols[1]:
            st.subheader(outfit["title"])

        with cols[2]:
            btns = st.columns(len(outfit["brands"]))
            for i, brand in enumerate(outfit["brands"]):
                with btns[i]:
                    st.link_button(brand["label"], brand["link"])
