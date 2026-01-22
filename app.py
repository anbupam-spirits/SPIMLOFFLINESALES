import streamlit as st
from datetime import datetime
from PIL import Image
from io import BytesIO
import base64

from gsheets_db import save_visit, get_all_store_names, get_last_visit
from location import get_browser_location, get_ip_location

# ======================================================
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# ======================================================
st.set_page_config(
    page_title="Daily Store Visit",
    page_icon="📝",
    layout="wide"
)

# ======================================================
# LOGIN (SAFE STREAMLIT PATTERN)
# ======================================================
if "user" not in st.session_state:
    st.title("Login")

    sr = st.text_input("SR Name")
    if st.button("Login") and sr.strip():
        st.session_state.user = sr.strip()
        st.rerun()

    st.stop()  # ⛔ stop execution until logged in

# ======================================================
# AFTER LOGIN
# ======================================================
sr_name = st.session_state.user

st.title("DAILY STORE VISIT REPORTS")

# ======================================================
# STORE PREFILL (RE VISIT LOGIC)
# ======================================================
stores = get_all_store_names()
store = st.selectbox(
    "STORE NAME AND CONTACT PERSON *",
    ["NEW"] + stores
)

prefill = get_last_visit(store) if store != "NEW" else {}

phone = st.text_input(
    "PHONE NUMBER *",
    value=prefill.get("PHONE NUMBER", "")
)

visit_type = st.radio(
    "STORE VISIT TYPE *",
    ["NEW VISIT", "RE VISIT"],
    horizontal=True
)

store_category = st.radio(
    "STORE CATEGORY *",
    ["MT", "HoReCa"],
    horizontal=True
)

lead_type = st.radio(
    "LEAD TYPE *",
    ["HOT", "WARM", "COLD", "DEAD"],
    horizontal=True
)

follow_up_date = st.date_input("FOLLOW UP DATE")

# ======================================================
# PRODUCTS
# ======================================================
st.markdown("### TOBACCO PRODUCTS INTERESTED IN *")
cols = st.columns(3)
products = []

if cols[0].checkbox("CIGARETTE"): products.append("CIGARETTE")
if cols[1].checkbox("ROLLING PAPERS"): products.append("ROLLING PAPERS")
if cols[2].checkbox("CIGARS"): products.append("CIGARS")
if cols[0].checkbox("HOOKAH"): products.append("HOOKAH")
if cols[1].checkbox("ZIPPO LIGHTERS"): products.append("ZIPPO LIGHTERS")
if cols[2].checkbox("NONE"): products.append("NONE")

order_details = st.text_area("ORDER DETAILS IF CONVERTED")
remarks = st.text_area("REMARKS *")

# ======================================================
# PHOTO
# ======================================================
photo = st.camera_input("PHOTOGRAPH *")

# ======================================================
# LOCATION (BUTTON-BASED – WORKS ON ALL DEVICES)
# ======================================================
st.markdown("### 📍 LOCATION")

if "lat" not in st.session_state:
    st.session_state.lat = None
if "lon" not in st.session_state:
    st.session_state.lon = None

if st.button("📍 RECORD LOCATION"):
    loc = get_browser_location()

    if loc:
        st.session_state.lat = loc["lat"]
        st.session_state.lon = loc["lon"]
    else:
        lat, lon = get_ip_location()
        st.session_state.lat = lat
        st.session_state.lon = lon

if st.session_state.lat:
    maps_link = f"https://www.google.com/maps?q={st.session_state.lat},{st.session_state.lon}"
    st.success("Location captured")
    st.markdown(f"[Open in Google Maps]({maps_link})")
    location_recorded = "YES"
else:
    maps_link = ""
    location_recorded = "NO"

# ======================================================
# SUBMIT
# ======================================================
st.markdown("---")
if st.button("SUBMIT REPORT", type="primary"):

    # ---- Validation ----
    if not store or store == "NEW":
        st.error("Store name is required")
        st.stop()

    if not phone:
        st.error("Phone number is required")
        st.stop()

    if not products:
        st.error("Select at least one product")
        st.stop()

    if not photo:
        st.error("Photograph is required")
        st.stop()

    # ---- Image encoding (TEMP – safe) ----
    img = Image.open(photo)
    buf = BytesIO()
    img.save(buf, format="JPEG")
    photo_b64 = base64.b64encode(buf.getvalue()).decode()

    now = datetime.now()

    save_visit({
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "store_name": store,
        "phone": phone,
        "time": now.strftime("%H:%M:%S"),
        "photo_link": photo_b64,   # later replace with Drive URL
        "products": ", ".join(products),
        "order_details": order_details,
        "location_recorded": location_recorded,
        "store_category": store_category,
        "sr_name": sr_name,
        "remarks": remarks,
        "lead_type": lead_type,
        "follow_up_date": str(follow_up_date),
        "visit_type": visit_type,
        "date": now.strftime("%Y-%m-%d"),
        "maps_link": maps_link,
    })

    st.success("✅ Report Saved Successfully")
    st.balloons()
