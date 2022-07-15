import streamlit as st
from app_pages import AppPages
from Pages import Introduction, Opportunity

# Create an instance of the app
st.set_page_config(layout="wide")
pages = AppPages()

# Title of the main page
st.title("Objectivity data analysis")

# Register each page that you want to build.
pages.define_page("Introduction", Introduction.build_page)
pages.define_page("Opportunity", Opportunity.build_page)

# The main application.
pages.build_page()