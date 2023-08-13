from prefect import task, flow
import prefect

# from prefect.engine.signals import SKIP
import json
import requests
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import logging
from collections import defaultdict
import time
from prefect import unmapped

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Constants
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8000/callback'
TOKEN_FILE = 'token.json'


@task
def load_and_refresh_token():
    def load_token():
        try:
            with open(TOKEN_FILE, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return None

    def save_token(token):
        with open(TOKEN_FILE, 'w') as file:
            json.dump(token, file)

    token = load_token()
    if not token:
        google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=['https://www.googleapis.com/auth/gmail.readonly'])
        authorization_url, state = google.authorization_url('https://accounts.google.com/o/oauth2/auth', access_type="offline", prompt="select_account")
        print(f"Visit this URL: {authorization_url}")
        code = input("Enter the code from the URL: ")
        token = google.fetch_token('https://accounts.google.com/o/oauth2/token', client_secret=CLIENT_SECRET, code=code)
        save_token(token)
    else:
        google = OAuth2Session(CLIENT_ID, token=token)
        if token['expires_at'] <= time.time():
            extra = {
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            }
            token = google.refresh_token('https://accounts.google.com/o/oauth2/token', **extra)
            save_token(token)
    return token


@task
def get_unread_message_ids(token):
    google = OAuth2Session(CLIENT_ID, token=token)
    base_url = 'https://www.googleapis.com/gmail/v1/users/me/messages?q=is:unread in:inbox'
    all_message_ids = []
    page_token = None

    while True:
        url = base_url
        if page_token:
            url += f"&pageToken={page_token}"

        response = google.get(url)
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            all_message_ids.extend([message.get('id') for message in messages])

            page_token = data.get('nextPageToken')
            if not page_token:
                break
        else:
            logging.error(f"Failed to fetch message IDs from URL {url}. Error: {response.json()}")
            break

    return all_message_ids



@task
def fetch_message_details(token, msg_id):
    google = OAuth2Session(CLIENT_ID, token=token)
    msg_data = google.get(f'https://www.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=metadata&metadataHeaders=From')
    if msg_data.status_code == 200:
        headers = msg_data.json().get('payload', {}).get('headers', [])
        from_header = next((header for header in headers if header['name'] == 'From'), None)
        return from_header['value'] if from_header else None
    else:
        print('SKIP2')
        # raise SKIP(f"Failed to get details for message ID {msg_id}.")


@task
def aggregate_message_details(details_list):
    senders_counts = defaultdict(int)
    for sender in details_list:
        senders_counts[sender] += 1
    return sorted(senders_counts.items(), key=lambda x: x[1], reverse=True)

@flow
def gmail_flow():
    token = load_and_refresh_token()
    ids = get_unread_message_ids(token)
    details_list = fetch_message_details.map(token=unmapped(token), msg_id=ids)
    senders_counts = aggregate_message_details(details_list)


# Run the flow
gmail_flow()

# Retrieve results
# senders_counts_result = state.result[senders_counts]._result
# for sender, count in senders_counts_result:
#     logging.info(f"Sender: {sender} - Unread Count: {count}")
