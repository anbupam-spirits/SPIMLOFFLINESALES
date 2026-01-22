import gspread
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime

SHEET_ID = "PASTE_YOUR_SHEET_ID"

HEADERS = [
    "Timestamp",
    "STORE NAME AND CONTACT PERSON",
    "PHONE NUMBER",
    "TIME",
    "PHOTOGRAPH",
    "TOBACCO PRODUCTS INTERESTED IN/THEY DEAL IN",
    "ORDER DETAILS IF CONVERTED",
    "CLICK THE LINK TO RECORD LOCATION. DID YOU RECORD THE LOCATION?",
    "STORE CATEGORY",
    "SR NAME",
    "REMARKS",
    "LEAD TYPE",
    "FOLLOW UP DATE",
    "STORE VISIT TYPE",
    "DATE",
    "ADMIN REMARKS",
    "LOCATION LINK"
]

def _get_sheet():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1

# ---------------- WRITE ----------------

def save_visit(data: dict):
    sheet = _get_sheet()
    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),      # Timestamp
        data["store_name"],                                # STORE NAME
        data["phone"],                                     # PHONE NUMBER
        data["time"],                                      # TIME
        data["photo_b64"],                                 # PHOTOGRAPH
        data["products"],                                  # PRODUCTS
        data["order_details"],                             # ORDER DETAILS
        data["location_recorded"],                         # LOCATION RECORDED
        data["store_category"],                            # STORE CATEGORY
        data["sr_name"],                                   # SR NAME
        data["remarks"],                                   # REMARKS
        data["lead_type"],                                 # LEAD TYPE
        data["follow_up_date"],                             # FOLLOW UP DATE
        data["visit_type"],                                # VISIT TYPE
        data["date"],                                      # DATE
        "",                                                 # ADMIN REMARKS
        data["maps_link"]                                  # LOCATION LINK
    ])

# ---------------- READ ----------------

def get_all_store_names():
    sheet = _get_sheet()
    records = sheet.get_all_records()
    return sorted(set(r["STORE NAME AND CONTACT PERSON"] for r in records if r["STORE NAME AND CONTACT PERSON"]))

def get_last_visit(store_name):
    sheet = _get_sheet()
    records = sheet.get_all_records()
    visits = [r for r in records if r["STORE NAME AND CONTACT PERSON"] == store_name]
    return visits[-1] if visits else None
