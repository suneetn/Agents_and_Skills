#!/usr/bin/env python3
"""
Email Sender via Mailgun API
Handles newsletter distribution with retry logic and archiving
"""

import os
import sys
import csv
import json
import time
import argparse
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


# Configuration
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', 'quanthub.ai')
MAILGUN_FROM = os.environ.get('MAILGUN_FROM', f'QuantHub Daily <newsletter@{MAILGUN_DOMAIN}>')
MAILGUN_API_BASE = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}'

# Paths
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = SKILL_DIR / 'data'
ARCHIVE_DIR = SKILL_DIR / 'archive'
SUBSCRIBERS_FILE = DATA_DIR / 'subscribers.csv'
FAILED_SENDS_FILE = DATA_DIR / 'failed_sends.json'
SEND_LOG_FILE = DATA_DIR / 'send_log.json'

# Retry settings
MAX_RETRIES = 4
RETRY_DELAYS = [0, 30, 120, 300]  # seconds: immediate, 30s, 2min, 5min

# Rate limiting
SEND_DELAY = 1  # seconds between sends
BATCH_SIZE = 50


@dataclass
class Subscriber:
    """Email subscriber"""
    email: str
    name: str = ""
    subscribed_date: str = ""
    active: bool = True


@dataclass
class SendResult:
    """Result of email send operation"""
    sent_count: int
    failed_count: int
    failures: List[Dict]
    message_ids: List[str]
    timestamp: str


