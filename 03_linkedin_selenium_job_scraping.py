
# source
# https://maoviola.medium.com/a-complete-guide-to-web-scraping-linkedin-job-postings-ad290fcaa97f

# needed a chromedriver
# https://googlechromelabs.github.io/chrome-for-testing/#stable

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import sys
import logging
# Set up logging
logging.basicConfig(level=logging.INFO)

url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Toronto%2C%20Ontario%2C%20Canada&geoId=100025096&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Budapest&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Gyor&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'

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

# browse all the jobs
def browse_down_all_jobs(wd, no_of_jobs, sleep_time=5):
    # measure of time to browse all jobs
    start_time = time.time()  # Start time measurement

    i = 2
    no_of_pages = int(no_of_jobs / 25) + 1
    while i <= no_of_pages:
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        logging.info('page: %s', i)
        i += 1

        try:
            button_xpath = "/html/body/div/div/main/section/button"
            wd.find_element(By.XPATH, button_xpath).click()
            logging.info('button clicked')
            time.sleep(sleep_time)
        except Exception as e:
            logging.error('no button at this stage')
            time.sleep(sleep_time)

    execution_time = time.time() - start_time  # Calculate execution time
    logging.info('Execution time: %s seconds', execution_time)

browse_down_all_jobs(wd, no_of_jobs, 3)

job_lists = wd.find_element(By.CLASS_NAME, 'jobs-search__results-list')
jobs = job_lists.find_elements(By.TAG_NAME, 'li')


# get information without clicking to the job
job_id = []
job_title = []
company_name = []
location = []
date = []
job_links = []
for job in jobs:

    element = job.find_element(By.CSS_SELECTOR,'div[data-entity-urn]')
    entity_urn = element.get_attribute('data-entity-urn')
    job_id_temp = entity_urn.split(':')[-1]

    # job_id0 = job.get_attribute('data - id')
    job_id.append(job_id_temp)

    job_title0 = job.find_element(By.CSS_SELECTOR, 'h3').get_attribute('innerText')
    job_title.append(job_title0)

    company_name0 = job.find_element(By.CSS_SELECTOR, 'h4').get_attribute('innerText')
    company_name.append(company_name0)

    location0 = job.find_element(By.CSS_SELECTOR, '[class ="job-search-card__location"]').get_attribute('innerText')
    location.append(location0)

    date0 = job.find_element(By.CSS_SELECTOR, 'div > div > time').get_attribute('datetime')
    date.append(date0)

    job_link0 = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    job_links.append(job_link0)


job_descriptions = []
job_characteristics = []
# for item in range(len(jobs)):
for i, job_link in enumerate(job_links):
    print(i)
    print(job_link)
    # clicking to given job
    # job = wd.find_element(By.CLASS_NAME, 'jobs-search__results-list').find_element(By.XPATH, f'li[{item + 1}]')
    # job_click_path = f'div / a'
    # job_href = job.find_element(By.XPATH, job_click_path).get_attribute('href')
    # wd.get(job_href)
    wd.get(job_link)

    time.sleep(3)

    # get job characteristics seniority, emp_type, job_func, industries
    ul_element = wd.find_element(By.CLASS_NAME, 'description__job-criteria-list')
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    job_criteria = {}
    for li in li_elements:
        header = li.find_element(By.CLASS_NAME, 'description__job-criteria-subheader').text
        text = li.find_element(By.CLASS_NAME, 'description__job-criteria-text--criteria').text
        job_criteria[header] = text
    job_characteristics.append(job_criteria)

    # get job description
    wd.find_element(By.XPATH, '//button[contains(text(), "Show more")]').click()
    time.sleep(2)
    # First, get the 'section' element.
    section_element = wd.find_element(By.CSS_SELECTOR, "section.show-more-less-html")
    # Then, within that section, find the 'div' element.
    div_element = section_element.find_element(By.CSS_SELECTOR, "div.show-more-less-html__markup")
    job_descriptions.append(div_element.text)


# Create a DataFrame from the job details
df_jobs = pd.DataFrame({
    'Job ID': job_id,
    'Job Title': job_title,
    'Company Name': company_name,
    'Location': location,
    'Date Posted': date,
    'Job Link': job_links,
    'Job Description': job_descriptions,
})

# Create a DataFrame from the job characteristics
df_characteristics = pd.DataFrame(job_characteristics)

# Concatenate the two DataFrames along the column axis
df = pd.concat([df_jobs, df_characteristics], axis=1)
