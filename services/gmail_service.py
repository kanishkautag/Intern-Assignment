import os
import re
import pickle
import time
from typing import List, Set, Optional
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from services.logger import LiveLogger

class GmailService:
    """Handles Gmail API interactions with robust error handling and retries."""
    
    SCOPES: List[str] = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, logger: LiveLogger):
        self.logger = logger
        self.creds = None
        self.service = None

    def authenticate(self, max_retries: int = 3) -> bool:
        """Handles OAuth2.0 authentication with retry logic."""
        attempt = 0
        while attempt < max_retries:
            try:
                self.logger.log("Authenticating with Google", "OAuth2", "STARTED")
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
                self.logger.log("Authenticating with Google", "OAuth2", "SUCCESS")
                return True
            except Exception as e:
                attempt += 1
                status = "RETRIED" if attempt < max_retries else "FAILED"
                self.logger.log(f"Auth Attempt {attempt}: {str(e)}", "OAuth2", status)
                time.sleep(2)
        return False

    def fetch_distinct_recipients(self, sender: str, limit: int = 50) -> List[str]:
        """Fetches messages and cleans emails using Regex."""
        try:
            self.logger.log(f"Fetching emails from {sender}", "Gmail API", "STARTED")
            query = f"from:{sender}"
            results = self.service.users().messages().list(userId='me', q=query, maxResults=limit).execute()
            messages = results.get('messages', [])
            
            recipients: Set[str] = set()
            
            for msg in messages:
                # Check for Abort/Pause signals from UI State
                self._check_execution_signals()
                
                msg_id = msg['id']
                self.logger.log(f"Scanning Header: {msg_id}", "Gmail API", "STARTED")
                
                m_data = self.service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
                headers = m_data.get('payload', {}).get('headers', [])
                
                for h in headers:
                    if h['name'] in ['To', 'Cc', 'Bcc']:
                        parts = h['value'].split(',')
                        for p in parts:
                            email = self._extract_email(p)
                            if email: recipients.add(email)
                
                self.logger.log(f"Scanning Header: {msg_id}", "Gmail API", "SUCCESS")
            
            self.logger.log(f"Found {len(recipients)} unique recipients", "Engine", "SUCCESS")
            return sorted(list(recipients))
        except Exception as e:
            self.logger.log(f"Fetch Error: {str(e)}", "Gmail API", "FAILED")
            raise e

    def _extract_email(self, text: str) -> Optional[str]:
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        return match.group(0).lower() if match else None

    def _check_execution_signals(self):
        """Simulated check for Pause/Abort signals."""
        import streamlit as st
        while st.session_state.get('paused', False):
            time.sleep(0.5)
        if st.session_state.get('abort', False):
            raise InterruptedError("Execution aborted by user.")