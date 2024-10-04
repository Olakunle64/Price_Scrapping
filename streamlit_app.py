import streamlit as st
import pandas as pd
import threading
import os
import datetime
from scraper import run_scraper  # Ensure this imports your scraper logic

# Set folders for uploads and results
UPLOAD_FOLDER = './uploads'
RESULTS_FOLDER = './results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Predefined password for authentication
PASSWORD = "123"  # Replace this with your actual password

# List of required columns
REQUIRED_COLUMNS = ['URL', 'XPATH', 'REMARKS', 'RRP']

# Helper function to check for required columns in all sheets
def validate_columns_in_all_sheets(excel_file):
    missing_columns_in_sheets = {}

    # Iterate through all sheets
    for sheet_name, df in excel_file.items():
        missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            missing_columns_in_sheets[sheet_name] = missing_columns

    if missing_columns_in_sheets:
        return False, missing_columns_in_sheets
    return True, None

# Helper function to save uploaded files
def save_uploaded_file(uploaded_file):
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(filepath, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return filepath

# Set the page layout (wide mode can be disabled here)
# st.set_page_config(layout="centered")

st.set_page_config(
    page_title="Marius Scraper",  # Change this to the title you want
    page_icon="🛠️",  # You can use an emoji or a file path to a favicon image (e.g., 'favicon.png')
    layout="centered"
)

# Inject custom CSS to control the title and content
custom_css = """
    <style>
    /* Center the title and add space below it */
    .title-container {
        text-align: center;
        margin-bottom: 30px;  /* Adds space between the title and other components */
    }
    /* Make the main content area centered and limit the width */
    .block-container {
        max-width: 800px;
        margin: auto;
        padding-top: 20px;
    }
    /* Hide the Streamlit branding, settings, and header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(custom_css, unsafe_allow_html=True)

# Custom HTML for the title with a centered style
st.markdown("<div class='title-container'><h1>Welcome to Marius Moldovan's Price Scraper</h1></div>", unsafe_allow_html=True)

# Password input field
password_input = st.text_input("Enter Password to Start Scraping", type="password")

# Streamlit UI for file upload
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Save the uploaded file
    # input_filepath = save_uploaded_file(uploaded_file)
    # st.success(f"File '{uploaded_file.name}' uploaded successfully!")

        # Load the Excel file with all sheets
    try:
        excel_file = pd.read_excel(uploaded_file, sheet_name=None)  # Read all sheets
    except Exception as e:
        st.error("Error reading the Excel file. Please upload a valid file.")
        st.stop()

    # Validate the columns in all sheets
    valid, missing_columns_in_sheets = validate_columns_in_all_sheets(excel_file)

    if not valid:
        for sheet, missing_columns in missing_columns_in_sheets.items():
            st.error(f"Sheet '{sheet}' is missing the following required columns: {', '.join(missing_columns)}")
    else:
        st.success("All sheets contain the required columns.")
        # Save the uploaded file
        # input_filepath = save_uploaded_file(uploaded_file)
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

        # Check password and start scraping if correct
        if st.button("Start Scraping"):
            if password_input == PASSWORD:
                input_filepath = save_uploaded_file(uploaded_file)
                output_filename = f"pricing_{datetime.datetime.now().strftime('%I-%M%p_%d-%m-%Y')}.xlsx"
                output_filepath = os.path.join(RESULTS_FOLDER, output_filename)

                # Run the scraper in a separate thread
                scraper_thread = threading.Thread(target=run_scraper, args=(input_filepath, output_filepath))
                scraper_thread.start()

                st.write("⏳ Please wait... Scraping is in progress...")

                # Wait for the scraping to complete
                scraper_thread.join()

                # Provide the download option after scraping
                if os.path.exists(output_filepath):
                    with open(output_filepath, "rb") as file:
                        st.download_button(
                            label="Download Results",
                            data=file,
                            file_name=output_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            else:
                st.error("❌ Incorrect password. Please try again.")
else:
    st.info("Please upload a valid Excel file to start scraping.")