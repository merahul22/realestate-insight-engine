



# Real Estate Insight Engine

This project is a comprehensive real estate analysis and recommendation platform built with **Streamlit**. It allows users to search for nearby apartments, receive personalized recommendations based on multiple similarity metrics, and explore pricing trends — all within a fast, interactive web interface.

---

## Features of this App

* **Real-Time Analytics**
  Analyze property listings by sector, price, area, and other parameters using visual insights.

* **Smart Recommendations**
  Get apartment suggestions tailored to your interests using a combination of cosine similarity matrices.

* **Nearby Apartment Search**
  Filter apartments within a specific radius of a selected location using precomputed geospatial distances.

* **Price Prediction Engine** *(Optional Module)*
  Estimate the price of an apartment using a trained regression model.

* **Map Visualizations & Location Insights**
  Understand proximity and geographic layout of properties around a selected point.

* **Property Website Redirection**
  Each recommended apartment comes with a direct link to the official property listing or website.

* **Intelligent Filtering**
  Apply filters such as distance, price, and square footage to refine your property search.

* **Modular Design**
  Structured for easy extension — add modules for scraping, analytics, ML, etc.

---

## Project Structure

```
capstone/
│
├── streamlit/
│   ├── Home.py                      # Main dashboard / landing page
│   ├── latlong-scraper.py          # Latitude and longitude collection script
│   ├── datasets/
│   │   ├── cosine_sim1.pkl         # Cosine similarity matrix (e.g. price-based)
│   │   ├── cosine_sim2.pkl         # Cosine similarity matrix (e.g. amenities/text features)
│   │   ├── cosine_sim3.pkl         # Cosine similarity matrix (e.g. combined features)
│   │   ├── location_distance.pkl   # Pairwise distances between properties (in meters)
│   │   └── price_df.csv            # Price, name, and website links for apartments
│   └── pages/
│       ├── 1_price-predictor.py    # (Optional) Predict price based on input features
│       ├── 2_analytic-module.py    # (Optional) Visual analysis tools
│       └── 3_Recommendation.py     # Core recommendation and filtering module
```

---

## Dataset Descriptions

| File                    | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| `cosine_sim1.pkl`       | Cosine similarity based on price or numerical data     |
| `cosine_sim2.pkl`       | Cosine similarity based on amenities or descriptions   |
| `cosine_sim3.pkl`       | Final combined cosine similarity matrix                |
| `location_distance.pkl` | Pairwise distances (in meters) between locations       |
| `price_df.csv`          | Contains apartment names, price info, and website URLs |

etc.etc 




This file is used to attach a direct URL for each property in the recommendation output.

---

## Installation

Ensure Python 3.8+ is installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the App

From your project root, run the main entry point:

```bash
streamlit run streamlit/Home.py
```

The application will open in your default browser at:
`http://localhost:8501`

---

## How the Recommendation Works

The engine uses **weighted cosine similarity** to find the top-N most similar apartments:

```python
final_similarity = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1.0 * cosine_sim3
```

The user selects a property, and the app recommends similar apartments with their similarity scores and website links.

---

## Future Enhancements

* Integrate user login and saved preferences
* Use geopy/geolocation APIs for dynamic distance computation
* Add mobile responsiveness with Streamlit themes

---

## Author

Developed by **Rahul Chourasiya**
You are welcome to fork, contribute, and suggest improvements.

---



