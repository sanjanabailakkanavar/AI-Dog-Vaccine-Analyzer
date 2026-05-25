import streamlit as st
import os
import sys

# add current folder to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vaccine_analyzer import VaccineAnalyzer, setup_logging
st.set_page_config(page_title="Vaccine Analyzer AI", layout="centered")

st.title("🩺 Vaccine Analyzer GenAI App")
st.write("Upload a vaccine image and get AI + LLM-based analysis")

# Upload image
uploaded_file = st.file_uploader(
    "📤 Upload Vaccine Image",
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded_file is not None:

    # Save image
    os.makedirs("uploads", exist_ok=True)
    image_path = os.path.join("uploads", uploaded_file.name)

    with open(image_path, "wb") as f:
        f.write(uploaded_file.read())

    # Show image
    st.image(image_path, caption="Uploaded Image", use_container_width=True)

    st.write("🔍 Processing image... please wait")

    # Run analyzer
    analyzer = VaccineAnalyzer(image_path)
    result = analyzer.analyze_vaccines()

    # Output section
    st.subheader("📊 Analysis Result")

    # 1. Matched vaccines
    st.write("### 🧪 Detected Vaccines")
    st.write(result.get("matched_vaccines"))

    # 2. LLM output (IMPORTANT PART)
    if "llm_analysis" in result:
        st.write("### 🤖 AI Analysis")
        st.markdown(result["llm_analysis"])

    # fallback message
    if "message" in result:
        st.warning(result["message"])

    # cleanup
    if os.path.exists(image_path):
        os.remove(image_path)