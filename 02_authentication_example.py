# from prefect import task, flow
# import prefect

# from prefect.engine.signals import SKIP
import json
import requests
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
import logging
from collections import defaultdict
import time
# from prefect import unmapped
import pickle



# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Constants
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:8000/callback'
TOKEN_FILE = 'token.json'


def save_temporary_results(data, filename):
    """Save data to a file using pickle."""
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_temporary_results(filename):
    """Load data from a file using pickle."""
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError, pickle.PickleError):
        return None

# @task
def load_and_refresh_token():

    logging.info("Loading and refreshing token...")

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

    logging.info("Token loaded and refreshed successfully.")
    return token


# @task
# def get_unread_message_ids(token):
#     logging.info("Fetching unread message IDs...")
#     google = OAuth2Session(CLIENT_ID, token=token)
#     base_url = 'https://www.googleapis.com/gmail/v1/users/me/messages?q=is:unread in:inbox'
#     all_message_ids = []
#     page_token = None
#
#     while True:
#         url = base_url
#         if page_token:
#             url += f"&pageToken={page_token}"
#
#         response = google.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             messages = data.get('messages', [])
#             all_message_ids.extend([message.get('id') for message in messages])
#
#             page_token = data.get('nextPageToken')
#             if not page_token:
#                 break
#         else:
#             logging.error(f"Failed to fetch message IDs from URL {url}. Error: {response.json()}")
#             break
#
#     logging.info(f"Retrieved {len(all_message_ids)} unread message IDs.")
#
#     return all_message_ids


BATCH_SIZE = 100


def get_unread_message_ids(token, start_page_token=None):
    logging.info("Fetching unread message IDs...")
    google = OAuth2Session(CLIENT_ID, token=token)
    base_url = 'https://www.googleapis.com/gmail/v1/users/me/messages?q=is:unread in:inbox'
    all_message_ids = []
    page_token = start_page_token

    while len(all_message_ids) < BATCH_SIZE:
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

    logging.info(f"Retrieved {len(all_message_ids)} unread message IDs.")

    return all_message_ids, page_token




# @task
def fetch_message_details(token, msg_id):
    google = OAuth2Session(CLIENT_ID, token=token)
    msg_data = google.get(f'https://www.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=metadata&metadataHeaders=From')
    if msg_data.status_code == 200:
        headers = msg_data.json().get('payload', {}).get('headers', [])
        from_header = next((header for header in headers if header['name'] == 'From'), None)
        return from_header['value'] if from_header else None
    else:
        logging.error(f"Failed to get details for message ID {msg_id}. Status code: {msg_data.status_code}")
        # raise SKIP(f"Failed to get details for message ID {msg_id}.")

def fetch_message_details_batch(token, msg_ids):
    logging.info("Fetching 'From' header details for message IDs...")
    """
    Fetch 'From' header details for a list of message IDs.

    Args:
    - token (dict): OAuth token
    - msg_ids (list): List of message IDs

    Returns:
    - list: List of 'From' header values
    """
    details = [fetch_message_details(token, msg_id) for msg_id in msg_ids]
    logging.info(f"Fetched 'From' header details for {len(msg_ids)} message IDs.")
    return details


# @task
def aggregate_message_details(details_list):
    logging.info("Aggregating message details...")
    senders_counts = defaultdict(int)
    for sender in details_list:
        senders_counts[sender] += 1
    logging.info(f"Aggregated {len(senders_counts)} senders.")
    return sorted(senders_counts.items(), key=lambda x: x[1], reverse=True)


#todo monitor execution, using pre

# @flow
def gmail_flow():
    token = load_and_refresh_token()
    ids = get_unread_message_ids(token)
    details_list = fetch_message_details_batch(token=token, msg_id=ids)
    # details_list = fetch_message_details.map(token=unmapped(token), msg_id=ids)
    senders_counts = aggregate_message_details(details_list)
    print(senders_counts)


def gmail_flow2():
    logging.info("Starting Gmail2 flow...")
    temp_filename = "temp_results.pkl"
    token = load_and_refresh_token()

    # Load the last saved page token, if any
    last_saved_page_token = load_temporary_results("last_page_token.pkl")

    # Initialize an empty list to store the aggregate results
    all_details_list = []

    while True:
        ids, next_page_token = get_unread_message_ids(token, last_saved_page_token)
        if not ids:
            break

        details_list = fetch_message_details_batch(token=token, msg_ids=ids)

        # Save the details and the last page token
        all_details_list.extend(details_list)
        save_temporary_results(all_details_list, temp_filename)
        save_temporary_results(next_page_token, "last_page_token.pkl")

    # Process and print results
    senders_counts = aggregate_message_details(all_details_list)
    print(senders_counts)
    logging.info("Gmail flow completed successfully.")



# Run the flow
gmail_flow2()

# Retrieve results
# senders_counts_result = state.result[senders_counts]._result
# for sender, count in senders_counts_result:
#     logging.info(f"Sender: {sender} - Unread Count: {count}")
