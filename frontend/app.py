import streamlit as st
from city_locations import loc_kolkata, loc_bangalore, loc_chennai,loc_delhi,loc_hyderabad,loc_mumbai
import requests

API_URL = "http://localhost:8000/predict"
st.title("House Price Prediction System")

city = st.selectbox(
    "Select City",
    ["Kolkata", "Bangalore", "Mumbai", "Chennai", "Hyderabad", "Delhi"]
)

location_mapping = {
    "Kolkata": loc_kolkata,
    "Bangalore": loc_bangalore,
    "Mumbai": loc_mumbai,
    "Chennai": loc_chennai,
    "Hyderabad": loc_hyderabad,
    "Delhi": loc_delhi
}

location = st.selectbox(
    "Select Location",
    location_mapping[city]
)

col1, col2 = st.columns(2)
with col1:
    area = st.number_input("Area (sqft)", min_value=100, max_value=10000, value=530)
    bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=1)
    price_per_sqft = st.number_input("Price per sqft", min_value=1000, value=7735)
    gymnasium = st.selectbox("Gymnasium", [0, 1], index=1)

with col2:
    swimming_pool = st.selectbox("Swimming Pool", [0, 1], index=1)
    ac = st.selectbox("Air Conditioning", [0, 1], index=1)
    gas_connection = st.selectbox("Gas Connection", [0, 1])

resale = st.checkbox("Resale Property", value=True)

if st.button("Predict Price"):
    input_data = {
        "City": city,
        "Location": location,
        "Price_per_sqft": float(price_per_sqft),
        "Area": int(area),
        "Bedrooms": int(bedrooms),
        "Gymnasium": int(gymnasium),
        "SwimmingPool": int(swimming_pool),
        "Resale": bool(resale),
        "AC": int(ac),
        "Gasconnection": int(gas_connection)
    }
    
    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            prediction = response.json().get("price", 0)
            st.success(f"## Predicted Price: ₹{prediction:,.2f}")
        else:
            st.error(f"API Error: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection failed: {str(e)}")


