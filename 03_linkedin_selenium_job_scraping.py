import time
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ThreadPoolExecutor, as_completed


from datetime import datetime
import json
import os
from prefect import task, flow
D_TIME = {
    'Past 24 ours': 'f_TPR=r86400',
    'Past Week': 'f_TPR=r604800',
    'Past Month': 'f_TPR=r2592000',
 }
D_WORKTYPE = {
    'On-site': 'f_WT=1',
    'Remote': 'f_WT=2',
    'Hybrid': 'f_WT=3'
}
D_JOBTYPE = {
    'Full-time': 'f_JT=F',
    'Contract': 'f_JT=C'
}
D_SENIORITY = {
    'Mid-Senior': 'f_E=4',
    'Director': 'f_E=5',
    'Executive': 'f_E=6',
 }



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# todo using multiple drivers
# take x urls to download, set the status to pending
# after ready, set the status to ready and fill the scraped at
# at the end save the file, refresh scraped at, set the status to done

# todo add new table for monitoring execution (jobs found, jobs scraped, jobs failed)
# todo add success or not to the database
# todo add record by record? concurrency? use file lock fcntl, or drivers can have temp files
# for german language, we have different name of the button


# todo filter jobs must exist (python) do not exist (C++)


# embedding
# free llm

# todo non showing gui webdriver

# todo notification
# todo parralelization 3 instances
# todo drop exclusion list (may be important later, so keep it)
# todo preinfo non show more
# todo check fields, error handling

# Constants
CONSTANTS = {
    'BROWSE_DOWN_RESULTS_SLEEP_TIME': 6,
    'CLICK_TO_JOB_SLEEP_TIME': 5,
    'SHOW_MORE_BUTTON_DESCRIPTION_SLEEP_TIME': 1,
    'WEBDRIVER_PATH': "C:/Program Files/chromedriver.exe",
    'BASE_URL': 'https://www.linkedin.com/jobs/search?'
}


# Set of previously scraped job IDs
PREVIOUSLY_SCRAPED_JOB_IDS = {"123", "456", "789", '3652076362'}  # Update this set with your real data
# PREVIOUSLY_SCRAPED_JOB_IDS = {"123", "456", "789"}  # Update this set with your real data


class JobURLsDB:
    def __init__(self, filename='database/job_urls.csv'):
        self.filename = filename
        if os.path.exists(filename):
            self.data = pd.read_csv(filename, dtype={'Job ID': str})
        else:
            self.data = pd.DataFrame(columns=['Job ID',
                'Title', 'Keywords', 'Location', 'Time', 'Work Type',
                'Job Type', 'Seniority', 'Generated At', 'Scraped At', 'Status', 'URL'])
            self.data['Status'] = None

    def add_job_urls(self, job_urls):  # job_urls is a list of dictionaries
        # Filter job_urls list to exclude jobs that are already in self.data
        job_urls = [d_job for d_job in job_urls if d_job['Job ID'] not in list(self.data['Job ID'].values)]
        self.data = pd.concat([self.data, pd.DataFrame(job_urls)], ignore_index=True)

    def set_status_to_done(self, job_ids):  # job_ids is a list of job IDs
        self.data.loc[self.data['Job ID'].isin(job_ids), 'Scraped At'] = datetime.now()
        self.data.loc[self.data['Status'].isin(job_ids), 'Done'] = datetime.now()
        # refresh database
        self.save()

    def get_unscraped_jobs(self):
        return self.data.loc[self.data['Scraped At'].isnull()]

    def save(self):
        self.data.to_csv(self.filename, index=False)

class JobDetailsDB:
    def __init__(self, filename='database/job_details.csv'):
        self.filename = filename
        if os.path.exists(filename):
            self.data = pd.read_csv(filename)
        else:
            self.data = pd.DataFrame(
                columns=['Job ID', 'Job Title', 'Company Name', 'Location', 'Date Posted', 'Job URL',
                        'Script Title', 'Script Description', 'Script Hiring Organization',
                        'Script Job Location', 'Script Address', 'Script Address Locality',
                        'Script Address Region', 'Script Industry', 'Script Employment Type',
                        'Script Valid Through', 'Script Skills', 'Script Education Requirements',
                        'Job Description', 'Job Characteristics', 'Scraped At'])

    def add_job_details_to_the_database(self, job_details):  # job_details is a list of dictionaries
        self.data = pd.concat([self.data, pd.DataFrame(job_details)], ignore_index=True)
        self.save()
        logger.info(f"+++++ SAVED +++++ {job_details['Job ID']} saved")

    def get_job_details(self, job_id):
        return self.data.loc[self.data['Job ID'] == job_id]

    def save(self):
        self.data.to_csv(self.filename, index=False)

