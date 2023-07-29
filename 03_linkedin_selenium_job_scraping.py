import time
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import os

# todo execution
# todo embedding
# todo sleep times
# todo prefect
# todo parralelization
# todo notification
# todo preinfo non show more
# todo check fields, error handling

# Constants
BROWSE_DOWN_RESULTS_SLEEP_TIME = 6
CLICK_TO_JOB_SLEEP_TIME = 6
SHOW_MORE_BUTTON_DESCRIPTION_SLEEP_TIME = 6
WEBDRIVER_PATH = "C:\Program Files\chromedriver.exe"

# Set up logging
logging.basicConfig(level=logging.INFO)

# Your URLs (You're overwriting the url variable, is this intentional?)
url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Gyor&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'

# Set of previously scraped job IDs
PREVIOUSLY_SCRAPED_JOB_IDS = {"123", "456", "789", '3652076362', '3674290696'}  # Update this set with your real data
# PREVIOUSLY_SCRAPED_JOB_IDS = {"123", "456", "789"}  # Update this set with your real data


class JobURLsDB:
    def __init__(self, filename='job_urls.csv'):
        self.filename = filename
        if os.path.exists(filename):
            self.data = pd.read_csv(filename, dtype={'Job ID': str})
        else:
            self.data = pd.DataFrame(columns=['Job ID', 'URL', 'Generated At', 'Scraped'])

    def add_job_urls(self, job_urls):  # job_urls is a list of dictionaries
        # Filter job_urls list to exclude jobs that are already in self.data
        job_urls = [d_job for d_job in job_urls if d_job['Job ID'] not in list(self.data['Job ID'].values)]
        self.data = pd.concat([self.data, pd.DataFrame(job_urls)], ignore_index=True)

    def mark_as_scraped(self, job_ids):  # job_ids is a list of job IDs
        self.data.loc[self.data['Job ID'].isin(job_ids), 'Scraped'] = True

    def get_unscraped_jobs(self):
        return self.data.loc[self.data['Scraped'] == False]

    def save(self):
        self.data.to_csv(self.filename, index=False)

class JobDetailsDB:
    def __init__(self, filename='job_details.csv'):
        self.filename = filename
        if os.path.exists(filename):
            self.data = pd.read_csv(filename)
        else:
            self.data = pd.DataFrame(columns=['Job ID', 'Job Title', 'Company Name', 'Location', 'Date Posted', 'Job URL',
                                              'Script Title', 'Script Description', 'Script Hiring Organization',
                                              'Script Job Location', 'Script Address', 'Script Address Locality',
                                              'Script Address Region', 'Script Industry', 'Script Employment Type',
                                              'Script Valid Through', 'Script Skills', 'Script Education Requirements',
                                              'Job Description', 'Job Characteristics', 'Scraped At'])

    def add_job_details(self, job_details):  # job_details is a list of dictionaries
        self.data = pd.concat([self.data, pd.DataFrame(job_details)], ignore_index=True)

    def get_job_details(self, job_id):
        return self.data.loc[self.data['Job ID'] == job_id]

    def save(self):
        self.data.to_csv(self.filename, index=False)

def extract_number(text):
    return int(text.replace(',', '').replace('+', ''))