class MailgunClient:
    """Mailgun API client"""
    
    def __init__(self, api_key: str, domain: str):
        self.api_key = api_key
        self.domain = domain
        self.base_url = f'https://api.mailgun.net/v3/{domain}'
        
    def send_email(
        self,
        to: str,
        subject: str,
        html: str,
        text: str,
        from_email: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Send a single email
        
        Returns:
            Tuple of (success, message_id, error_message)
        """
        data = {
            'from': from_email or MAILGUN_FROM,
            'to': to,
            'subject': subject,
            'html': html,
            'text': text
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/messages',
                auth=('api', self.api_key),
                data=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return True, result.get('id'), None
            else:
                return False, None, f"HTTP {response.status_code}: {response.text}"
                
        except requests.exceptions.Timeout:
            return False, None, "Request timeout"
        except requests.exceptions.RequestException as e:
            return False, None, str(e)
    
    def send_batch(
        self,
        recipients: List[str],
        subject: str,
        html: str,
        text: str,
        from_email: Optional[str] = None
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """
        Send to multiple recipients with rate limiting
        
        Returns:
            Tuple of (successful_message_ids, failed_recipients_with_errors)
        """
        successes = []
        failures = []
        
        for i, recipient in enumerate(recipients):
            success, msg_id, error = self.send_email(
                to=recipient,
                subject=subject,
                html=html,
                text=text,
                from_email=from_email
            )
            
            if success:
                successes.append(msg_id)
                print(f"  ✅ [{i+1}/{len(recipients)}] Sent to {recipient}")
            else:
                failures.append((recipient, error))
                print(f"  ❌ [{i+1}/{len(recipients)}] Failed: {recipient} - {error}")
            
            # Rate limiting
            if i < len(recipients) - 1:
                time.sleep(SEND_DELAY)
        
        return successes, failures


class SubscriberManager:
    """Manages subscriber list"""
    
    def __init__(self, subscribers_file: Path = SUBSCRIBERS_FILE):
        self.file = subscribers_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create subscribers file if it doesn't exist"""
        self.file.parent.mkdir(parents=True, exist_ok=True)
        if not self.file.exists():
            with open(self.file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['email', 'name', 'subscribed_date', 'active'])
    
    def get_active_subscribers(self) -> List[Subscriber]:
        """Get all active subscribers"""
        subscribers = []
        with open(self.file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('active', 'true').lower() == 'true':
                    subscribers.append(Subscriber(
                        email=row['email'],
                        name=row.get('name', ''),
                        subscribed_date=row.get('subscribed_date', ''),
                        active=True
                    ))
        return subscribers
    
    def get_all_subscribers(self) -> List[Subscriber]:
        """Get all subscribers including inactive"""
        subscribers = []
        with open(self.file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                subscribers.append(Subscriber(
                    email=row['email'],
                    name=row.get('name', ''),
                    subscribed_date=row.get('subscribed_date', ''),
                    active=row.get('active', 'true').lower() == 'true'
                ))
        return subscribers
    
    def add_subscriber(self, email: str, name: str = "") -> bool:
        """Add a new subscriber"""
        # Check if already exists
        existing = self.get_all_subscribers()
        if any(s.email.lower() == email.lower() for s in existing):
            return False
        
        with open(self.file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([email, name, datetime.now().isoformat(), 'true'])
        return True
    
    def remove_subscriber(self, email: str) -> bool:
        """Remove a subscriber (set inactive)"""
        subscribers = self.get_all_subscribers()
        found = False
        
        for sub in subscribers:
            if sub.email.lower() == email.lower():
                sub.active = False
                found = True
        
        if found:
            self._write_all(subscribers)
        return found
    
    def _write_all(self, subscribers: List[Subscriber]):
        """Rewrite all subscribers"""
        with open(self.file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['email', 'name', 'subscribed_date', 'active'])
            for sub in subscribers:
                writer.writerow([sub.email, sub.name, sub.subscribed_date, str(sub.active).lower()])
    
    def import_from_csv(self, import_file: Path) -> int:
        """Import subscribers from another CSV file"""
        count = 0
        with open(import_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get('email') or row.get('Email')
                name = row.get('name') or row.get('Name', '')
                if email and self.add_subscriber(email, name):
                    count += 1
        return count


class NewsletterArchive:
    """Manages newsletter archive"""
    
    def __init__(self, archive_dir: Path = ARCHIVE_DIR):
        self.dir = archive_dir
        self.dir.mkdir(parents=True, exist_ok=True)
    
    def archive_newsletter(
        self,
        html: str,
        text: str,
        subject: str,
        result: SendResult,
        date: Optional[str] = None
    ) -> Path:
        """Archive a sent newsletter"""
        date = date or datetime.now().strftime('%Y-%m-%d')
        archive_path = self.dir / date
        archive_path.mkdir(parents=True, exist_ok=True)
        
        # Save HTML
        with open(archive_path / 'newsletter.html', 'w') as f:
            f.write(html)
        
        # Save text
        with open(archive_path / 'newsletter.txt', 'w') as f:
            f.write(text)
        
        # Save metadata
        metadata = {
            'subject': subject,
            'sent_at': result.timestamp,
            'sent_count': result.sent_count,
            'failed_count': result.failed_count,
            'message_ids': result.message_ids
        }
        with open(archive_path / 'metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return archive_path
    
    def list_archives(self) -> List[Dict]:
        """List all archived newsletters"""
        archives = []
        for path in sorted(self.dir.iterdir(), reverse=True):
            if path.is_dir():
                metadata_file = path / 'metadata.json'
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    metadata['date'] = path.name
                    archives.append(metadata)
        return archives
    
    def get_archive(self, date: str) -> Optional[Dict]:
        """Get a specific archived newsletter"""
        archive_path = self.dir / date
        if not archive_path.exists():
            return None
        
        result = {'date': date}
        
        # Load files
        html_file = archive_path / 'newsletter.html'
        if html_file.exists():
            result['html'] = html_file.read_text()
        
        text_file = archive_path / 'newsletter.txt'
        if text_file.exists():
            result['text'] = text_file.read_text()
        
        metadata_file = archive_path / 'metadata.json'
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                result['metadata'] = json.load(f)
        
        return result


class EmailSender:
    """Main email sender orchestrator"""
    
    def __init__(self):
        self.client = MailgunClient(MAILGUN_API_KEY, MAILGUN_DOMAIN) if MAILGUN_API_KEY else None
        self.subscribers = SubscriberManager()
        self.archive = NewsletterArchive()
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    def send_newsletter(
        self,
        html: str,
        text: str,
        subject: str,
        recipients: Optional[List[str]] = None,
        dry_run: bool = False
    ) -> SendResult:
        """
        Send newsletter to recipients or all subscribers
        
        Args:
            html: HTML content
            text: Plain text content
            subject: Email subject
            recipients: Optional list of recipients (uses subscribers if None)
            dry_run: If True, don't actually send
        """
        # Get recipients
        if recipients:
            target_emails = recipients
        else:
            subs = self.subscribers.get_active_subscribers()
            target_emails = [s.email for s in subs]
        
        if not target_emails:
            print("❌ No recipients found!")
            return SendResult(
                sent_count=0,
                failed_count=0,
                failures=[],
                message_ids=[],
                timestamp=datetime.now().isoformat()
            )
        
        print(f"\n📧 Preparing to send newsletter:")
        print(f"   Subject: {subject}")
        print(f"   Recipients: {len(target_emails)}")
        print(f"   From: {MAILGUN_FROM}")
        
        if dry_run:
            print("\n🔍 DRY RUN - No emails will be sent")
            for email in target_emails:
                print(f"   Would send to: {email}")
            return SendResult(
                sent_count=len(target_emails),
                failed_count=0,
                failures=[],
                message_ids=['dry-run'],
                timestamp=datetime.now().isoformat()
            )
        
        if not self.client:
            print("\n❌ Error: MAILGUN_API_KEY not set!")
            return SendResult(
                sent_count=0,
                failed_count=len(target_emails),
                failures=[{'email': e, 'error': 'API key not configured'} for e in target_emails],
                message_ids=[],
                timestamp=datetime.now().isoformat()
            )
        
        print(f"\n🚀 Sending emails...")
        message_ids, failures = self.client.send_batch(
            recipients=target_emails,
            subject=subject,
            html=html,
            text=text
        )
        
        # Retry failed sends
        if failures:
            print(f"\n🔄 Retrying {len(failures)} failed sends...")
            message_ids, failures = self._retry_failed(
                failures=failures,
                subject=subject,
                html=html,
                text=text
            )
        
        result = SendResult(
            sent_count=len(message_ids),
            failed_count=len(failures),
            failures=[{'email': e, 'error': err} for e, err in failures],
            message_ids=message_ids,
            timestamp=datetime.now().isoformat()
        )
        
        # Log result
        self._log_send(result)
        
        # Log permanent failures
        if failures:
            self._log_failures(failures)
        
        # Archive
        print(f"\n📁 Archiving newsletter...")
        archive_path = self.archive.archive_newsletter(html, text, subject, result)
        print(f"   Saved to: {archive_path}")
        
        # Summary
        print(f"\n{'='*50}")
        print(f"📊 SEND SUMMARY")
        print(f"{'='*50}")
        print(f"   ✅ Sent: {result.sent_count}")
        print(f"   ❌ Failed: {result.failed_count}")
        print(f"   📧 Total: {result.sent_count + result.failed_count}")
        
        return result
    
    def _retry_failed(
        self,
        failures: List[Tuple[str, str]],
        subject: str,
        html: str,
        text: str
    ) -> Tuple[List[str], List[Tuple[str, str]]]:
        """Retry failed sends with exponential backoff"""
        all_message_ids = []
        remaining_failures = failures
        
        for attempt in range(1, MAX_RETRIES):
            if not remaining_failures:
                break
            
            delay = RETRY_DELAYS[attempt]
            print(f"   Retry attempt {attempt}/{MAX_RETRIES-1} in {delay}s...")
            time.sleep(delay)
            
            new_failures = []
            for email, _ in remaining_failures:
                success, msg_id, error = self.client.send_email(
                    to=email,
                    subject=subject,
                    html=html,
                    text=text
                )
                
                if success:
                    all_message_ids.append(msg_id)
                    print(f"   ✅ Retry success: {email}")
                else:
                    new_failures.append((email, error))
            
            remaining_failures = new_failures
        
        return all_message_ids, remaining_failures
    
    def _log_send(self, result: SendResult):
        """Log send result"""
        log = []
        if SEND_LOG_FILE.exists():
            with open(SEND_LOG_FILE, 'r') as f:
                log = json.load(f)
        
        log.append(asdict(result))
        
        # Keep last 100 entries
        log = log[-100:]
        
        with open(SEND_LOG_FILE, 'w') as f:
            json.dump(log, f, indent=2)
    
    def _log_failures(self, failures: List[Tuple[str, str]]):
        """Log permanent failures"""
        existing = []
        if FAILED_SENDS_FILE.exists():
            with open(FAILED_SENDS_FILE, 'r') as f:
                existing = json.load(f)
        
        for email, error in failures:
            existing.append({
                'email': email,
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
        
        with open(FAILED_SENDS_FILE, 'w') as f:
            json.dump(existing, f, indent=2)
    
    def get_status(self) -> Dict:
        """Get sending status"""
        status = {
            'subscribers': len(self.subscribers.get_active_subscribers()),
            'total_subscribers': len(self.subscribers.get_all_subscribers()),
            'recent_sends': [],
            'failed_count': 0
        }
        
        # Recent sends
        if SEND_LOG_FILE.exists():
            with open(SEND_LOG_FILE, 'r') as f:
                log = json.load(f)
            status['recent_sends'] = log[-5:]
        
        # Failed count
        if FAILED_SENDS_FILE.exists():
            with open(FAILED_SENDS_FILE, 'r') as f:
                failures = json.load(f)
            status['failed_count'] = len(failures)
        
        return status


def main():
    parser = argparse.ArgumentParser(description='Email sender via Mailgun')
    
    # Send options
    parser.add_argument('--send', type=str, metavar='HTML_FILE',
                       help='Send newsletter from HTML file')
    parser.add_argument('--text', type=str, metavar='TEXT_FILE',
                       help='Plain text version (auto-generated if not provided)')
    parser.add_argument('--subject', type=str, default='Daily Stock Picks',
                       help='Email subject')
    parser.add_argument('--to', type=str, nargs='+',
                       help='Send to specific email(s) instead of subscribers')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview without sending')
    
    # Subscriber management
    parser.add_argument('--subscribers', type=str, nargs='+',
                       metavar=('ACTION', 'ARGS'),
                       help='Manage subscribers: list, add EMAIL [NAME], remove EMAIL, import FILE')
    
    # Archive
    parser.add_argument('--archive', type=str, nargs='+',
                       metavar=('ACTION', 'DATE'),
                       help='Archive operations: list, view DATE')
    
    # Status
    parser.add_argument('--status', action='store_true',
                       help='Show sending status')
    
    # Retry
    parser.add_argument('--retry', action='store_true',
                       help='Retry failed sends')
    
    args = parser.parse_args()
    
    sender = EmailSender()
    
    # Handle commands
    if args.send:
        # Read HTML
        with open(args.send, 'r') as f:
            html = f.read()
        
        # Read or generate text
        if args.text:
            with open(args.text, 'r') as f:
                text = f.read()
        else:
            # Simple HTML to text conversion
            import re
            text = re.sub(r'<[^>]+>', '', html)
            text = re.sub(r'\s+', ' ', text).strip()
        
        result = sender.send_newsletter(
            html=html,
            text=text,
            subject=args.subject,
            recipients=args.to,
            dry_run=args.dry_run
        )
        
        sys.exit(0 if result.failed_count == 0 else 1)
    
    elif args.subscribers:
        action = args.subscribers[0]
        
        if action == 'list':
            subs = sender.subscribers.get_all_subscribers()
            print(f"\n📋 Subscribers ({len(subs)} total):")
            print("-" * 50)
            for sub in subs:
                status = "✅" if sub.active else "❌"
                print(f"   {status} {sub.email} ({sub.name or 'No name'})")
        
        elif action == 'add' and len(args.subscribers) >= 2:
            email = args.subscribers[1]
            name = args.subscribers[2] if len(args.subscribers) > 2 else ""
            if sender.subscribers.add_subscriber(email, name):
                print(f"✅ Added: {email}")
            else:
                print(f"⚠️ Already exists: {email}")
        
        elif action == 'remove' and len(args.subscribers) >= 2:
            email = args.subscribers[1]
            if sender.subscribers.remove_subscriber(email):
                print(f"✅ Removed: {email}")
            else:
                print(f"⚠️ Not found: {email}")
        
        elif action == 'import' and len(args.subscribers) >= 2:
            import_file = Path(args.subscribers[1])
            count = sender.subscribers.import_from_csv(import_file)
            print(f"✅ Imported {count} subscribers")
        
        else:
            print("Usage: --subscribers list|add EMAIL [NAME]|remove EMAIL|import FILE")
    
    elif args.archive:
        action = args.archive[0]
        
        if action == 'list':
            archives = sender.archive.list_archives()
            print(f"\n📁 Newsletter Archive ({len(archives)} newsletters):")
            print("-" * 60)
            for arch in archives:
                print(f"   {arch['date']}: {arch.get('subject', 'No subject')} "
                      f"({arch.get('sent_count', 0)} sent)")
        
        elif action == 'view' and len(args.archive) >= 2:
            date = args.archive[1]
            archive = sender.archive.get_archive(date)
            if archive:
                print(f"\n📧 Newsletter: {date}")
                print("-" * 50)
                meta = archive.get('metadata', {})
                print(f"Subject: {meta.get('subject', 'N/A')}")
                print(f"Sent: {meta.get('sent_count', 0)}")
                print(f"Failed: {meta.get('failed_count', 0)}")
                print(f"\n--- Preview ---\n")
                print(archive.get('text', 'No text version')[:500])
            else:
                print(f"❌ Archive not found: {date}")
        
        else:
            print("Usage: --archive list|view DATE")
    
    elif args.status:
        status = sender.get_status()
        print(f"\n📊 Email Sender Status")
        print("=" * 50)
        print(f"Active Subscribers: {status['subscribers']}")
        print(f"Total Subscribers: {status['total_subscribers']}")
        print(f"Failed Sends (pending): {status['failed_count']}")
        
        if status['recent_sends']:
            print(f"\nRecent Sends:")
            for send in status['recent_sends'][-3:]:
                print(f"   {send['timestamp']}: {send['sent_count']} sent, {send['failed_count']} failed")
    
    elif args.retry:
        if not FAILED_SENDS_FILE.exists():
            print("No failed sends to retry")
            sys.exit(0)
        
        # TODO: Implement retry of logged failures
        print("⚠️ Retry functionality coming soon")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()



