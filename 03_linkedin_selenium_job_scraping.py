import time
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import json
import os
from prefect import task, flow

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# todo parralelization
# todo execution
# todo embedding
# todo drop exclusion list (may be important later, so keep it)
# todo how to pass logger to prefect logger?
# todo notification
# todo preinfo non show more
# todo check fields, error handling

# Constants
CONSTANTS = {
    'BROWSE_DOWN_RESULTS_SLEEP_TIME': 6,
    'CLICK_TO_JOB_SLEEP_TIME': 5,
    'SHOW_MORE_BUTTON_DESCRIPTION_SLEEP_TIME': 1,
    'WEBDRIVER_PATH': "C:\\Program Files\\chromedriver.exe",
    'BASE_URL': 'https://www.linkedin.com/jobs/search?'
}


# Set of previously scraped job IDs
PREVIOUSLY_SCRAPED_JOB_IDS = {"123", "456", "789", '3652076362'}  # Update this set with your real data
# PREVIOUSLY_SCRAPED_JOB_IDS = {"123", "456", "789"}  # Update this set with your real data


class JobURLsDB:
    def __init__(self, filename='job_urls.csv'):
        self.filename = filename
        if os.path.exists(filename):
            self.data = pd.read_csv(filename, dtype={'Job ID': str})
        else:
            self.data = pd.DataFrame(columns=['Job ID', 'URL', 'Search URL', 'Keywords', 'Location', 'Generated At', 'Scraped'])

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

class WebDriverManager:
    def __init__(self, webdriver_path: str, keywords: str, location: str):
        service = Service(webdriver_path)
        url = f"{CONSTANTS['BASE_URL']}keywords={keywords}&location={location}&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(url)
        self.search_url = url  # Store the search URL
        # time.sleep(5)

    # Getter for search URL
    def get_search_url(self):
        return self.search_url

    def get_driver(self):
        return self.driver

