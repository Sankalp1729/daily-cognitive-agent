import random
from datetime import datetime, timedelta
import json

class EmailSimulator:
    def __init__(self):
        # Sample senders
        self.senders = [
            "john.doe@company.com",
            "sarah.smith@business.org",
            "mike.wilson@startup.io",
            "lisa.chen@techcorp.com",
            "david.brown@consulting.net",
            "emma.davis@marketing.co",
            "alex.johnson@finance.com",
            "maria.garcia@hr.org",
            "james.lee@operations.io",
            "anna.white@support.net",
            "blackhole01729@gmail.com"  # The specified email
        ]
        
        # Sample subjects
        self.subjects = [
            "Meeting tomorrow at 10 AM",
            "Project update - Q4 results",
            "Urgent: Client feedback needed",
            "Weekly report attached",
            "Question about the budget",
            "Deadline reminder - important",
            "New feature request",
            "Team lunch this Friday?",
            "ASAP: Server maintenance",
            "Monthly newsletter",
            "Invoice #12345",
            "Job application status",
            "Password reset request",
            "Holiday schedule update",
            "Performance review meeting"
        ]
        
        # Sample email bodies
        self.body_templates = [
            "Hi there,\n\nI hope this email finds you well. {content}\n\nBest regards,\n{name}",
            "Hello,\n\n{content}\n\nThanks,\n{name}",
            "Good morning,\n\n{content}\n\nRegards,\n{name}",
            "Hi {name},\n\n{content}\n\nBest,\n{name}",
            "Dear team,\n\n{content}\n\nSincerely,\n{name}"
        ]
        
        # Content variations
        self.content_variations = [
            "I wanted to follow up on our previous discussion about the project timeline. Could you please provide an update on the current status?",
            "We have a new client meeting scheduled for next week. Please review the attached documents before the meeting.",
            "The quarterly results are in and they look promising. I've attached the detailed report for your review.",
            "There's an urgent issue that needs your attention. Can you please call me as soon as possible?",
            "I'm writing to confirm our meeting tomorrow. The agenda has been updated and is attached to this email.",
            "We need your input on the upcoming budget planning session. Your expertise would be valuable.",
            "The new software update is ready for testing. Please let me know if you encounter any issues.",
            "I'm organizing a team building event next month. Please let me know your availability.",
            "There's been a change in the project requirements. I'll need to discuss this with you in detail.",
            "The monthly metrics are now available. I've highlighted the key performance indicators in the report."
        ]
        
        # Names for signatures
        self.names = [
            "John Doe", "Sarah Smith", "Mike Wilson", "Lisa Chen", "David Brown",
            "Emma Davis", "Alex Johnson", "Maria Garcia", "James Lee", "Anna White"
        ]
        
        # Email history for continuity
        self.email_history = []
        
    def generate_email(self, sender=None, subject=None, body=None, timestamp=None):
        """Generate a realistic email"""
        if sender is None:
            sender = random.choice(self.senders)
        
        if subject is None:
            subject = random.choice(self.subjects)
        
        if body is None:
            template = random.choice(self.body_templates)
            content = random.choice(self.content_variations)
            name = random.choice(self.names)
            body = template.format(content=content, name=name)
        
        if timestamp is None:
            # Generate timestamp within last 24 hours
            hours_ago = random.randint(0, 24)
            timestamp = datetime.now() - timedelta(hours=hours_ago)
        
        email_data = {
            'id': f"email_{len(self.email_history) + 1}",
            'sender': sender,
            'subject': subject,
            'body': body,
            'timestamp': timestamp.isoformat(),
            'read': False,
            'priority': random.choice(['low', 'medium', 'high']),
            'attachments': random.choice([[], ['document.pdf'], ['report.xlsx', 'presentation.pptx']])
        }
        
        self.email_history.append(email_data)
        return email_data
    
    def generate_inbox(self, count=10):
        """Generate a full inbox of emails"""
        inbox = []
        for i in range(count):
            email = self.generate_email()
            inbox.append(email)
        
        # Sort by timestamp (newest first)
        inbox.sort(key=lambda x: x['timestamp'], reverse=True)
        return inbox
    
    def generate_specific_email(self, sender="blackhole01729@gmail.com", subject_type="urgent"):
        """Generate a specific type of email for testing"""
        if subject_type == "urgent":
            subject = "URGENT: Action required immediately"
            body = "Hi,\n\nThis is an urgent matter that requires your immediate attention. Please respond as soon as possible.\n\nBest regards,\nSupport Team"
        elif subject_type == "question":
            subject = "Question about your recent order"
            body = "Hello,\n\nI have a question regarding your recent order #12345. Could you please clarify the delivery address?\n\nThanks,\nCustomer Service"
        elif subject_type == "newsletter":
            subject = "Weekly Newsletter - Latest Updates"
            body = "Hi there,\n\nHere's your weekly newsletter with the latest updates and news from our team.\n\nBest regards,\nNewsletter Team"
        else:
            subject = "General inquiry"
            body = "Hello,\n\nI hope this email finds you well. I'm writing to inquire about your services.\n\nBest regards,\nInquiry"
        
        return self.generate_email(sender=sender, subject=subject, body=body)
    
    def get_unread_count(self):
        """Get count of unread emails"""
        return sum(1 for email in self.email_history if not email['read'])
    
    def mark_as_read(self, email_id):
        """Mark an email as read"""
        for email in self.email_history:
            if email['id'] == email_id:
                email['read'] = True
                break
    
    def get_recent_emails(self, hours=24):
        """Get emails from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_emails = []
        
        for email in self.email_history:
            email_time = datetime.fromisoformat(email['timestamp'])
            if email_time >= cutoff_time:
                recent_emails.append(email)
        
        return recent_emails
    
    def save_inbox(self, filename='inbox_data.json'):
        """Save inbox data to file"""
        with open(filename, 'w') as f:
            json.dump(self.email_history, f, indent=2, default=str)
    
    def load_inbox(self, filename='inbox_data.json'):
        """Load inbox data from file"""
        try:
            with open(filename, 'r') as f:
                self.email_history = json.load(f)
        except FileNotFoundError:
            # Start with empty inbox
            self.email_history = [] 