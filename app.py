import streamlit as st
import json
from pathlib import Path

# 🔐 Password protection via Streamlit Secrets
PASSWORD = st.secrets["app_password"]
user_input = st.text_input("Enter password to unlock outfits", type="password")

if user_input != PASSWORD:
    st.warning("🔐 Incorrect password or not entered.")
    st.stop()

# ✅ Streamlit app config
st.set_page_config(page_title="Outfit Vault", layout="wide")
st.title("🧵 Outfit Vault – Curated Looks by Category")

# 📁 Paths
DATA_DIR = Path("data")
STATIC_DIR = "static"

# 🔁 Load all outfit category JSONs
categories = {}
for json_file in sorted(DATA_DIR.glob("*.json")):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        category = data.get("category", json_file.stem.replace("_", " ").title())
        categories[category] = data

# 🧭 Select category
selected_category = st.selectbox("📂 Choose a category", list(categories.keys()))
section = categories[selected_category]
folder = section.get("folder", "")
outfits = section.get("outfits", [])

# 🎨 Display each outfit block
for outfit in outfits:
    st.markdown("---")
    cols = st.columns([2, 3, 5])

    image_file = outfit.get("image", "")
    image_path = f"{STATIC_DIR}/{folder}/{image_file}"

    with cols[0]:
        if any(image_file.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
            st.image(image_path, use_container_width=True)
        else:
            st.warning("⚠️ Unsupported or missing image file.")

    with cols[1]:
        st.subheader(outfit.get("title", "Untitled Look"))

    with cols[2]:
        brands = outfit.get("brands", [])
        if brands:
            st.markdown("**🛍️ Available At:**")
            for brand in brands:
                label = brand.get("label", "").title()
                link = brand.get("link", "#")
                st.markdown(
                    f"""
                    <a href="{link}" target="_blank">
                        <div style="display:inline-block; padding:6px 14px;
                                    margin:6px 8px 6px 0;
                                    border-radius:20px; background-color:#f5f5f5;
                                    border:1px solid #ccc; text-decoration:none;
                                    font-size:14px; color:#333;">
                            {label}
                        </div>
                    </a>
                    """,
                    unsafe_allow_html=True
                )
