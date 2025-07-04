import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("✈️ Kiwi Flight Price Checker")

origin = st.text_input("From (City Code)", "DEL")
destination = st.text_input("To (City Code)", "SYD")
date = st.date_input("Travel Date")

if st.button("Check Flights"):
    formatted_date = date.strftime("%d/%m/%Y")  # 👈 Required by Kiwi API

    url = f"https://api.skypicker.com/flights?fly_from={origin}&fly_to={destination}&date_from={formatted_date}&date_to={formatted_date}&partner=picky"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                df = pd.DataFrame([{
                    "From": f.get("cityFrom"),
                    "To": f.get("cityTo"),
                    "Airline": f.get("airlines", [""])[0],
                    "Price (₹)": f.get("price"),
                } for f in data[:10]])
                st.dataframe(df)
            else:
                st.warning("No flights found.")
        else:
            st.error("API request failed. Please try again.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
