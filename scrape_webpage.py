import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract all the links from a given HTML content
def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

# Function to perform a recursive search for links
def search_links_recursively(url, depth):
    if depth == 0:
        return []

    response = requests.get(url)
    content = response.text
    links = extract_links(content)

    for link in links:
        full_link = url + link if not link.startswith('http') else link
        links.extend(search_links_recursively(full_link, depth - 1))

    return links

# Function to fetch the content of a given URL
def fetch_content(url):
    response = requests.get(url)
    content = response.text
    return content

# Function to save content to a text file and log progress
# Other functions (extract_links, search_links_recursively, fetch_content) remain unchanged

# Function to save content to a text file and log progress
def save_content_to_file(base_url, links, output_file):
    total_links = len(links)
    total_rows = 0

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, link in enumerate(links):
            full_link = base_url + link if not link.startswith('http') else link

            try:
                content = fetch_content(full_link)
                outfile.write(content)
                outfile.write('\n')

                num_rows = len(content.split('\n'))
                total_rows += num_rows

                print(f'Parsing {i + 1}/{total_links} links...')
                print(f'Current link: {full_link}')
                print(f'Current link has {num_rows} rows, merged file has {total_rows} rows.')

            except Exception as e:
                print(f'Error while parsing {full_link}: {e}')

    print(f'Content saved to {output_file}')



# Main code to execute the functions
def main():
    url = 'https://python.langchain.com/en/latest/'
    depth = 1
    output_file = 'merged_content.txt'

    links = search_links_recursively(url, depth)
    links = list(set(links))

    save_content_to_file(url, links, output_file)


    
if __name__ == "__main__":
    main()
