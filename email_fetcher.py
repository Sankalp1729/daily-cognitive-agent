import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime
import re
from typing import List, Dict, Any
import base64

class RealEmailFetcher:
    def __init__(self, email_address: str, password: str = None):
        """
        Initialize email fetcher for Gmail
        
        Args:
            email_address: Gmail address
            password: App password (not regular password)
        """
        self.email_address = email_address
        self.password = password or os.getenv('GMAIL_APP_PASSWORD')
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        
    def connect(self):
        """Connect to Gmail IMAP server"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.mail.login(self.email_address, self.password)
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Gmail"""
        if hasattr(self, 'mail'):
            self.mail.logout()
    
    def clean_text(self, text: str) -> str:
        """Clean email text content"""
        if not text:
            return ""
        
        # Decode if needed
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='ignore')
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove common email artifacts
        text = re.sub(r'\[image:.*?\]', '', text)  # Remove image placeholders
        text = re.sub(r'\[.*?\]', '', text)  # Remove other brackets
        
        # Clean up URLs (make them readable)
        text = re.sub(r'https?://[^\s]+', lambda m: f"🔗 {m.group(0)}", text)
        
        # Clean up excessive whitespace but preserve line breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)  # Remove excessive line breaks
        text = re.sub(r' +', ' ', text)  # Remove multiple spaces
        
        # Clean up the text
        text = text.strip()
        
        return text
    
    def get_email_body(self, msg) -> str:
        """Extract email body from message"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        continue
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                body = str(msg.get_payload())
        
        return self.clean_text(body)
    
    def get_attachments(self, msg) -> List[Dict[str, Any]]:
        """Extract attachment information"""
        attachments = []
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                
                filename = part.get_filename()
                if filename:
                    attachments.append({
                        'name': filename,
                        'size': len(part.get_payload()),
                        'type': part.get_content_type()
                    })
        
        return attachments
    
    def fetch_recent_emails(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch recent emails from inbox"""
        if not self.connect():
            return []
        
        try:
            # Select inbox
            self.mail.select('INBOX')
            
            # Search for recent emails
            _, message_numbers = self.mail.search(None, 'ALL')
            
            # Get the latest emails
            email_list = message_numbers[0].split()
            recent_emails = email_list[-limit:] if len(email_list) > limit else email_list
            
            emails = []
            
            for num in recent_emails:
                try:
                    _, msg_data = self.mail.fetch(num, '(RFC822)')
                    email_body = msg_data[0][1]
                    msg = email.message_from_bytes(email_body)
                    
                    # Extract email details
                    subject = decode_header(msg["subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    sender = decode_header(msg["from"])[0][0]
                    if isinstance(sender, bytes):
                        sender = sender.decode()
                    
                    date = msg["date"]
                    if date:
                        try:
                            parsed_date = email.utils.parsedate_to_datetime(date)
                        except:
                            parsed_date = datetime.now()
                    else:
                        parsed_date = datetime.now()
                    
                    # Determine priority based on subject and sender
                    priority = "medium"
                    if any(word in subject.lower() for word in ["urgent", "asap", "important", "critical"]):
                        priority = "high"
                    elif any(word in subject.lower() for word in ["newsletter", "update", "weekly"]):
                        priority = "low"
                    
                    email_data = {
                        'subject': subject or "No Subject",
                        'sender': sender or "Unknown Sender",
                        'timestamp': parsed_date.isoformat(),
                        'priority': priority,
                        'body': self.get_email_body(msg),
                        'attachments': self.get_attachments(msg),
                        'message_id': msg["message-id"] or f"msg_{num.decode()}",
                        'real_email': True
                    }
                    
                    emails.append(email_data)
                    
                except Exception as e:
                    print(f"❌ Error processing email {num}: {e}")
                    continue
            
            return emails
            
        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return []
        finally:
            self.disconnect()
    
    def fetch_emails_by_sender(self, sender_email: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch emails from a specific sender"""
        if not self.connect():
            return []
        
        try:
            self.mail.select('INBOX')
            
            # Search for emails from specific sender
            search_criteria = f'FROM "{sender_email}"'
            _, message_numbers = self.mail.search(None, search_criteria)
            
            email_list = message_numbers[0].split()
            recent_emails = email_list[-limit:] if len(email_list) > limit else email_list
            
            emails = []
            
            for num in recent_emails:
                try:
                    _, msg_data = self.mail.fetch(num, '(RFC822)')
                    email_body = msg_data[0][1]
                    msg = email.message_from_bytes(email_body)
                    
                    # Extract email details (same as above)
                    subject = decode_header(msg["subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    sender = decode_header(msg["from"])[0][0]
                    if isinstance(sender, bytes):
                        sender = sender.decode()
                    
                    date = msg["date"]
                    if date:
                        try:
                            parsed_date = email.utils.parsedate_to_datetime(date)
                        except:
                            parsed_date = datetime.now()
                    else:
                        parsed_date = datetime.now()
                    
                    priority = "medium"
                    if any(word in subject.lower() for word in ["urgent", "asap", "important", "critical"]):
                        priority = "high"
                    elif any(word in subject.lower() for word in ["newsletter", "update", "weekly"]):
                        priority = "low"
                    
                    email_data = {
                        'subject': subject or "No Subject",
                        'sender': sender or "Unknown Sender",
                        'timestamp': parsed_date.isoformat(),
                        'priority': priority,
                        'body': self.get_email_body(msg),
                        'attachments': self.get_attachments(msg),
                        'message_id': msg["message-id"] or f"msg_{num.decode()}",
                        'real_email': True
                    }
                    
                    emails.append(email_data)
                    
                except Exception as e:
                    print(f"❌ Error processing email {num}: {e}")
                    continue
            
            return emails
            
        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return []
        finally:
            self.disconnect()

# Demo function to test email fetching
def demo_email_fetching():
    """Demo function to test email fetching"""
    print("📧 Real Email Fetcher Demo")
    print("=" * 50)
    
    # You need to set up Gmail App Password
    # 1. Go to Google Account settings
    # 2. Enable 2-factor authentication
    # 3. Generate App Password for this application
    # 4. Set environment variable: GMAIL_APP_PASSWORD=your_app_password
    
    email_address = "blackhole01729@gmail.com"
    app_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not app_password:
        print("❌ GMAIL_APP_PASSWORD environment variable not set!")
        print("📝 To set up:")
        print("1. Enable 2-factor authentication on your Google account")
        print("2. Generate an App Password")
        print("3. Set environment variable: GMAIL_APP_PASSWORD=your_app_password")
        return
    
    fetcher = RealEmailFetcher(email_address, app_password)
    
    print(f"🔗 Connecting to {email_address}...")
    
    # Test connection
    if fetcher.connect():
        print("✅ Connected successfully!")
        fetcher.disconnect()
        
        # Fetch recent emails
        print("\n📬 Fetching recent emails...")
        emails = fetcher.fetch_recent_emails(5)
        
        if emails:
            print(f"✅ Found {len(emails)} emails:")
            for i, email_data in enumerate(emails, 1):
                print(f"\n📧 Email {i}:")
                print(f"   Subject: {email_data['subject']}")
                print(f"   From: {email_data['sender']}")
                print(f"   Date: {email_data['timestamp']}")
                print(f"   Priority: {email_data['priority']}")
                print(f"   Body preview: {email_data['body'][:100]}...")
                print(f"   Attachments: {len(email_data['attachments'])}")
        else:
            print("❌ No emails found or error occurred")
    else:
        print("❌ Failed to connect to Gmail")

if __name__ == "__main__":
    demo_email_fetching()
