import time
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Constants
BROWSE_DOWN_RESULTS_SLEEP_TIME = 5
CLICK_TO_JOB_SLEEP_TIME = 5
SHOW_MORE_BUTTON_DESCRIPTION_SLEEP_TIME = 5

WEBDRIVER_PATH = "C:\Program Files\chromedriver.exe"

# Set up logging
logging.basicConfig(level=logging.INFO)

# Your URLs (You're overwriting the url variable, is this intentional?)
# url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Toronto%2C%20Ontario%2C%20Canada&geoId=100025096&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
# url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Budapest&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
url = 'https://www.linkedin.com/jobs/search?keywords=Data%20Scientist&location=Gyor&geoId=&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'


def extract_number(text):
    """Extract and return integer from the provided text."""
    return int(text.replace(',', '').replace('+', ''))


def browse_down_all_jobs(driver, num_jobs, sleep_time=BROWSE_DOWN_RESULTS_SLEEP_TIME):
    """Scroll through all jobs on the page."""
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


def collect_job_info(job):
    """Collect and return job info from a job element."""
    element = job.find_element(By.CSS_SELECTOR, 'div[data-entity-urn]')
    job_id = element.get_attribute('data-entity-urn').split(':')[-1]
    job_title = job.find_element(By.CSS_SELECTOR, 'h3').get_attribute('innerText')
    company_name = job.find_element(By.CSS_SELECTOR, 'h4').get_attribute('innerText')
    location = job.find_element(By.CSS_SELECTOR, '[class ="job-search-card__location"]').get_attribute('innerText')
    date_posted = job.find_element(By.CSS_SELECTOR, 'div > div > time').get_attribute('datetime')
    job_link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

    return job_id, job_title, company_name, location, date_posted, job_link


def collect_job_details_by_visiting_the_site(driver, job_link):
    """Collect and return job details by visiting a job link."""
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
    # cleaning description column
    job_description = div_element.text
    job_description = job_description.replace('\n', ' ')

    return job_description, job_characteristics


def main():
    # Set up WebDriver
    service = Service(WEBDRIVER_PATH)
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # Get number of jobs
    element = driver.find_element(By.CSS_SELECTOR, 'h1>span')
    num_jobs = extract_number(element.get_attribute('innerText'))

    # Browse all jobs
    browse_down_all_jobs(driver, num_jobs)

    # Collect job info and details
    job_list = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list')
    jobs = job_list.find_elements(By.TAG_NAME, 'li')
    job_info_list = [collect_job_info(job) for job in jobs]
    job_details_list = [collect_job_details_by_visiting_the_site(driver, job_link) for _, _, _, _, _, job_link in job_info_list]

    # Create DataFrames and save to CSV
    df_jobs = pd.DataFrame(job_info_list,
                           columns=['Job ID', 'Job Title', 'Company Name', 'Location', 'Date Posted', 'Job Link'])
    df_descriptions = pd.DataFrame([desc for desc, _ in job_details_list], columns=['Job Description'])
    df_characteristics = pd.DataFrame([charac for _, charac in job_details_list])
    df = pd.concat([df_jobs, df_descriptions, df_characteristics], axis=1)
    df.to_csv('linkedin_jobs.csv', index=False)


if __name__ == "__main__":
    main()
