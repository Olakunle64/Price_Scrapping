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

# Helper function to save uploaded files
def save_uploaded_file(uploaded_file):
    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(filepath, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return filepath

# Set the page layout (wide mode can be disabled here)
st.set_page_config(layout="centered")

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

# Streamlit UI
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    # Save the uploaded file
    input_filepath = save_uploaded_file(uploaded_file)
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Button to start scraping
    if st.button("Start Scraping"):
        output_filename = f"pricing_{datetime.datetime.now().strftime('%I-%M%p_%d-%m-%Y')}.xlsx"
        output_filepath = os.path.join(RESULTS_FOLDER, output_filename)

        # Run the scraper in a separate thread
        scraper_thread = threading.Thread(target=run_scraper, args=(input_filepath, output_filepath))
        scraper_thread.start()

        st.write("Scraping in progress... Please wait.")

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
    st.info("Please upload a valid Excel file to start scraping.")
