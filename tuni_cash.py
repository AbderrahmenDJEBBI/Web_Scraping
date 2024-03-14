from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from datetime import timedelta
import pandas as pd
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
import os

# Define the URL for Tuni.cash
url_tuni_cash = "https://tuni.cash/"

# Define the URL for Remitly
url_remitly = "https://www.remitly.com/fr/en/tunisia/pricing"

# Define the URL for Western Union
url_western_union = "https://www.westernunion.com/fr/fr/currency-converter/eur-to-tnd-rate.html"

# Define the URL for wordremit
url_worldremit = "https://www.worldremit.com/en/tunisia?amountfrom=100.00&selectfrom=fr&currencyfrom=eur&selectto=tn&currencyto=tnd&transfer=csh"

# Define the URL for MyEasyTransfer
url_myeasytransfer = "https://www.myeasytransfer.com/"

# Specify the path to the ChromeDriver executable
chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')

# Create Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

# Add additional options as needed
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-setuid-sandbox')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--disable-browser-side-navigation')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--window-size=1920x1080')
chrome_options.add_argument('--disable-features=VizDisplayCompositor')

# Create a new instance of the Chrome driver with options
driver = webdriver.Chrome(options=chrome_options)

# Open the URL for Tuni.cash
driver.get(url_tuni_cash)

try:
    # Input "1" in the "Vous envoyez" field
    sender_amount_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'sender_amount'))
    )
    sender_amount_input.clear()
    sender_amount_input.send_keys("1")

    # Wait for the exchange rate element to be present
    exchange_rate_element_tuni_cash = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'exchangeRate'))
    )

    # Extract the exchange rate for Tuni.cash
    exchange_rate_tuni_cash = exchange_rate_element_tuni_cash.text.strip()

    # Get the current date and time
    rate_date_time_tuni_cash = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a DataFrame with the exchange rate information for Tuni.cash
    data_tuni_cash = {'Date': [rate_date_time_tuni_cash], 'Source': ['Tuni.cash'], 'Rate': [exchange_rate_tuni_cash]}
    df_tuni_cash = pd.DataFrame(data_tuni_cash)

    # Print the formatted result for Tuni.cash
    print(df_tuni_cash)

except Exception as e:
    print(f"Unable to retrieve the exchange rate from Tuni.cash. Error: {str(e)}")
    df_tuni_cash = pd.DataFrame()  # Initialize an empty DataFrame if an error occurs

finally:
    # Close the browser window for Tuni.cash
    driver.quit()

# Open the URL for Remitly
driver = webdriver.Chrome(options=chrome_options)
driver.get(url_remitly)

try:
    exchange_rate_element_remitly = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'f1f3aw3g'))
    )

    # Extract the exchange rate and currencies for Remitly
    rate_eur_to_tnd_remitly = exchange_rate_element_remitly.find_elements(By.CLASS_NAME, 'f1xrk329')[2].text
    rate_date_time_remitly = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a DataFrame with the exchange rate information for Remitly
    data_remitly = {'Date': [rate_date_time_remitly], 'Source': ['Remitly'], 'Rate': [rate_eur_to_tnd_remitly]}
    df_remitly = pd.DataFrame(data_remitly)

    # Print the formatted result for Remitly
    print(df_remitly)

except Exception as e:
    print(f"Unable to retrieve the exchange rate from Remitly. Error: {str(e)}")
    df_remitly = pd.DataFrame()  # Initialize an empty DataFrame if an error occurs

finally:
    # Close the browser window for Remitly
    driver.quit()

# Create Firefox options for Western Union
firefox_options_wu = Options()
firefox_options_wu.add_argument('--headless')

# Set a user agent string to mimic a regular browser
firefox_options_wu.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Create a new instance of the Firefox driver with options for Western Union
driver_wu = Firefox(options=firefox_options_wu)

# Open the URL for Western Union
driver_wu.get(url_western_union)

try:
    WebDriverWait(driver_wu, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'fx-to'))
    )

    # Wait for the exchange rate to be non-empty for Western Union
    while True:
        exchange_rate_element_wu = driver_wu.find_element(By.CLASS_NAME, 'fx-to')
        exchange_rate_wu = exchange_rate_element_wu.text.strip()
        if exchange_rate_wu:
            break
        time.sleep(1)  # Wait for 1 second before checking again

    # Get the current date and time for Western Union
    current_datetime_wu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a DataFrame with the exchange rate information for Western Union
    data_wu = {'Date': [current_datetime_wu], 'Source': ['Western Union'], 'Rate': [exchange_rate_wu]}
    df_wu = pd.DataFrame(data_wu)

    # Print the formatted output for Western Union
    print(df_wu)