class WebDriverManager:
    def __init__(self, webdriver_path: str, keywords: str,
                 location: str, time: str, worktype: str, jobtype: str,
                 seniority: str):
        service = Service(webdriver_path)
        url = self.generate_url(keywords, location, time, worktype, jobtype, seniority)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(url)
        self.search_url = url  # Store the search URL

    @classmethod
    def generate_url(cls, keywords: str, location: str,
                     time: str, worktype: str, jobtype: str, seniority: str):
        url = f"{CONSTANTS['BASE_URL']}keywords={keywords}&location={location}"
        if time in D_TIME:
            url += f"&{D_TIME[time]}"
        if worktype in D_WORKTYPE:
            url += f"&{D_WORKTYPE[worktype]}"
        if jobtype in D_JOBTYPE:
            url += f"&{D_JOBTYPE[jobtype]}"
        if seniority in D_SENIORITY:
            url += f"&{D_SENIORITY[seniority]}"
        url += "&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"
        logger.info(f"Generated URL: {url}")
        return url

    @classmethod
    def from_job_urls_db(cls, webdriver_path: str):
        instance = cls.__new__(cls) # Create new instance
        service = Service(webdriver_path)
        instance.driver = webdriver.Chrome(service=service)
        return instance

    # Getter for search URL
    def get_search_url(self):
        return self.search_url

    def get_driver(self):
        return self.driver


