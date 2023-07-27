import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

from urllib.parse import quote_plus, urlencode


def create_linkedin_job_search_url(keywords, location, geo_id, current_job_id, start):
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

    query_params = {
        'keywords': keywords,
        'location': location,
        'geoId': geo_id,
        'currentJobId': current_job_id,
        'start': start
    }

    query_string = urlencode(query_params, quote_via=quote_plus)

    return f"{base_url}?{query_string}"



l=[]
o={}
k=[]

# Usage
keywords = "Python (Programming Language)"
location = "Las Vegas, Nevada, United States"
geo_id = 100293800
current_job_id = 3415227738
start = 0

target_url = create_linkedin_job_search_url(keywords, location, geo_id, current_job_id, start)
print(target_url)


headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
target_url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python%20%28Programming%20Language%29&location=Las%20Vegas%2C%20Nevada%2C%20United%20States&geoId=100293800&currentJobId=3415227738&start={}'
target_url='https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python%20%28Programming%20Language%29&location=Las%20Vegas%2C%20Nevada%2C%20United%20States&start={}'


for i in range(0,math.ceil(117/25)):

    res = requests.get(target_url.format(i))
    soup=BeautifulSoup(res.text,'html.parser')
    alljobs_on_this_page=soup.find_all("li")
    print(len(alljobs_on_this_page))
    for x in range(0,len(alljobs_on_this_page)):
        jobid = alljobs_on_this_page[x].find("div",{"class":"base-card"}).get('data-entity-urn').split(":")[3]
        l.append(jobid)

target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
for j in range(0,len(l)):

    resp = requests.get(target_url.format(l[j]))
    soup=BeautifulSoup(resp.text,'html.parser')

    try:
        o["company"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        o["company"]=None

    try:
        o["job-title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
    except:
        o["job-title"]=None

    try:
        o["level"]=soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
    except:
        o["level"]=None

    k.append(o)
    o={}

df = pd.DataFrame(k)
print(df)
df.to_csv('linkedinjobs.csv', index=False, encoding='utf-8')
print(k)