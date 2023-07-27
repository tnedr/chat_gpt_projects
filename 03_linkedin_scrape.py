import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

def get_job_ids(target_url):
    job_ids = []
    for i in range(math.ceil(117/25)):
        res = requests.get(target_url.format(i))
        soup = BeautifulSoup(res.text,'html.parser')
        jobs = soup.find_all("li")
        for job in jobs:
            job_id = job.find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
            job_ids.append(job_id)
    return job_ids

def get_job_details(job_ids, target_url):
    job_details = []
    for job_id in job_ids:
        res = requests.get(target_url.format(job_id))
        soup = BeautifulSoup(res.text, 'html.parser')
        details = {}

        try:
            details["company"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            details["company"]=None

        try:
            details["job-title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
        except:
            details["job-title"]=None

        try:
            details["level"]=soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
        except:
            details["level"]=None

        job_details.append(details)
    return job_details

def save_to_csv(job_details, file_name):
    df = pd.DataFrame(job_details)
    df.to_csv(file_name, index=False, encoding='utf-8')

def main():
    target_url_jobs = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python%20%28Programming%20Language%29&location=Las%20Vegas%2C%20Nevada%2C%20United%20States&geoId=100293800&currentJobId=3415227738&start={}'
    job_ids = get_job_ids(target_url_jobs)

    target_url_details = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    job_details = get_job_details(job_ids, target_url_details)

    save_to_csv(job_details, 'linkedinjobs.csv')
    print(job_details)

if __name__ == "__main__":
    main()
