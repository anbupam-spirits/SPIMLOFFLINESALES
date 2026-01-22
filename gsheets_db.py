import gspread
import streamlit as st
from google.oauth2.service_account import Credentials
from datetime import datetime

SHEET_ID = "1Y6Lv7Ui5d3ESmRMOuBq5beW1_0SxaBwfPYyJfTjfMb8"

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

def save_visit(data):
    sheet = get_sheet()

    row = [
        data["timestamp"],                       # Timestamp
        data["store_name"],                      # STORE NAME AND CONTACT PERSON
        data["phone"],                           # PHONE NUMBER
        data["time"],                            # TIME
        data["photo_link"],                      # PHOTOGRAPH (Drive link)
        data["products"],                        # TOBACCO PRODUCTS
        data["order_details"],                   # ORDER DETAILS
        data["location_recorded"],               # LOCATION RECORDED (YES/NO)
        data["store_category"],                  # STORE CATEGORY
        data["sr_name"],                         # SR NAME
        data["remarks"],                         # REMARKS
        data["lead_type"],                       # LEAD TYPE
        data["follow_up_date"],                  # FOLLOW UP DATE
        data["visit_type"],                      # STORE VISIT TYPE
        data["date"],                            # DATE
        "",                                      # ADMIN REMARKS
        data["maps_link"],                       # LOCATION LINK
    ]

    # Ensure all values are strings
    row = ["" if v is None else str(v) for v in row]

    sheet.append_row(row, value_input_option="USER_ENTERED")

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
