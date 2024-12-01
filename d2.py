import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import date

st.set_page_config(page_title="Wide Layout Example", layout="wide")


# Function to connect to Google Sheets
def connect_to_gsheet(sheet_name):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(".streamlit\data-entry-form-Anhad.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet("Staff")  # Replace with your specific sheet name
    return sheet

# Connect to Google Sheets
sheet = connect_to_gsheet("Offline University Contact List")

# Read existing data
data = sheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])  # Assuming first row is headers

# Display the data

left_column, right_column= st.columns([1,4])
# User input for data update
with left_column:
    
    st.subheader("Update Contact Information")

    tier= ['Tier 1', 'Tier 2', 'Tier 3']
    status= ['Not contacted', 'In progress', 'Terminated', 'Successful']
    names= ['Anhad', 'Gurashish', 'Arjun', 'Sumeet', 'kanupriya']

    uni_name = st.text_input("University", )
    tier_type = st.selectbox("Tier", options=tier)
    contact = st.text_input("Contact Name")
    email = st.text_input("Email")
    designation = st.text_input("Designation")
    status_type = st.selectbox("Status", options=status)
    approacher = st.selectbox("Who is contacting?", options=names)
    contact_date = st.date_input("Contact Date", value=date.today())
    follow_up_date = st.date_input("Follow-up Date", value=date.today())
    feedback_comments = st.text_input("Feedback/Comments")

    if st.button("Add Contact"):
        # Prepare data as a new row
        new_row = [
            uni_name,
            tier_type,
            contact,
            email,
            designation,
            status_type,
            approacher,
            contact_date.strftime("%Y-%m-%d"),
            follow_up_date.strftime("%Y-%m-%d"),
            feedback_comments,
            ""  # Empty cell for 'Notes' if needed
        ]
        # Append the new row to the Google Sheet
        sheet.append_row(new_row)
        st.success("New contact added successfully!")

        data = sheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])

with right_column:
    st.header("Existing Contacts Database")
    st.dataframe(df)