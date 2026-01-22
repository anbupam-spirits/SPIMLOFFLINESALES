import requests
from streamlit_js_eval import streamlit_js_eval

def get_browser_location():
    return streamlit_js_eval(
        js_expressions="""
        new Promise((resolve) => {
            navigator.geolocation.getCurrentPosition(
                pos => resolve({lat: pos.coords.latitude, lon: pos.coords.longitude}),
                () => resolve(null)
            )
        })
        """,
        want_output=True
    )

def get_ip_location():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=3).json()
        lat, lon = r["loc"].split(",")
        return lat, lon
    except:
        return None, None
