import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from user_agent import user_agents

# Function to extract prices from text using regex
def extract_prices(text):
    prices = re.findall(r'\d+\.\d+|\d+', text)  # Find numeric values in the text
    if prices:
        prices_float = [float(price) for price in prices]  # Convert found prices to float
        return min(prices_float)  # Return the smallest price (in case there are multiple)
    return None

def run_scraper(input_file, output_file):
    # Set up Selenium Chrome WebDriver options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={user_agents}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Load the input Excel file
    xls = pd.ExcelFile(input_file)

    with pd.ExcelWriter(output_file) as writer:
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            results = []  # Store scraped data

            for index, row in df.iterrows():
                # Extract URL, XPATH, REMARKS, and RRP columns
                url = row['URL']
                xpath = row['XPATH']
                remarks = row['REMARKS']
                rrp = row['RRP']

                # Scrape the URL
                try:
                    driver.get(url)  # Navigate to the URL
                    if str(xpath).endswith("text()"):
                        xpath = str(xpath).rstrip("text()")
                    elements = driver.find_elements(By.XPATH, xpath)  # Find elements using XPATH
                    price = "N/A"  # Default value in case price extraction fails

                    # Extract price if elements are found
                    if elements:
                        price_text = elements[0].text  # Get the text from the element
                        extracted_price = extract_prices(price_text)  # Extract the price using the regex function
                        if extracted_price is not None:
                            price = extracted_price  # Assign the extracted price if found

                    # Append the results to the list
                    results.append({
                        'URL': url,
                        'Price': price,  # Scraped and extracted price
                        'REMARKS': remarks,  # Preserve REMARKS from the input
                        'RRP': rrp  # Preserve RRP from the input
                    })
                    print(f"saved row {index} in with {price} to {sheet_name}")
                    time.sleep(10)  # Small delay between requests
                    # break
                except Exception as e:
                    print(f"Error processing {url}: {e}")
                    continue

            # Create a DataFrame for the results and write to Excel
            result_df = pd.DataFrame(results)
            result_df.to_excel(writer, sheet_name=sheet_name, index=False)  # Save sheet data
            print("saved all sheets")
            # break

    # Quit the WebDriver after scraping
    driver.quit()