class JobURLScraper:
    def __init__(self, driver, search_url, keywords, location,
                 time, worktype, jobtype, seniority):
        self.driver = driver
        self.keywords = keywords
        self.location = location
        self.time = time
        self.worktype = worktype
        self.jobtype = jobtype
        self.seniority = seniority
        self.search_url = search_url
        self.job_urls_db = JobURLsDB('database/job_urls.csv')

    def scrape(self):
        try:
            num_jobs = self._get_num_jobs()
            if num_jobs>0:
                self._browse_down_all_jobs(num_jobs)
                self._get_job_urls()
                self.job_urls_db.save()
        finally:
            self.driver.quit()

    def _get_num_jobs(self):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, 'h1>span')
            num_jobs = self._extract_number(element.get_attribute('innerText'))
            return num_jobs
        except NoSuchElementException:
            print("Element not found")
            return 0

    @staticmethod
    def _extract_number(text):
        return int(text.replace(',', '').replace('+', ''))

    def _browse_down_all_jobs(self, num_jobs, sleep_time=CONSTANTS['BROWSE_DOWN_RESULTS_SLEEP_TIME']):
        num_pages = (num_jobs // 25) + 1
        for page_num in range(2, num_pages + 1):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            logger.info('Browsing page: %s', page_num)

            try:
                button_xpath = "/html/body/div/div/main/section/button"
                self.driver.find_element(By.XPATH, button_xpath).click()
                logger.info('Next page button clicked.')
            except Exception as e:
                logger.info('No next page button found.')
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
                title = job_element.find_element(By.CSS_SELECTOR, 'span').get_attribute('innerText')
                job_urls[job_id] = [title, job_url]
                logger.info(f'Getting job url: {job_id}')
            else:
                logger.info(f'Skipping job: {job_id}')
        self.job_urls_db.add_job_urls([
            {
                'Job ID': str(job_id),
                'Title': information[0],
                'Scraped At': '',
                'Keywords': self.keywords,  # Add the keywords
                'Location': self.location,  # Add the location
                'Time': self.time,  # Add the time
                'Work Type': self.worktype,  # Add the work type
                'Job Type': self.jobtype,  # Add the job type
                'Seniority': self.seniority,  # Add the seniority
                'Generated At': datetime.now(),
                'URL': information[1]
            } for job_id, information in job_urls.items()
        ])
        self.job_urls_db.save()


class JobDetailsScraper:
    def __init__(self, driver, job_urls_db):
        self.driver = driver
        self.job_urls_db = job_urls_db
        self.job_details_db = JobDetailsDB('database/job_details.csv')
        self.results_df = []  # a list to hold all the dataframes

    def start_scraping(self, job_ids):
        # for job_id in job_ids:
        #     pending_job_ids.append(job_id)

        # self.job_urls_db.data.loc[self.job_urls_db.data['Job ID'].isin(pending_job_ids), 'Status'] = 'Pending'
        self.job_urls_db.data.loc[self.job_urls_db.data['Job ID'].isin(job_ids), 'Status'] = 'Pending'
        self.job_urls_db.save()

        # make a list to store job data dicts
        jobs_data = []
        try:
            for job_id in job_ids:
                job_url = self.job_urls_db.data.loc[self.job_urls_db.data['Job ID'] == job_id, 'URL'].iloc[0]
                title = self.job_urls_db.data.loc[self.job_urls_db.data['Job ID'] == job_id, 'Title'].iloc[0]
                logger.info(f'Scraping job: {title}, {job_id}')
                # get the job url
                self.driver.get(job_url)
                time.sleep(CONSTANTS['CLICK_TO_JOB_SLEEP_TIME'])
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
                logger.info(f'job_data: {job_data}')
                # self.job_details_db.add_job_details_to_the_database([job_data])
                # append the job_data dict to the list
                jobs_data.append(job_data)
            # set the status to done in the job urls database
            self.job_urls_db.data.loc[self.job_urls_db.data['Job ID'].isin(job_ids), 'Status'] = 'Done'
            self.job_urls_db.save()
        finally:
            self.driver.quit()

            # convert the jobs data list into a DataFrame
        jobs_df = pd.DataFrame(jobs_data)

        # return the DataFrame
        return jobs_df

    def _collect_job_info(self):
        try:
            jobinfo_path = '// *[ @ id = "main-content"] / section[1] / div / section[2] / div / div[1] / div'
            jobinfo = self.driver.find_element(By.XPATH, jobinfo_path)
            job_title = jobinfo.find_element(By.XPATH, 'h1').text
            company_name = jobinfo.find_element(By.XPATH, 'h4 / div / span').text
            location = jobinfo.find_element(By.XPATH, 'h4 / div / span[2]').text
            script = self.driver.find_element(By.XPATH, "//script[@type='application/ld+json']").get_attribute(
                'innerHTML')
            data = json.loads(script)
            return {
                'Job Title': job_title,
                'Company Name': company_name,
                'Location': location,
                'Script Data': data
            }
        except Exception as e:
            logger.error(f'Error when collecting job info: {e}')
            return None  # or you could return some default values

    def _collect_job_details_by_visiting_the_site(self, job_url):
        try:
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
        except Exception as e:
            logger.error(f'Error when collecting job details: {e}')
            return None, None  # or you could return some default values


def initialize_batch_details_scraper(webdriver_path, job_urls_db, job_ids):
    manager = WebDriverManager.from_job_urls_db(webdriver_path)
    details_scraper = JobDetailsScraper(manager.get_driver(), job_urls_db)
    return details_scraper, job_ids

@task
def initialize_url_scraper(webdriver_path, keywords,
    location, time, worktype, jobtype, seniority):
    manager = WebDriverManager(webdriver_path, keywords, location,
                               time, worktype, jobtype, seniority)
    url_scraper = JobURLScraper(manager.get_driver(), manager.get_search_url(),
        keywords, location, time, worktype, jobtype, seniority)
    return url_scraper

@task
def initialize_details_scraper(webdriver_path, job_urls_db):
    manager = WebDriverManager.from_job_urls_db(webdriver_path)
    details_scraper = JobDetailsScraper(manager.get_driver(), job_urls_db)
    return details_scraper


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
def flow_scrape_urls():
    logger.info('----------------------------')
    logger.info('Starting the scraping of job urls')
    logger.info('----------------------------')
    webdriver_path = CONSTANTS["WEBDRIVER_PATH"]
    keywords = 'Data Scientist'  # You can change these values to your liking
    location = 'United States'
    location = 'Germany'
    location = 'Budapest'
    time = 'Past Week'
    worktype = 'Remote'
    jobtype = 'Contract'
    seniority = None

    url_scraper = initialize_url_scraper(
        webdriver_path, keywords, location, time, worktype, jobtype, seniority)
    scrape(url_scraper)
    job_urls_db = get_job_urls_db(url_scraper)
    save_job_urls_db(job_urls_db)


@flow
def flow_scrape_details():
    logger.info('----------------------------')
    logger.info('Starting the scraping job details')
    logger.info('----------------------------')
    webdriver_path = CONSTANTS["WEBDRIVER_PATH"]
    job_urls_db = JobURLsDB('database/job_urls.csv')

    batch_size = 1  # Set the batch size for processing job URLs
    unscraped_jobs = job_urls_db.get_unscraped_jobs()
    total_jobs_to_scrape = len(unscraped_jobs)

    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, total_jobs_to_scrape, batch_size):
            logger.info(f'Batch {i // batch_size + 1} processing started.')
            batch_job_ids = unscraped_jobs.iloc[i:i + batch_size]['Job ID'].tolist()
            details_scraper, batch_job_ids = initialize_batch_details_scraper(webdriver_path, job_urls_db, batch_job_ids)
            futures.append(
                executor.submit(details_scraper.start_scraping, batch_job_ids))  # Change this to start_scraping

            # executor.submit(details_scraper.scrape_details_for_jobids, batch_job_ids)
            logger.info(f'Batch {i // batch_size + 1} processing ended.')

        # Wait for all tasks to complete and gather results
        for future in as_completed(futures):
            result_df = future.result()  # This will give you the DataFrame returned by the start_scraping function
            details_scraper.results_df.append(result_df)

    # After all tasks are done, you can concatenate all the dataframes and save to your database
    final_df = pd.concat(details_scraper.results_df, ignore_index=True)
    # Here you can save your final_df to database
    print(final_df)

if __name__ == "__main__":
    flow_scrape_urls()
    flow_scrape_details()





