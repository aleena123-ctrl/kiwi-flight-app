import streamlit as st
import requests
import pandas as pd

st.title("✈️ Kiwi Flight Price Checker")

origin = st.text_input("From (City Code)", "DEL")
destination = st.text_input("To (City Code)", "SYD")
date = st.text_input("Travel Date (YYYY-MM-DD)", "2024-08-01")

if st.button("Check Flights"):
    url = f"https://api.skypicker.com/flights?fly_from={origin}&fly_to={destination}&date_from={date}&date_to={date}&partner=picky"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", [])
        if data:
            df = pd.DataFrame([{
                "Airline": f.get("airlines", [""])[0],
                "Price (₹)": f.get("price"),
                "From": f.get("cityFrom"),
                "To": f.get("cityTo")
            } for f in data[:10]])
            st.write(df)
        else:
            st.warning("No flights found.")
    else:
        st.error("API error occurred.")