def browse_down_all_jobs(driver, num_jobs, sleep_time=BROWSE_DOWN_RESULTS_SLEEP_TIME):
    logging.info('Starting browsing.')
    start_time = time.time()
    num_pages = (num_jobs // 25) + 1

    for page_num in range(2, num_pages + 1):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        logging.info('Browsing page: %s', page_num)
        try:
            button_xpath = "/html/body/div/div/main/section/button"
            driver.find_element(By.XPATH, button_xpath).click()
            logging.info('Next page button clicked.')
        except Exception as e:
            logging.error('No next page button found.')
        time.sleep(sleep_time)

    logging.info('Finished browsing. Total execution time: %s seconds', time.time() - start_time)

def collect_job_info(driver):

    jobinfo_path = '// *[ @ id = "main-content"] / section[1] / div / section[2] / div / div[1] / div'
    jobinfo = driver.find_element(By.XPATH, jobinfo_path)

    # job_title = job.find_element(By.CSS_SELECTOR, 'h3').get_attribute('innerText')
    job_title = jobinfo.find_element(By.XPATH, 'h1').text

    # company_name = job.find_element(By.CSS_SELECTOR, 'h4').get_attribute('innerText')
    company_name = jobinfo.find_element(By.XPATH, 'h4 / div / span').text

    # location = job.find_element(By.CSS_SELECTOR, '[class="job-search-card__location"]').get_attribute('innerText')
    location = jobinfo.find_element(By.XPATH, 'h4 / div / span[2]').text
    # Identify the script tag with the relevant information.
    # You may need to adjust the xpath to accurately target the correct script tag.
    script = driver.find_element(By.XPATH, "//script[@type='application/ld+json']").get_attribute('innerHTML')
    data = json.loads(script)
    script_date_posted = data.get('datePosted', None)
    script_title = data.get('title', None)
    script_description = data.get('description', None)
    script_description = script_description.replace("&lt;", "<").replace("&gt;", ">")
    script_hiringOrganization = data.get('hiringOrganization', None)
    script_name = script_hiringOrganization.get('name', None)
    script_jobLocation = data.get('jobLocation', None)
    script_address = script_jobLocation.get('address', None)
    script_addressLocality = script_address.get('addressLocality', None)
    script_addressRegion = script_address.get('addressRegion', None)
    script_industry = data.get('industry', None)
    script_employmentType = data.get('employmentType', None)
    script_validThrough = data.get('validThrough', None)
    script_skills = data.get('skills', None)
    script_educationRequirements = data.get('educationRequirements', None)

    return job_title, company_name, location, script_date_posted,\
           script_title, script_description, script_hiringOrganization, script_jobLocation, script_address, script_addressLocality, script_addressRegion,\
           script_industry, script_employmentType, script_validThrough, script_skills, script_educationRequirements

def collect_job_details_by_visiting_the_site(driver, job_link):
    driver.get(job_link)
    time.sleep(CLICK_TO_JOB_SLEEP_TIME)

    # Job characteristics
    ul_element = driver.find_element(By.CLASS_NAME, 'description__job-criteria-list')
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    job_characteristics = {li.find_element(By.CLASS_NAME, 'description__job-criteria-subheader').text:
                           li.find_element(By.CLASS_NAME, 'description__job-criteria-text--criteria').text
                           for li in li_elements}

    # Job description
    driver.find_element(By.XPATH, '//button[contains(text(), "Show more")]').click()
    time.sleep(SHOW_MORE_BUTTON_DESCRIPTION_SLEEP_TIME)
    section_element = driver.find_element(By.CSS_SELECTOR, "section.show-more-less-html")
    div_element = section_element.find_element(By.CSS_SELECTOR, "div.show-more-less-html__markup")
    job_description = div_element.text.replace('\n', ' ')
    return job_description, job_characteristics

def get_job_urls(driver):
    job_list = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
    job_elements = job_list.find_elements(By.TAG_NAME, 'li')

    job_urls = {}
    for job_element in job_elements:
        element = job_element.find_element(By.CSS_SELECTOR, 'div[data-entity-urn]')
        job_id = element.get_attribute('data-entity-urn').split(':')[-1]
        if job_id not in PREVIOUSLY_SCRAPED_JOB_IDS:
            job_url = job_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            job_urls[job_id] = job_url
        else:
            logging.info(f'Skipping job: {job_id}')
    return job_urls

def scrape_job_data(driver, job_urls_db, job_details_db):

    unscraped_jobs = job_urls_db.get_unscraped_jobs()
    for index, row in unscraped_jobs.iterrows():
        job_id = row['Job ID']  # or whatever the correct column name is
        job_url = row['URL']
        driver.get(job_url)
        time.sleep(CLICK_TO_JOB_SLEEP_TIME)
        # scrape the job info
        job_title, company_name, location, script_date_posted, \
        script_title, script_description, script_hiringOrganization, script_jobLocation, script_address, script_addressLocality, script_addressRegion, \
        script_industry, script_employmentType, script_validThrough, script_skills, script_educationRequirements \
            = collect_job_info(driver)
        logging.info(f'Scraping job: {job_id}, {job_title}, {company_name}, {location}, {script_date_posted}')
        job_description, job_characteristics = collect_job_details_by_visiting_the_site(driver, job_url)
        job_details_db.add_job_details([
            {
                'Job ID': job_id,
                'Job Title': job_title,
                'Company Name': company_name,
                'Location': location,
                'Date Posted': script_date_posted,
                'Job URL': job_url,
                'Script Title': script_title,
                'Script Description': script_description,
                'Script Hiring Organization': script_hiringOrganization,
                'Script Job Location': script_jobLocation,
                'Script Address': script_address,
                'Script Address Locality': script_addressLocality,
                'Script Address Region': script_addressRegion,
                'Script Industry': script_industry,
                'Script Employment Type': script_employmentType,
                'Script Valid Through': script_validThrough,
                'Script Skills': script_skills,
                'Script Education Requirements': script_educationRequirements,
                'Job Description': job_description,
                'Job Characteristics': job_characteristics,
                'Scraped At': datetime.now()
            }
        ])

        job_urls_db.mark_as_scraped([job_id])

def main():
    # Set up WebDriver
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    time.sleep(5)

    # Get number of jobs
    element = driver.find_element(By.CSS_SELECTOR, 'h1>span')
    num_jobs = extract_number(element.get_attribute('innerText'))

    # Browse all jobs
    browse_down_all_jobs(driver, num_jobs)

    # Initialize databases
    job_urls_db = JobURLsDB('job_urls.csv')
    job_details_db = JobDetailsDB('job_details.csv')

    # Get job urls
    job_urls = get_job_urls(driver)
    job_urls_db.add_job_urls([{'Job ID': str(job_id), 'URL': url, 'Generated At': datetime.now(), 'Scraped': False} for job_id, url in job_urls.items()])
    job_urls_db.save()

    # Scrape job data
    scrape_job_data(driver, job_urls_db, job_details_db)

    # Save the data
    job_urls_db.save()
    job_details_db.save()

if __name__ == "__main__":
    main()
