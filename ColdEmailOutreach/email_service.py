import base64
import os
import pickle
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send',
		  'https://www.googleapis.com/auth/gmail.readonly']

def get_service():
	creds = None
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
			creds = flow.run_local_server(port=0)
		with open("token.json", "w") as token:
			token.write(creds.to_json())
	service = build("gmail", "v1", credentials=creds)
	return service

def create_message(sender, to, subject, body_html):
	message = MIMEText(body_html, "html")
	message["to"] = to
	message["from"] = sender
	message["subject"] = subject
	raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
	return {"raw": raw}

def send_email(to, subject, body_html):
	service = get_service()
	message = create_message("me", to, subject, body_html)
	sent = service.users().messages().send(userId="me", body=message).execute()
	return sent["id"]
