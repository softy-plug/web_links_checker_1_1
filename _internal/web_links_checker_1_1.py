import os

# Install required packages via pip
os.system("pip install webdriver-manager")
os.system("pip install selenium")

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Function to read URLs from a text file
def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = file.readlines()
    return [link.strip() for link in links]

# Initialize the WebDriver (Chrome in this case)
def init_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (without GUI)
    service = ChromeService(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    return browser

# Function to check if a link loads successfully and checks for 404 errors
def check_link(browser, url):
    try:
        browser.get(url)
        time.sleep(2)  # Wait for the page to load
        # Check for 404 based on the page title or by searching for elements
        if "404" in browser.title or "Not Found" in browser.page_source or "HTTP ERROR 404" in browser.page_source:
        # or "не найдена" in browser.page_source     
            return False  # Link leads to a 404 page
        if browser.find_element(By.TAG_NAME, 'body'):
            return True  # Page loaded successfully
    except Exception as e:
        print(f"Error accessing {url}: {e}")
    return False  # Catch-all for other issues

# Main function to check all links from the file
def main():
    links = read_links_from_file('links.txt')
    browser = init_browser()

    results = {}
    for link in links:
        success = check_link(browser, link)
        results[link] = success
        print(f"URL: {link} - {'Success' if success else 'Failed (HTTP ERROR 404 or other error)'}")

    browser.quit()

    # Write results to a file
    with open('results.txt', 'w') as result_file:
        for link, status in results.items():
            result_file.write(f"{link} - {'Success' if status else 'Failed (HTTP ERROR 404 or other error)'}\n")

if __name__ == "__main__":
    main()
 
input("Проверка ссылок завершена. Нажмите Enter для закрытия окна")

#softy_plug