import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

# ----------- PAGE CONFIG -----------
st.set_page_config(page_title=" Real Estate Visual Analytics", layout="wide")

# ----------- LOAD DATA -----------
new_df = pd.read_csv('streamlit/data_viz1.csv')
feature_text = pickle.load(open('streamlit/feature_text.pkl', 'rb'))

cols = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
new_df[cols] = new_df[cols].apply(pd.to_numeric, errors='coerce')
new_df = new_df.dropna(subset=['sector'])

# ----------- AGGREGATION FOR MAP -----------
group_df = new_df.groupby('sector')[cols].mean()

# ----------- SECTION 1: MAPBOX GEO VISUALIZATION -----------
st.markdown("##  Sector Price per Sqft Geomap")
fig_map = px.scatter_mapbox(
    group_df,
    lat="latitude",
    lon="longitude",
    color="price_per_sqft",
    size='built_up_area',
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=10,
    mapbox_style="open-street-map",
    width=1200,
    height=700,
    hover_name=group_df.index
)
st.plotly_chart(fig_map, use_container_width=True)

# ----------- SECTION 2: WORD CLOUD -----------
st.markdown("##  Features Wordcloud")
wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='black',
    stopwords=set(['s']),
    min_font_size=10
).generate(feature_text)

fig_wc, ax = plt.subplots(figsize=(8, 8))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)
st.pyplot(fig_wc)

# ----------- SECTION 3: AREA VS PRICE -----------
st.markdown("##  Area vs Price by Property Type")
property_type = st.selectbox('Select Property Type', ['flat', 'house'])

df_filtered = new_df[new_df['property_type'] == property_type]
fig_scatter = px.scatter(
    df_filtered,
    x="built_up_area",
    y="price",
    color="bedRoom",
    title=f"Area vs Price for {property_type.capitalize()}s",
    labels={"built_up_area": "Built-up Area (sq.ft)", "price": "Price (Cr)"}
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ----------- SECTION 4: BHK PIE CHART -----------
st.markdown("##  BHK Distribution by Sector")
sector_options = sorted(new_df['sector'].dropna().unique().tolist())
sector_options.insert(0, 'overall')
selected_sector = st.selectbox('Select Sector for BHK Pie Chart', sector_options)

if selected_sector == 'overall':
    df_sector = new_df
else:
    df_sector = new_df[new_df['sector'] == selected_sector]

fig_pie = px.pie(df_sector, names='bedRoom', title=f"BHK Distribution - {selected_sector.title()}")
st.plotly_chart(fig_pie, use_container_width=True)

# ----------- SECTION 5: BOX PLOT BHK PRICE RANGE -----------
st.markdown("##  Side-by-Side BHK Price Comparison")
fig_box = px.box(
    new_df[new_df['bedRoom'] <= 4],
    x='bedRoom',
    y='price',
    title='BHK Price Range (Up to 4 BHK)',
    labels={"price": "Price (Cr)", "bedRoom": "Number of Bedrooms"}
)
st.plotly_chart(fig_box, use_container_width=True)

# ----------- SECTION 6: DISTPLOT OF PROPERTY TYPES -----------
st.markdown("##  Property Price Distribution by Type")
fig_dist, ax = plt.subplots(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='House', kde=True, color="green")
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='Flat', kde=True, color="blue")
plt.xlabel("Price (Cr)")
plt.ylabel("Frequency")
plt.legend()
st.pyplot(fig_dist)
