import time
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import json
import os

# todo drop exclusion list (may be important later, so keep it)
# todo when skipping use already existing data
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
PREVIOUSLY_SCRAPED_JOB_IDS = {"123", "456", "789", '3652076362'}  # Update this set with your real data
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

class WebDriverManager:
    def __init__(self, webdriver_path: str, url: str):
        service = Service(webdriver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(url)
        time.sleep(5)

    def get_driver(self):
        return self.driver


class JobScraper:
    def __init__(self, driver):
        self.driver = driver
        self.job_urls_db = JobURLsDB('job_urls.csv')
        self.job_details_db = JobDetailsDB('job_details.csv')

    def scrape(self):
        num_jobs = self._get_num_jobs()
        self._browse_down_all_jobs(num_jobs)
        self._get_job_urls()
        self._scrape_job_data()
        self.job_urls_db.save()
        self.job_details_db.save()

    def _get_num_jobs(self):
        element = self.driver.find_element(By.CSS_SELECTOR, 'h1>span')
        num_jobs = self._extract_number(element.get_attribute('innerText'))
        return num_jobs

    @staticmethod
    def _extract_number(text):
        return int(text.replace(',', '').replace('+', ''))

    def _browse_down_all_jobs(self, num_jobs, sleep_time=BROWSE_DOWN_RESULTS_SLEEP_TIME):
        num_pages = (num_jobs // 25) + 1
        for page_num in range(2, num_pages + 1):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            logging.info('Browsing page: %s', page_num)
            try:
                button_xpath = "/html/body/div/div/main/section/button"
                self.driver.find_element(By.XPATH, button_xpath).click()
                logging.info('Next page button clicked.')
            except Exception as e:
                logging.error('No next page button found.')
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
                logging.info(f'Getting job url: {job_id}')
            else:
                logging.info(f'Skipping job: {job_id}')
        self.job_urls_db.add_job_urls([{'Job ID': str(job_id), 'URL': url, 'Generated At': datetime.now(), 'Scraped': False} for job_id, url in job_urls.items()])
        self.job_urls_db.save()

    def _scrape_job_data(self):
        unscraped_jobs = self.job_urls_db.get_unscraped_jobs()
        for index, row in unscraped_jobs.iterrows():
            job_id = row['Job ID']  # or whatever the correct column name is
            job_url = row['URL']
            self.driver.get(job_url)
            time.sleep(CLICK_TO_JOB_SLEEP_TIME)
            logging.info(f'Scraping job: {job_id}')
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
        time.sleep(CLICK_TO_JOB_SLEEP_TIME)
        ul_element = self.driver.find_element(By.CLASS_NAME, 'description__job-criteria-list')
        li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
        job_characteristics = {li.find_element(By.CLASS_NAME, 'description__job-criteria-subheader').text:
                               li.find_element(By.CLASS_NAME, 'description__job-criteria-text--criteria').text
                               for li in li_elements}
        self.driver.find_element(By.XPATH, '//button[contains(text(), "Show more")]').click()
        time.sleep(SHOW_MORE_BUTTON_DESCRIPTION_SLEEP_TIME)
        section_element = self.driver.find_element(By.CSS_SELECTOR, "section.show-more-less-html")
        div_element = section_element.find_element(By.CSS_SELECTOR, "div.show-more-less-html__markup")
        job_description = div_element.text.replace('\n', ' ')
        return job_description, job_characteristics


if __name__ == "__main__":
    url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Gyor&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
    manager = WebDriverManager(str(WEBDRIVER_PATH), url)
    scraper = JobScraper(manager.get_driver())
    scraper.scrape()






