# create gcp project

# Go to the Google Cloud Console.
# https://console.cloud.google.com/welcome?project=email-automation-384414
# t..197....gm

# Create a new project.
# Enable the Gmail API (or any other API you're interested in).

# Create OAuth 2.0 client IDs. Choose "Web application".
# Note down the client ID and client secret.

# run server
# from terminal
# python -m http.server 8000

import json
import requests
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import time
import logging
from collections import defaultdict


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Your client ID and secret from the Google Cloud Console
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8000/callback'
TOKEN_FILE = 'token.json'

def save_token(token):
    with open(TOKEN_FILE, 'w') as file:
        json.dump(token, file)

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None


def get_unread_count(google_session):
    base_url = 'https://www.googleapis.com/gmail/v1/users/me/messages?q=is:unread in:inbox'
    total_unread_count = 0
    page_token = None

    logging.info("Fetching unread messages count from Gmail...")  # Starting

    while True:
        url = base_url
        if page_token:
            url += f"&pageToken={page_token}"

        unread_messages_response = google_session.get(url)
        if unread_messages_response.status_code == 200:
            response_data = unread_messages_response.json()
            fetched_count = len(response_data.get('messages', []))
            total_unread_count += fetched_count

            logging.info(f"Fetched {fetched_count}/{total_unread_count} messages from current page...")  # Progress

            # Check for nextPageToken to see if there are more results
            page_token = response_data.get('nextPageToken', None)
            if not page_token:
                break
        else:
            logging.error(f"Error fetching messages: {unread_messages_response.json()}")
            return None

    logging.info("Finished fetching unread messages.")  # Finished
    return total_unread_count


def get_unread_senders_and_counts(google_session):
    base_url = 'https://www.googleapis.com/gmail/v1/users/me/messages?q=is:unread in:inbox'
    senders_counts = defaultdict(int)
    page_token = None

    logging.info("Fetching unread messages senders...")

    while True:
        url = base_url
        if page_token:
            url += f"&pageToken={page_token}"

        unread_messages_response = google_session.get(url)
        if unread_messages_response.status_code == 200:
            response_data = unread_messages_response.json()
            messages = response_data.get('messages', [])

            for message in messages:
                msg_id = message.get('id')
                msg_data = google_session.get(
                    f'https://www.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=metadata&metadataHeaders=From')
                if msg_data.status_code == 200:
                    headers = msg_data.json().get('payload', {}).get('headers', [])
                    from_header = next((header for header in headers if header['name'] == 'From'), None)
                    if from_header:
                        sender = from_header['value']
                        senders_counts[sender] += 1

            # Check for nextPageToken to see if there are more results
            page_token = response_data.get('nextPageToken', None)
            if not page_token:
                break
        else:
            logging.error(f"Error fetching messages: {unread_messages_response.json()}")
            return None

    logging.info("Finished fetching unread messages senders.")
    return sorted(senders_counts.items(), key=lambda x: x[1], reverse=True)



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
    if token['expires_at'] <= time.time():  # Token has expired
        extra = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        }
        token = google.refresh_token('https://accounts.google.com/o/oauth2/token', **extra)
        save_token(token)

# unread_count = get_unread_count(google)
# if unread_count is not None:
#     print(f"You have {unread_count} unread messages.")
# else:
#     print("Could not fetch unread count.")

senders_counts = get_unread_senders_and_counts(google)
for sender, count in senders_counts:
    print(f"Sender: {sender} - Unread Count: {count}")