import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from html2text import HTML2Text


def find_relevant_pages(start_url, filtername):
    try:
        # Send a GET request to the starting URL
        response = requests.get(start_url)
        response.raise_for_status()  # Raise an exception if there's an error
    except requests.exceptions.HTTPError as e:
        print(f"Error accessing {start_url}: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all <a> tags with an 'href' attribute
    links = soup.find_all('a', href=True)

    # Extract the absolute URLs of child pages
    child_pages = []
    for link in links:
        absolute_url = urljoin(start_url, link['href'])
        child_pages.append(absolute_url)

    # Filter out the URLs related to tutorials
    filtered_pages = [url for url in child_pages if filtername in url]

    return filtered_pages


def download_content_of_pages(pages):
    # Create a directory to store the downloaded files
    output_dir = '../langchain_projects/input/prefect2_documentation'
    os.makedirs(output_dir, exist_ok=True)

    # Set up HTML-to-Text converter
    html2text = HTML2Text()
    html2text.ignore_links = True  # Ignore hyperlinks in the text

    # Download the relevant content for each page
    for page in pages:
        # Extract the last part of the URL as the file name
        file_name = page.split('/')[-2] + '.txt'

        # Send a GET request to the page URL
        response = requests.get(page)
        response.raise_for_status()  # Raise an exception if there's an error

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the relevant headings (h1, h2, etc.) and their following paragraphs
        relevant_content = []
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        for heading in headings:
            content = heading.get_text(separator='\n').strip()
            relevant_content.append(content)
            next_element = heading.next_sibling
            while next_element and next_element.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                if next_element.name == 'p':
                    paragraph = next_element.get_text(separator='\n').strip()
                    relevant_content.append(paragraph)
                next_element = next_element.next_sibling

        # Convert the relevant content to plain text
        plain_text = html2text.handle('\n'.join(relevant_content))

        # Save the plain text content as a text file
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(plain_text)

        print(f"Downloaded: {file_path}")


# Example usage
start_url = 'https://docs.prefect.io/2.10.12/'
child_pages = find_relevant_pages(start_url, 'tutorial')
# Print the filtered child page URLs row by row
for page in child_pages:
    print(page)

pages = [
    'https://docs.prefect.io/2.10.12/tutorial/first-steps/',
    'https://docs.prefect.io/2.10.12/tutorial/flow-task-config/',
    'https://docs.prefect.io/2.10.12/tutorial/execution/',
    'https://docs.prefect.io/2.10.12/tutorial/orchestration/',
    'https://docs.prefect.io/2.10.12/tutorial/projects/',
    'https://docs.prefect.io/2.10.12/tutorial/deployments/',
    'https://docs.prefect.io/2.10.12/tutorial/storage/'
]
download_content_of_pages(pages)