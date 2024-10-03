# Marius Moldovan's Price Scraper

This is a web scraping application built using **Streamlit**. The app allows users to upload an Excel file, which contains product URLs or relevant information, and scrapes the corresponding pricing data. The scraped results are then made available for download as an Excel file.

## Features

- **Upload Excel Files**: Upload an `.xlsx` file containing product data.
- **Automated Web Scraping**: The app runs the `run_scraper` function to scrape product prices.
- **Progress Indicator**: The app shows real-time feedback while scraping is in progress.
- **Download Results**: Once scraping is completed, you can download the output file in Excel format.

## Prerequisites

- Python 3.8+
- Required packages (see below)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/price-scraper.git
   cd price-scraper
