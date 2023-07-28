import time
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import json

# todo multiple phase
# todo database
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
    # element = job.find_element(By.CSS_SELECTOR, 'div[data-entity-urn]')
    # job_id = element.get_attribute('data-entity-urn').split(':')[-1]

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

    # date_posted = driver.find_element(By.CSS_SELECTOR, 'div > div > time').get_attribute('datetime')
    # job_link = job.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
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

    # Collect job info and details
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

    job_info_list = []
    job_details_list = []
    for job_id, job_url in job_urls.items():
        driver.get(job_url)
        time.sleep(CLICK_TO_JOB_SLEEP_TIME)
        job_title, company_name, location, script_date_posted, \
        script_title, script_description, script_hiringOrganization, script_jobLocation, script_address, script_addressLocality, script_addressRegion, \
        script_industry, script_employmentType, script_validThrough, script_skills, script_educationRequirements\
            = collect_job_info(driver)
        logging.info(f'Scraping job: {job_id}, {job_title}, {company_name}, {location}, {script_date_posted}')
        job_info_list.append((job_id, job_title, company_name, location, script_date_posted, job_url,
                              script_title, script_description, script_hiringOrganization, script_jobLocation,
                              script_address, script_addressLocality, script_addressRegion,
                              script_industry, script_employmentType, script_validThrough, script_skills,
                              script_educationRequirements))
        job_details_list.append(collect_job_details_by_visiting_the_site(driver, job_url))

    # Create DataFrames and save to CSV
    df_jobs = pd.DataFrame(job_info_list,
                           columns=['Job ID', 'Job Title', 'Company Name', 'Location', 'Date Posted', 'Job url',
                                    'Script Title', 'Script Description', 'Script Hiring Organization', 'Script Job Location',
                                    'Script Address', 'Script Address Locality', 'Script Address Region',
                                    'Script Industry', 'Script Employment Type', 'Script Valid Through', 'Script Skills',
                                    'Script Education Requirements'])
    df_descriptions = pd.DataFrame([desc for desc, _ in job_details_list], columns=['Job Description'])
    df_characteristics = pd.DataFrame([charac for _, charac in job_details_list])
    df = pd.concat([df_jobs, df_descriptions, df_characteristics], axis=1)

    # Add the date and time of scraping to the DataFrame
    df['Scraped at'] = datetime.now()

    df.to_csv('linkedin_jobs.csv', index=False)

if __name__ == "__main__":
    main()
