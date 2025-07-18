import streamlit as st
import json
from pathlib import Path

# 🔧 Must be first
st.set_page_config(page_title="Outfit Vault", layout="wide")

# Set a fixed image display width for all images and gifs
IMAGE_DISPLAY_WIDTH = 300
# Patch muscle group folder paths to match new static directory structure
def fix_muscle_folder(folder):
    # Ensure 'muscles/' prefix is present and no leading/trailing slashes
    folder = folder.strip("/")
    if not folder.startswith("muscles/"):
        folder = f"muscles/{folder}"
    return folder
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

# Only show muscle group section if "Muscle Group" category is selected
if selected_category.lower() != "muscle group":
    st.stop()
show_muscle_section = st.checkbox("Show Body Vault section", value=False)
if not show_muscle_section:
    st.stop()

# ...existing code...

IMAGE_DISPLAY_WIDTH = 150
IMAGE_DISPLAY_HEIGHT = 100

def fix_muscle_folder(folder):
    # Remove 'muscles/' if present, for static path consistency
    return folder.replace('muscles/', '')

# Utility: Centered image in fixed-size container
def centered_image(image_path, caption=None, width=IMAGE_DISPLAY_WIDTH, height=IMAGE_DISPLAY_HEIGHT):
    container_style = f"""
        display: flex;
        justify-content: center;
        align-items: center;
        height: {height}px;
        width: {width}px;
        background: #fafafa;
        border: 1px solid #eee;
        border-radius: 12px;
        margin: 0 auto 10px auto;
        overflow: hidden;
    """
    img_html = f"""
        <div style="{container_style}">
            <img src="{image_path}" alt="{caption or ''}" style="max-width: 100%; max-height: 100%; object-fit: contain;"/>
        </div>
    """
    st.markdown(img_html, unsafe_allow_html=True)
    if caption:
        st.caption(caption)

muscle_group_names = [mg.get("muscle_group", "Unknown") for mg in muscle_data]
# Only show muscle group selectbox if "Muscle Group" category is selected
if selected_category.lower() == "muscle group":
    selected_muscle = st.selectbox("🏋️ Choose a muscle group", muscle_group_names)
else:
    selected_muscle = None

# Find selected muscle group
muscle_group = next((mg for mg in muscle_data if mg.get("muscle_group") == selected_muscle), None)

if muscle_group:
    st.subheader(f"🔹 {muscle_group.get('muscle_group', '')}")

    # Show main muscle group image if available, centered and fixed size
    main_image = muscle_group.get("image")
    if main_image:
        folder = fix_muscle_folder(muscle_group.get('folder', ''))
        main_image_path = f"{STATIC_DIR}/{folder}/{main_image}"
        try:
            centered_image(main_image_path, caption=muscle_group.get('muscle_group', ''))
        except:
            st.error(f"❌ Error loading image: {main_image_path}")

    sub_muscles = muscle_group.get("sub_muscles", [])
    if not sub_muscles:
        st.info("No sub sections available for this muscle group.")
    else:
        for sub in sub_muscles:
            st.markdown(f"### {sub.get('name', 'Sub Muscle')}")
            # Show sub muscle image if available, centered and fixed size
            sub_image = sub.get("image")
            if sub_image:
                folder = fix_muscle_folder(muscle_group.get('folder', ''))
                sub_image_path = f"{STATIC_DIR}/{folder}/{sub_image}"
                try:
                    centered_image(sub_image_path, caption=sub.get('name', ''))
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
                            folder = fix_muscle_folder(muscle_group.get('folder', ''))
                            gif_path = f"{STATIC_DIR}/{folder}/{gif_file}"
                            try:
                                centered_image(gif_path, width=IMAGE_DISPLAY_WIDTH, height=IMAGE_DISPLAY_HEIGHT)
                            except:
                                st.error(f"❌ Error loading gif: {gif_path}")
                        else:
                            st.info("No GIF available")
                    with cols[1]:
                        st.markdown(f"**{title}**")
# ...existing code...s