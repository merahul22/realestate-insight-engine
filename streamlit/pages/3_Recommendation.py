import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(
    page_title="Apartment Recommendor",
    page_icon="🏡",
    layout="wide"
)

# Load original CSV to get property links
original_df = pd.read_csv("apartments.csv")  # make sure this is the correct path

# Load distance DataFrame and similarity matrices
location_df = pickle.load(open("streamlit/datasets/location_distance.pkl", "rb"))
cosine_sim1 = pickle.load(open("streamlit/datasets/cosine_sim1.pkl", "rb"))
cosine_sim2 = pickle.load(open("streamlit/datasets/cosine_sim2.pkl", "rb"))
cosine_sim3 = pickle.load(open("streamlit/datasets/cosine_sim3.pkl", "rb"))

# Normalize and combine similarity matrices
scaler = MinMaxScaler()
sim1_scaled = scaler.fit_transform(cosine_sim1)
sim2_scaled = scaler.fit_transform(cosine_sim2)
sim3_scaled = scaler.fit_transform(cosine_sim3)

cosine_sim_matrix = 0.5 * sim1_scaled + 0.8 * sim2_scaled + 1.0 * sim3_scaled

# Recommendation function
def recommend_properties_with_scores(property_name, top_n=5):
    try:
        idx = location_df.index.get_loc(property_name)
    except KeyError:
        return pd.DataFrame(columns=['PropertyName', 'SimilarityScore', 'Link'])

    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    top_indices = [i[0] for i in sorted_scores]
    top_scores = [i[1] for i in sorted_scores]
    top_properties = location_df.index[top_indices].tolist()

    result_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': [round(score, 3) for score in top_scores]
    })

    # Merge with original_df to get property links
    result_df = result_df.merge(original_df[['PropertyName', 'Link']], on='PropertyName', how='left')

    return result_df

# UI
st.title("🔍 Apartment Finder & Recommender")

# --- Location radius filter ---
st.subheader("📍 Filter by Location and Radius")
col1, col2 = st.columns(2)

with col1:
    selected_location = st.selectbox("Choose a location", sorted(location_df.columns.to_list()))
with col2:
    radius = st.number_input("Radius (in kilometers)", min_value=0.0, step=0.5)

if st.button("Search Nearby Apartments"):
    if selected_location in location_df.columns:
        result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
        if not result_ser.empty:
            st.markdown(f"### Properties within {radius} km of {selected_location}:")
            for key, value in result_ser.items():
                st.write(f"🔹 **{key}** — {round(value / 1000, 2)} km")
        else:
            st.warning("No properties found in the given radius.")
    else:
        st.error("Selected location not found.")

# --- Recommendations section ---
st.subheader("🏡 Recommend Similar Apartments")
selected_apartment = st.selectbox("Select an apartment", sorted(location_df.index.to_list()))

if st.button("Get Recommendations"):
    recommendation_df = recommend_properties_with_scores(selected_apartment)
    if not recommendation_df.empty:
        st.markdown("### 🔗 Recommended Properties:")

        for _, row in recommendation_df.iterrows():
            st.markdown(f"🔹 **{row['PropertyName']}**  \n"
                        f"Similarity Score: `{row['SimilarityScore']}`  \n"
                        f"[Visit Website]({row['Link']})", unsafe_allow_html=True)
    else:
        st.error("Apartment not found or similarity data unavailable.")
