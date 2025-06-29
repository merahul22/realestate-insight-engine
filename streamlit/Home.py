import streamlit as st
from PIL import Image

# Page setup
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics App",
    page_icon="🏡",
    layout="wide"
)

# Optional: Add a background image or hero image
# st.image("https://images.pexels.com/photos/439391/pexels-photo-439391.jpeg")

# Title & subtitle
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🏙️ Gurgaon Real Estate Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Explore • Predict • Invest Smart</h4>", unsafe_allow_html=True)
st.markdown("---")

# Columns for layout
col1, col2 = st.columns([2, 3])

with col1:
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c", caption="Gurgaon Skyline", use_column_width=True)

with col2:
    st.markdown("""
    ### 🔍 Features of this App
    - 📊 **Real-Time Analytics** on properties by sector, price, area, and more.
    - 🎯 **Smart Recommendations** based on features and preferences.
    - 💰 **Price Prediction Engine** using machine learning models.
    - 🌐 **Map Visualizations** with neighborhood insights.
    - 🧠 **Intelligent Filtering** by budget, area, rooms, and amenities.

    ---
    👉 Use the **sidebar** to navigate between modules.

    💡 Whether you're a buyer, seller, or investor — this app helps you make **data-driven decisions**.
    """)

# Sidebar
st.sidebar.title("📁 Navigation")
st.sidebar.success("Choose a module to get started:")

# Footer (optional)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Built with ❤️ using Streamlit | © 2025 Gurgaon Analytics</p>", unsafe_allow_html=True)
