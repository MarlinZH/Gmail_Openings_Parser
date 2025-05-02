from __future__ import print_function
import os.path
import Gmail_Server_Auth
# import XMind_Maps_to_Dict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from notion_integration import NotionDatabase
from email_vectorizer import EmailVectorizer
import base64
from email.mime.text import MIMEText
import json
from typing import Dict, List

#https://developers.google.com/gmail/api/quickstart/python

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Initialize Notion and Vectorizer
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
notion_db = NotionDatabase(NOTION_API_KEY, NOTION_DATABASE_ID)
vectorizer = EmailVectorizer()

def get_email_content(service, message_id: str) -> Dict:
    """
    Get full email content including body
    Args:
        service: Gmail API service
        message_id: ID of the email message
    Returns:
        Dictionary containing email data
    """
    message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    
    headers = message['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
    date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
    
    # Get email body
    if 'parts' in message['payload']:
        parts = message['payload']['parts']
        data = parts[0]['body']['data']
    else:
        data = message['payload']['body']['data']
    
    data = data.replace("-", "+").replace("_", "/")
    decoded_data = base64.b64decode(data)
    content = decoded_data.decode('utf-8')
    
    return {
        'id': message_id,
        'subject': subject,
        'from': sender,
        'date': date,
        'content': content
    }

def process_emails(service, search_query: str):
    """
    Process emails matching the search query
    Args:
        service: Gmail API service
        search_query: Search query for emails
    """
    try:
        # Get emails matching the search query
        emails = service.users().messages().list(userId='me', q=search_query).execute()
        messages = emails.get('messages', [])
        
        if not messages:
            print('No emails found matching the criteria.')
            return
        
        print(f'Found {len(messages)} emails to process')
        
        for message in messages:
            # Get full email content
            email_data = get_email_content(service, message['id'])
            
            # Vectorize the email
            email_data = vectorizer.vectorize_email(email_data)
            
            # Find similar emails in Notion
            existing_emails = notion_db.get_pages()
            similar_emails = vectorizer.find_similar_emails(email_data, existing_emails)
            
            if similar_emails:
                print(f"Found {len(similar_emails)} similar emails for: {email_data['subject']}")
                for similar in similar_emails:
                    print(f"Similarity: {similar['similarity']:.2f} - {similar['email']['subject']}")
            
            # Store in Notion
            notion_db.create_page(email_data)
            print(f"Stored email in Notion: {email_data['subject']}")
            
    except HttpError as error:
        print(f'An error occurred: {error}')

def main():
    """Main function to process Gmail messages"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\Froap\_DEV\Gmail_Openings_Parser\resi.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # Example search query - modify as needed
        search_query = "subject:(SQL)"
        process_emails(service, search_query)
        
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
Gmail_Server_Auth.authorize