class JobScraper:
    def __init__(self, driver, search_url, keywords, location):
        self.driver = driver
        self.search_url = search_url
        self.keywords = keywords
        self.location = location
        self.job_urls_db = JobURLsDB('job_urls.csv')
        self.job_details_db = JobDetailsDB('job_details.csv')


    def scrape(self):
        try:
            num_jobs = self._get_num_jobs()
            self._browse_down_all_jobs(num_jobs)
            self._get_job_urls()
            self._scrape_job_data()
            self.job_urls_db.save()
            self.job_details_db.save()
        finally:
            self.driver.quit()

    def _get_num_jobs(self):
        element = self.driver.find_element(By.CSS_SELECTOR, 'h1>span')
        num_jobs = self._extract_number(element.get_attribute('innerText'))
        return num_jobs

    @staticmethod
    def _extract_number(text):
        return int(text.replace(',', '').replace('+', ''))

    def _browse_down_all_jobs(self, num_jobs, sleep_time=CONSTANTS['BROWSE_DOWN_RESULTS_SLEEP_TIME']):
        num_pages = (num_jobs // 25) + 1
        for page_num in range(2, num_pages + 1):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            logger.info('Browsing page: %s', page_num)

            # try:
            #     button_xpath = "/html/body/div/div/main/section/button"
            #     wait = WebDriverWait(self.driver, CONSTANTS['BROWSE_DOWN_RESULTS_SLEEP_TIME'])
            #     button_element = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
            #     button_element.click()
            #     logger.info('Next page button clicked.')
            # except TimeoutException as e:
            #     logger.error('No next page button found.')


            try:
                button_xpath = "/html/body/div/div/main/section/button"
                self.driver.find_element(By.XPATH, button_xpath).click()
                logger.info('Next page button clicked.')
            except Exception as e:
                logger.error('No next page button found.')
            time.sleep(sleep_time)

    def _get_job_urls(self):
        job_list = self.driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
        job_elements = job_list.find_elements(By.TAG_NAME, 'li')

        job_urls = {}
        for job_element in job_elements:
            element = job_element.find_element(By.CSS_SELECTOR, 'div[data-entity-urn]')
            job_id = element.get_attribute('data-entity-urn').split(':')[-1]
            if job_id not in PREVIOUSLY_SCRAPED_JOB_IDS:
                job_url = job_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                job_urls[job_id] = job_url
                logger.info(f'Getting job url: {job_id}')
            else:
                logger.info(f'Skipping job: {job_id}')
        self.job_urls_db.add_job_urls([
            {
                'Job ID': str(job_id),
                'URL': url,
                'Search URL': self.search_url,  # Add the search URL
                'Keywords': self.keywords,  # Add the keywords
                'Location': self.location,  # Add the location
                'Generated At': datetime.now(),
                'Scraped': False
            } for job_id, url in job_urls.items()
        ])
        self.job_urls_db.save()

    def _scrape_job_data(self):
        unscraped_jobs = self.job_urls_db.get_unscraped_jobs()
        for index, row in unscraped_jobs.iterrows():
            job_id = row['Job ID']  # or whatever the correct column name is
            job_url = row['URL']

            self.driver.get(job_url)
            time.sleep(CONSTANTS['CLICK_TO_JOB_SLEEP_TIME'])
            logger.info(f'Scraping job: {job_id}')
            # self.driver.get(job_url)
            # wait = WebDriverWait(self.driver, CONSTANTS['CLICK_TO_JOB_SLEEP_TIME'])
            # try:
            #     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'description__job-criteria-list')))
            #     logger.info(f'Scraping job: {job_id}')
            # except TimeoutException:
            #     logger.error(f'Failed to load job details page: {job_id}')


            # scrape the job info
            job_data = self._collect_job_info()
            job_description, job_characteristics = self._collect_job_details_by_visiting_the_site(job_url)
            job_data.update({
                'Job ID': job_id,
                'Job URL': job_url,
                'Job Description': job_description,
                'Job Characteristics': job_characteristics,
                'Scraped At': datetime.now()
            })
            self.job_details_db.add_job_details([job_data])
            self.job_urls_db.mark_as_scraped([job_id])

    def _collect_job_info(self):
        jobinfo_path = '// *[ @ id = "main-content"] / section[1] / div / section[2] / div / div[1] / div'
        jobinfo = self.driver.find_element(By.XPATH, jobinfo_path)
        job_title = jobinfo.find_element(By.XPATH, 'h1').text
        company_name = jobinfo.find_element(By.XPATH, 'h4 / div / span').text
        location = jobinfo.find_element(By.XPATH, 'h4 / div / span[2]').text
        script = self.driver.find_element(By.XPATH, "//script[@type='application/ld+json']").get_attribute('innerHTML')
        data = json.loads(script)
        return {
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'Script Data': data
        }

    def _collect_job_details_by_visiting_the_site(self, job_url):
        self.driver.get(job_url)
        time.sleep(CONSTANTS['CLICK_TO_JOB_SLEEP_TIME'])
        ul_element = self.driver.find_element(By.CLASS_NAME, 'description__job-criteria-list')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        job_characteristics = {li.find_element(By.CLASS_NAME, 'description__job-criteria-subheader').text:
                               li.find_element(By.CLASS_NAME, 'description__job-criteria-text--criteria').text
                               for li in li_elements}
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Show more")]').click()
        time.sleep(CONSTANTS['SHOW_MORE_BUTTON_DESCRIPTION_SLEEP_TIME'])
        section_element = self.driver.find_element(By.CSS_SELECTOR, "section.show-more-less-html")
        div_element = section_element.find_element(By.CSS_SELECTOR, "div.show-more-less-html__markup")
        job_description = div_element.text.replace('\n', ' ')
        return job_description, job_characteristics


# Tasks
@task
def initialize_scraper(webdriver_path, keywords, location):
    manager = WebDriverManager(webdriver_path, keywords, location)
    scraper = JobScraper(manager.get_driver(), manager.get_search_url(), keywords, location)
    return scraper

@task
def scrape(scraper):
    scraper.scrape()

@task
def get_job_urls_db(scraper):
    return scraper.job_urls_db

@task
def get_job_details_db(scraper):
    return scraper.job_details_db

@task
def save_job_urls_db(job_urls_db):
    job_urls_db.save()

@task
def save_job_details_db(job_details_db):
    job_details_db.save()

# @flow(task_runner=SequentialTaskRunner(),
# name='towering-infernflow')
@flow
def whole_process():
    webdriver_path = CONSTANTS["WEBDRIVER_PATH"]
    keywords = 'Data Scientist'  # You can change these values to your liking
    location = 'Gyor'
    scraper = initialize_scraper(webdriver_path, keywords, location)

    scrape(scraper)

    job_urls_db = get_job_urls_db(scraper)
    job_details_db = get_job_details_db(scraper)

    save_job_urls_db(job_urls_db)
    save_job_details_db(job_details_db)


if __name__ == "__main__":
    whole_process()





