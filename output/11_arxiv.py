import feedparser
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import sys
import urllib.parse

# https://info.arxiv.org/help/api/user-manual.html#sort
# https://info.arxiv.org/help/api/user-manual.html#detailed_examples



def get_data_from_arxiv(url):
    feed = feedparser.parse(url)
    data = []

    for entry in feed.entries:
        data.append({
            'title': entry.title,
            'authors': ', '.join(author.name for author in entry.authors),
            'abstract': entry.summary,
            'keywords': entry.tags[0]['term'] if entry.tags else '',
            'publication_date': entry.published,
            'categories': ', '.join(tag.term for tag in entry.tags),
            'journal': entry.arxiv_journal_ref if 'arxiv_journal_ref' in entry else 'Not specified'
        })

    return pd.DataFrame(data)


def search_pandas_df(df, search_term, column):
    return df[df[column].str.contains(search_term, case=False, na=False)]


# AI, ML, CL, MA
# def update_database(cat, max_results=100):
#     search_query = 'cat:' + cat
#     base_url = 'http://export.arxiv.org/api/query?'
#     query = f'search_query={search_query}&start=0&max_results={max_results}'
#     df = get_data_from_arxiv(base_url + query)
#     return df

def get_recent_articles_for(search_query, max_results=100):
    base_url = 'http://export.arxiv.org/api/query?'
    query = f'search_query={search_query}&sortBy=lastUpdatedDate&sortOrder=descending&max_results={max_results}'
    df = get_data_from_arxiv(base_url + query)
    return df

# df = get_recent_articles_for('ti:chatgpt')

# df = get_recent_articles_for('cat:cs.CL&ti:transformer')
df = get_recent_articles_for('cat:cs.CL', max_results=2000)
# df = get_recent_articles_for('ti:electron,thermal,conductivity')

# results = search_pandas_df(df, 'deep learning', 'title')
# Save DataFrame to a CSV file
df.to_csv('arxiv_data.csv', index=False)

# Load DataFrame from a CSV file
df = pd.read_csv('arxiv_data.csv')

