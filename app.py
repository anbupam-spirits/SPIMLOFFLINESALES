import streamlit as st
from gsheets_db import save_visit, get_all_store_names, get_last_visit
from location import get_browser_location, get_ip_location
from PIL import Image
from io import BytesIO
import base64
from datetime import datetime

st.set_page_config("Daily Store Visit", "📝", layout="wide")

# --- LOGIN (simple) ---
if "user" not in st.session_state:
    name = st.text_input("SR Name")
    if st.button("Login"):
        st.session_state.user = name
        st.rerun()

sr_name = st.session_state.user

st.title("Daily Store Visit")

# --- STORE PREFILL ---
stores = get_all_store_names()
store = st.selectbox("Store", ["New"] + stores)

prefill = get_last_visit(store) if store != "New" else {}

phone = st.text_input("Phone", prefill.get("PHONE NUMBER", ""))
visit_type = st.radio("Visit Type", ["NEW VISIT", "RE VISIT"])
category = st.radio("Category", ["MT", "HoReCa"])
lead_type = st.radio("Lead Type", ["HOT", "WARM", "COLD", "DEAD"])
follow_up = st.date_input("Follow Up Date")

products = st.text_input("Products")
order_details = st.text_area("Order Details")
remarks = st.text_area("Remarks")

photo = st.camera_input("Photo")

# --- LOCATION ---
loc = get_browser_location()
lat, lon = None, None

if loc:
    lat, lon = loc["lat"], loc["lon"]
else:
    lat, lon = get_ip_location()

maps_link = f"https://www.google.com/maps?q={lat},{lon}" if lat else ""
location_recorded = "YES" if lat else "NO"

# --- SUBMIT ---
if st.button("Submit"):
    img = Image.open(photo)
    buf = BytesIO()
    img.save(buf, format="JPEG")
    photo_b64 = base64.b64encode(buf.getvalue()).decode()

    save_visit({
        "store_name": store,
        "phone": phone,
        "time": datetime.now().strftime("%H:%M:%S"),
        "photo_b64": photo_b64,
        "products": products,
        "order_details": order_details,
        "location_recorded": location_recorded,
        "store_category": category,
        "sr_name": sr_name,
        "remarks": remarks,
        "lead_type": lead_type,
        "follow_up_date": str(follow_up),
        "visit_type": visit_type,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "maps_link": maps_link
    })

    st.success("✅ Saved to Google Sheet")