except Exception as e:
    print(f"Unable to retrieve the exchange rate from Western Union. Error: {str(e)}")
    df_wu = pd.DataFrame()  # Initialize an empty DataFrame if an error occurs

finally:
    # Close the browser window for Western Union
    driver_wu.quit()


# Create Firefox options for WorldRemit
firefox_options_worldremit = Options()
firefox_options_worldremit.add_argument('--headless')

# Set a user agent string to mimic a regular browser
firefox_options_worldremit.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Create a new instance of the Firefox driver with options for WorldRemit
driver_worldremit = webdriver.Firefox(options=firefox_options_worldremit)

# Open the URL for WorldRemit
driver_worldremit.get(url_worldremit)

try:
    print("Waiting for the exchange rate element to be present for WorldRemit...")

    # Wait for the element to be visible for WorldRemit
    exchange_rate_element_worldremit = WebDriverWait(driver_worldremit, 40).until(
        EC.visibility_of_element_located((By.XPATH, '//span[@class="MuiTypography-root MuiTypography-h4 css-1csklm7"]/strong'))
    )

    # Extract the exchange rate for WorldRemit
    exchange_rate_worldremit = exchange_rate_element_worldremit.text.strip()

    # Get the current date and time for WorldRemit
    rate_date_time_worldremit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a DataFrame with the exchange rate information for WorldRemit
    data_worldremit = {'Date': [rate_date_time_worldremit], 'Source': ['WorldRemit'], 'Rate': [exchange_rate_worldremit]}
    df_worldremit = pd.DataFrame(data_worldremit)

    # Print the formatted result for WorldRemit
    print(df_worldremit)

except Exception as e:
    print(f"Unable to retrieve the exchange rate from WorldRemit. Error: {str(e)}")
    df_worldremit = pd.DataFrame()  # Initialize an empty DataFrame if an error occurs

finally:
    # Close the browser window for WorldRemit
    driver_worldremit.quit()

# Open the URL for MyEasyTransfer
driver = webdriver.Chrome(options=chrome_options)
driver.get(url_myeasytransfer)

try:
    # Wait for the exchange rate element to be present, with retries and increased waiting time
    exchange_rate_element_myeasytransfer = WebDriverWait(driver, 120, poll_frequency=2).until(
        EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Montant à recevoir")]/following-sibling::input'))
    )

    # Extract the exchange rate from "Montant à recevoir"
    exchange_rate_myeasytransfer = exchange_rate_element_myeasytransfer.get_attribute('value')

    # Convert exchange rate to float and divide by 100
    exchange_rate_myeasytransfer = float(exchange_rate_myeasytransfer) / 100

    # Get the current date and time
    rate_date_time_myeasytransfer = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create a DataFrame with the exchange rate information for MyEasyTransfer
    data_myeasytransfer = {'Date': [rate_date_time_myeasytransfer], 'Source': ['MyEasyTransfer'], 'Rate': [exchange_rate_myeasytransfer]}
    df_myeasytransfer = pd.DataFrame(data_myeasytransfer)

    # Print the formatted result for MyEasyTransfer
    print(df_myeasytransfer)

except Exception as e:
    print(f"Unable to retrieve the exchange rate from MyEasyTransfer. Error: {str(e)}")
    df_myeasytransfer = pd.DataFrame()  # Initialize an empty DataFrame if an error occurs

finally:
    # Close the browser window for MyEasyTransfer
    driver.quit()

# Concatenate the DataFrames for Tuni.cash, Remitly, Western Union, and WorldRemit
df_combined_all = pd.concat([df_tuni_cash, df_remitly, df_wu, df_worldremit], ignore_index=True)

# Modify the Rate column to extract only the numerical part
df_combined_all['Rate'] = df_combined_all['Rate'].str.extract(r'(\d+\.\d+)')
df_combined_all = pd.concat([df_combined_all, df_myeasytransfer], ignore_index=True)

# Convert "Date" column to datetime format
df_combined_all['Date'] = pd.to_datetime(df_combined_all['Date'])

# Add 1 hour to each date
df_combined_all['Date'] += timedelta(hours=1)

# Specify the CSV file path for all data
csv_file_path_all = 'exchange_rate.csv'

# Check if the CSV file exists
if not os.path.isfile(csv_file_path_all):
    # Save the DataFrame to a new CSV file
    df_combined_all.to_csv(csv_file_path_all, index=False)
else:
    # Append to the existing CSV file
    df_combined_all.to_csv(csv_file_path_all, index=False, mode='a', header=False)

# Print the modified DataFrame for all data
print(df_combined_all)

