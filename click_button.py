from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import uuid

# Set up Chrome options
options = webdriver.ChromeOptions()
# Remove the --headless flag
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Specify a unique user data directory
user_data_dir = f"/tmp/chrome-user-data-{uuid.uuid4()}"
options.add_argument(f'--user-data-dir={user_data_dir}')

# Set the User-Agent to mimic a mobile device (e.g., Chrome on Android)
mobile_user_agent = "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
options.add_argument(f'user-agent={mobile_user_agent}')

# Set mobile emulation options
mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": mobile_user_agent,
}
options.add_experimental_option("mobileEmulation", mobile_emulation)

# Disable automation flags
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Add additional options to make the browser appear more like a real browser
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-notifications')

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# Modify navigator.webdriver property to prevent detection
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
    '''
})

try:
    # Open the website
    driver.get('https://mycutebaby.in/contest/participant/679e77f65b140')

    # Wait for the page to load
    time.sleep(10)

    # Print all text from the website (not page source)
    print(driver.find_element(By.TAG_NAME, 'body').text)

    # Find the vote form and print its text
    vote_form = driver.find_element(By.ID, "votefrm_sec")
    print(vote_form.text)

    # Find the button by its ID
    vote_button = driver.find_element(By.ID, 'vote_btn')

    # Scroll the button into view
    driver.execute_script("arguments[0].scrollIntoView(true);", vote_button)
    time.sleep(2)  # Wait for scrolling to complete

    # Use JavaScript to click the button (to bypass overlapping elements)
    driver.execute_script("arguments[0].click();", vote_button)

    print("Vote button clicked successfully!")

    # After clicking the button, wait for 4 seconds and extract all the content from id votefrm_sec
    time.sleep(4)
    vote_form = driver.find_element(By.ID, "votefrm_sec")
    print(vote_form.text)

except Exception as e:
    print(f"An error occurred: {e}")
    print(driver.page_source)  # Print the page source for debugging

finally:
    # Close the browser
    driver.quit()

    # Clean up the user data directory
    if os.path.exists(user_data_dir):
        os.system(f"rm -rf {user_data_dir}")


import socket

def get_ip_addresses():
    try:
        # Get the local machine name (hostname)
        host_name = socket.gethostname()

        # Get the IPv4 address of the machine
        ipv4_address = socket.gethostbyname(host_name)
        print("\nIPv4 Address:", ipv4_address)

        # Get the IPv6 addresses, but handle the case where the system may not have IPv6 support
        ipv6_addresses = []
        try:
            addr_info = socket.getaddrinfo(host_name, None, socket.AF_INET6)
            for info in addr_info:
                ipv6_addresses.append(info[4][0])
            print("IPv6 Addresses:", ipv6_addresses)
        except socket.gaierror:
            print("No IPv6 addresses found or supported in this environment.")

    except socket.gaierror as e:
        print("Error: Could not resolve hostname. Check your network connection or DNS settings.")
        print(f"Details: {e}")

get_ip_addresses()
