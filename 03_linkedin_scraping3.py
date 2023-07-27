# https://maoviola.medium.com/a-complete-guide-to-web-scraping-linkedin-job-postings-ad290fcaa97f

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys

url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Toronto%2C%20Ontario%2C%20Canada&geoId=100025096&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'

def extract_number(text):
    # Remove commas and plus sign, then convert to int
    return int(text.replace(',', '').replace('+', ''))

# Set the path to the Chrome WebDriver executable
webdriver_path = "C:\Program Files\chromedriver.exe"
# Create a service instance with the executable path
service = Service(webdriver_path)

# Create an instance of Chrome WebDriver with the service
wd = webdriver.Chrome(service=service)
wd.get(url)

# step1: to get the number of jobs
# find the first child element of h1 all span
element = wd.find_element(By.CSS_SELECTOR, 'h1>span')
inner_text = element.get_attribute('innerText')
no_of_jobs = extract_number(inner_text)

# no_of_jobs = int(wd.find_element_by_css_selector(‘h1>span’).get_attribute(‘innerText’))
print(no_of_jobs)

sys.exit()

# Create an instance of Chrome WebDriver


# Maximize the browser window
driver.maximize_window()

# Navigate to a website
driver.get("https://www.example.com")

# Find an element by its ID and click on it
# Find an element by its ID using the find_element method
element = driver.find_element(By.ID, "my-button")
element.click()

# Close the browser
driver.quit()

# Close the browser
driver.quit()
url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Toronto%2C%20Ontario%2C%20Canada&geoId=100025096&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'

wd = webdriver.Chrome(executable_path="C:\Program Files\chromedriver.exe")

wd.get(url)

no_of_jobs = int(wd.find_element_by_css_selector('h1>span').get_attribute('innerText'))
print(no_of_jobs)