import os
import re
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GmailService:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, logger):
        self.logger = logger
        self.creds = None
        self.service = None

    def authenticate(self):
        self.logger.log("Checking OAuth Tokens", "Google Auth", "STARTED")
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('gmail', 'v1', credentials=self.creds)
        self.logger.log("Checking OAuth Tokens", "Google Auth", "SUCCESS")

    def _clean_email(self, raw_string):
        """Helper to extract only the email part using Regex."""
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_string)
        return match.group(0).lower() if match else None

    def fetch_emails(self, sender_email):
        self.logger.log(f"Searching emails from {sender_email}", "Gmail API", "STARTED")
        query = f"from:{sender_email}"
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        recipients = set() # Automatically handles 'distinct' requirement
        
        for msg in messages:
            msg_id = msg['id']
            self.logger.log(f"Processing Msg ID: {msg_id}", "Gmail API", "STARTED")
            
            # Fetching metadata (headers only) for performance/token optimization
            full_msg = self.service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
            headers = full_msg.get('payload', {}).get('headers', [])
            
            for h in headers:
                if h['name'] in ['To', 'Cc', 'Bcc']:
                    # Split comma-separated emails
                    raw_parts = [e.strip() for e in h['value'].split(',')]
                    for part in raw_parts:
                        clean_addr = self._clean_email(part)
                        if clean_addr:
                            recipients.add(clean_addr)
                            
            self.logger.log(f"Processing Msg ID: {msg_id}", "Gmail API", "SUCCESS")
            
        self.logger.log(f"Extracted {len(recipients)} distinct IDs", "Gmail API", "SUCCESS")
        return list(recipients)