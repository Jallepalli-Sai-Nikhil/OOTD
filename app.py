import streamlit as st
import json
from pathlib import Path

# 🔧 Must be first
st.set_page_config(page_title="Outfit Vault", layout="wide")

# 🔐 Password protection via Streamlit Secrets
try:
    PASSWORD = st.secrets["password"]
except Exception as e:
    st.error("❌ Secrets file missing! Create .streamlit/secrets.toml locally or set on Streamlit Cloud.")
    st.stop()

user_input = st.text_input("Enter password to unlock outfits", type="password")
if user_input != PASSWORD:
    st.warning("🔐 Incorrect password or not entered.")
    st.stop()

# 🎨 Title
st.title("🧵 Outfit Vault – Curated Looks")

# 📁 Paths
DATA_DIR = Path("data")
STATIC_DIR = "static"

# 📦 Load all outfit category JSONs
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

# 🧥 Display outfits
for outfit in outfits:
    st.markdown("---")
    cols = st.columns([2, 3, 5])

    image_file = outfit.get("image", "")
    image_path = f"{STATIC_DIR}/{folder}/{image_file}"

    with cols[0]:
        # Check if image format is valid
        if any(image_file.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png"]):
            try:
                st.image(image_path, use_container_width=True)
            except:
                st.error(f"❌ Error loading image: {image_path}")
        else:
            st.warning("⚠️ Unsupported image format")

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

# --- BODY SECTION ADDITION ---
st.markdown("---")
st.header("💪 Body Vault – Muscle Groups & Exercises")

# 📦 Load muscle group data
MUSCLE_GROUPS_PATH = DATA_DIR / "muscle_group.json"
if MUSCLE_GROUPS_PATH.exists():
    with open(MUSCLE_GROUPS_PATH, "r", encoding="utf-8") as f:
        muscle_data = json.load(f)
else:
    muscle_data = []

# If muscle_data is a dict, wrap in list for uniformity
if isinstance(muscle_data, dict):
    muscle_data = [muscle_data]

muscle_group_names = [mg.get("muscle_group", "Unknown") for mg in muscle_data]
selected_muscle = st.selectbox("🏋️ Choose a muscle group", muscle_group_names)

# Find selected muscle group
muscle_group = next((mg for mg in muscle_data if mg.get("muscle_group") == selected_muscle), None)

# ...existing code...

# ...existing code above...

if muscle_group:
    st.subheader(f"🔹 {muscle_group.get('muscle_group', '')}")
    sub_muscles = muscle_group.get("sub_muscles", [])
    if not sub_muscles:
        st.info("No sub sections available for this muscle group.")
    else:
        for sub in sub_muscles:
            st.markdown(f"### {sub.get('name', 'Sub Muscle')}")
            # Show sub muscle image if available
            sub_image = sub.get("image")
            if sub_image:
                folder = muscle_group.get('folder', '').replace('muscles/', '')
                sub_image_path = f"{STATIC_DIR}/{folder}/{sub_image}"
                try:
                    st.image(sub_image_path, caption=sub.get('name', ''), use_container_width=True)
                except:
                    st.error(f"❌ Error loading image: {sub_image_path}")
            # List exercises for this sub muscle
            exercises = sub.get("exercises", [])
            if not exercises:
                st.write("_No exercises listed._")
            else:
                for ex in exercises:
                    cols = st.columns([2, 8])
                    gif_file = ex.get("gif")
                    title = ex.get("title", "Untitled Exercise")
                    with cols[0]:
                        if gif_file:
                            gif_path = f"{STATIC_DIR}/{folder}/{gif_file}"
                            try:
                                st.image(gif_path, use_container_width=True)
                            except:
                                st.error(f"❌ Error loading gif: {gif_path}")
                        else:
                            st.info("No GIF available")
                    with cols[1]:
                        st.markdown(f"**{title}**")