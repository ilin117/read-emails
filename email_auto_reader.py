from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# In-memory set to avoid re-processing IDs during a single run
seen = set()


def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def get_unread_message_ids(service):
    ids = []
    page_token = None

    while True:
        resp = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=500,
            fields='messages/id,nextPageToken',
            pageToken=page_token,
        ).execute()

        messages = resp.get('messages', [])
        for m in messages:
            mid = m.get('id')
            if mid and mid not in seen:
                ids.append(mid)

        page_token = resp.get('nextPageToken')
        if not page_token:
            break

    return ids


def mark_emails_as_read():
    service = get_gmail_service()
    ids = get_unread_message_ids(service)

    if not ids:
        return {
            'success': True,
            'marked': 0,
            'message': 'No unread messages to mark.',
        }

    chunk_size = 500
    for i in range(0, len(ids), chunk_size):
        chunk = ids[i:i + chunk_size]
        service.users().messages().batchModify(
            userId='me',
            body={'ids': chunk, 'removeLabelIds': ['UNREAD']},
        ).execute()

    seen.update(ids)
    return {
        'success': True,
        'marked': len(ids),
        'message': f'Successfully marked {len(ids)} message(s) as read.',
    }


if __name__ == '__main__':
    result = mark_emails_as_read()
    print(result)
