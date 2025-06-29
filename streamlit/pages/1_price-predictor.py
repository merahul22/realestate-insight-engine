import pickle
import numpy as np
import pandas as pd
import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title=" Price Prediction", page_icon="💰", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4B8BBE;'> Property Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Get an estimated price based on property details</p>",
            unsafe_allow_html=True)
st.markdown("---")

# ---------- LOAD DATA ----------
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)
with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# ---------- INPUT COLUMNS ----------
col1, col2, col3 = st.columns(3)

with col1:
    property_type = st.selectbox(' Property Type', ['flat', 'house'])
    sector = st.selectbox(' Sector', sorted(df['sector'].dropna().unique().tolist()))
    furnishing_type = st.selectbox(' Furnishing Type', sorted(df['furnishing_type'].dropna().unique().tolist()))

with col2:
    bedrooms = float(st.selectbox(' Number of Bedrooms', sorted(df['bedRoom'].dropna().unique().tolist())))
    bathroom = float(st.selectbox(' Number of Bathrooms', sorted(df['bathroom'].dropna().unique().tolist())))
    floor_category = st.selectbox(' Floor Category', sorted(df['floor_category'].dropna().unique().tolist()))

with col3:
    balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].dropna().unique().tolist()))
    property_age = st.selectbox(' Property Age', sorted(df['agePossession'].dropna().unique().tolist()))
    luxury_category = st.selectbox(' Luxury Category', sorted(df['luxury_category'].dropna().unique().tolist()))

# ---------- ADDITIONAL INPUT ----------
st.markdown("#### Additional Details")
a_col1, a_col2, a_col3 = st.columns(3)

with a_col1:
    built_up_area = float(st.number_input('Built Up Area (in sq.ft)', min_value=100.0))

with a_col2:
    servant_room = float(st.selectbox('Servant Room', [0.0, 1.0]))

with a_col3:
    store_room = float(st.selectbox('Store Room', [0.0, 1.0]))

# ---------- PREDICT BUTTON ----------
st.markdown("---")
if st.button(' Predict Price'):
    data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area,
             servant_room, store_room, furnishing_type, luxury_category, floor_category]]

    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    one_df = pd.DataFrame(data, columns=columns)
    st.subheader(" Input Summary")
    st.dataframe(one_df)

    # ---------- PREDICTION ----------
    base_price = np.expm1(pipeline.predict(one_df))[0]  # If target was log-transformed
    low = base_price - 0.22
    high = base_price + 0.22

    st.success(f" **Estimated Price Range:** ₹{round(low, 2)} Cr – ₹{round(high, 2)} Cr")
    st.caption("*(Note: ±0.22 Cr uncertainty based on model variance)*")
