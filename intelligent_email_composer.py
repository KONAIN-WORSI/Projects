"""
Intelligent Email Automation System
====================================
An AI-powered email composer that understands context, learns from patterns,
and generates personalized emails with minimal input.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import argparse
import csv
from abc import ABC, abstractmethod


@dataclass
class EmailContext:
    """Represents the context for email generation."""
    recipient_name: str
    recipient_email: str
    relationship: str  # colleague, client, friend, boss, etc.
    topic: str
    urgency: str = "normal"  # low, normal, high, urgent
    tone: str = "professional"  # casual, professional, formal, friendly
    previous_threads: List[str] = field(default_factory=list)
    key_points: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "recipient_name": self.recipient_name,
            "recipient_email": self.recipient_email,
            "relationship": self.relationship,
            "topic": self.topic,
            "urgency": self.urgency,
            "tone": self.tone,
            "previous_threads": self.previous_threads,
            "key_points": self.key_points
        }


@dataclass
class GeneratedEmail:
    """Represents a generated email with metadata."""
    subject: str
    body: str
    greeting: str
    closing: str
    tone_score: float  # 0-1, confidence in tone match
    context_used: Dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def full_text(self) -> str:
        return f"{self.greeting}\n\n{self.body}\n\n{self.closing}"
    
    def __str__(self) -> str:
        return f"Subject: {self.subject}\n\n{self.full_text()}"


class ToneAnalyzer:
    """Analyzes and adapts email tone based on context."""
    
    TONE_PATTERNS = {
        "casual": {
            "greetings": ["Hey {name}!", "Hi {name},", "Hey there,"],
            "closings": ["Cheers,", "Talk soon!", "Best,"],
            "patterns": ["contractions", "emoji_optional", "short_sentences"]
        },
        "professional": {
            "greetings": ["Hi {name},", "Hello {name},", "Dear {name},"],
            "closings": ["Best regards,", "Best,", "Thanks,"],
            "patterns": ["clear_structure", "polite_direct"]
        },
        "formal": {
            "greetings": ["Dear {name},", "To {name},", "Dear Mr./Ms. {last_name},"],
            "closings": ["Sincerely,", "Respectfully,", "Yours truly,"],
            "patterns": ["no_contractions", "full_sentences", "honorifics"]
        },
        "friendly": {
            "greetings": ["Hi {name}!", "Hey {name},", "Hello {name},"],
            "closings": ["Take care!", "Looking forward to hearing from you!", "Best wishes,"],
            "patterns": ["warm_phrases", "personal_touch", "conversational"]
        }
    }
    
    def __init__(self):
        self.relationship_tone_map = {
            "boss": ["formal", "professional"],
            "client": ["professional", "formal"],
            "colleague": ["professional", "friendly"],
            "friend": ["casual", "friendly"],
            "vendor": ["professional"],
            "recruiter": ["professional", "formal"],
            "mentor": ["professional", "friendly"]
        }
    
    def suggest_tone(self, relationship: str, urgency: str, user_preference: str = None) -> str:
        """Suggests appropriate tone based on relationship and urgency."""
        if user_preference and user_preference in self.TONE_PATTERNS:
            return user_preference
        
        possible_tones = self.relationship_tone_map.get(relationship, ["professional"])
        
        # Urgency adjustments
        if urgency == "urgent":
            return "professional"  # Urgent emails should be clear and professional
        elif urgency == "casual_meeting":
            return "friendly" if "friendly" in possible_tones else possible_tones[0]
        
        return possible_tones[0]
    
    def get_greeting(self, tone: str, name: str) -> str:
        """Generate appropriate greeting."""
        templates = self.TONE_PATTERNS[tone]["greetings"]
        template = random.choice(templates)
        
        # Extract last name if formal and possible
        if tone == "formal" and " " in name:
            last_name = name.split()[-1]
            return template.format(name=name, last_name=last_name)
        
        # For casual, use first name only
        first_name = name.split()[0] if " " in name else name
        return template.format(name=first_name, first_name=first_name)
    
    def get_closing(self, tone: str) -> str:
        """Generate appropriate closing."""
        return random.choice(self.TONE_PATTERNS[tone]["closings"])


class ContextLearner:
    """Learns from past email patterns to improve future compositions."""
    
    def __init__(self, memory_path: str = "email_memory.json"):
        self.memory_path = Path(memory_path)
        self.patterns = self._load_memory()
    
    def _load_memory(self) -> Dict:
        """Load learned patterns from disk."""
        if self.memory_path.exists():
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "relationship_templates": {},
            "topic_phrases": {},
            "subject_patterns": {},
            "word_frequencies": {},
            "avg_email_length": 150
        }
    
    def save_memory(self):
        """Persist learned patterns."""
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, indent=2)
    
    def learn_from_sent_email(self, context: EmailContext, email: GeneratedEmail):
        """Extract patterns from a sent email."""
        rel = context.relationship
        topic = context.topic
        
        # Track relationship templates
        if rel not in self.patterns["relationship_templates"]:
            self.patterns["relationship_templates"][rel] = []
        self.patterns["relationship_templates"][rel].append({
            "greeting": email.greeting,
            "closing": email.closing,
            "tone": context.tone
        })
        
        # Track topic keywords
        if topic not in self.patterns["topic_phrases"]:
            self.patterns["topic_phrases"][topic] = []
        
        # Extract key phrases from subject and body
        words = re.findall(r'\b\w+\b', email.subject.lower() + " " + email.body.lower())
        important_words = [w for w in words if len(w) > 4]
        self.patterns["topic_phrases"][topic].extend(important_words[:10])
        
        # Update average length
        word_count = len(email.body.split())
        avg = self.patterns["avg_email_length"]
        self.patterns["avg_email_length"] = (avg * 0.9) + (word_count * 0.1)
        
        self.save_memory()
    
    def get_suggested_phrases(self, topic: str, limit: int = 3) -> List[str]:
        """Get commonly used phrases for a topic."""
        phrases = self.patterns["topic_phrases"].get(topic, [])
        if phrases:
            from collections import Counter
            most_common = Counter(phrases).most_common(limit)
            return [phrase for phrase, _ in most_common]
        return []
    
    def get_preferred_style(self, relationship: str) -> Dict:
        """Get learned preferences for a relationship type."""
        templates = self.patterns["relationship_templates"].get(relationship, [])
        if not templates:
            return {}
        
        # Find most common tone
        tones = [t["tone"] for t in templates]
        from collections import Counter
        preferred_tone = Counter(tones).most_common(1)[0][0] if tones else "professional"
        
        return {
            "tone": preferred_tone,
            "sample_count": len(templates)
        }


class ContentGenerator:
    """Generates email content based on understanding of context."""
    
    # Topic-specific templates with intelligent slots
    TEMPLATES = {
        "meeting": {
            "subject": ["Meeting: {topic} - {date}", "Let's meet about {topic}", "Meeting Request: {topic}"],
            "openers": [
                "I'd like to schedule a meeting to discuss {topic}.",
                "Are you available for a quick meeting about {topic}?",
                "I think it would be valuable to sync up on {topic}."
            ],
            "bodies": [
                "I'm thinking {timeframe} would work. Would {suggested_time} work for you?",
                "Please let me know your availability {timeframe}.",
                "I'd estimate we'll need about {duration}."
            ],
            "closers": [
                "Looking forward to our discussion.",
                "Let me know what works best for your schedule."
            ]
        },
        "follow_up": {
            "subject": ["Following up: {topic}", "Quick follow-up on {topic}", "Re: {topic}"],
            "openers": [
                "I wanted to follow up on {topic}.",
                "Just checking in regarding {topic}.",
                "Following up on our previous discussion about {topic}."
            ],
            "bodies": [
                "Have you had a chance to review {item}?",
                "I wanted to see if there are any updates on {item}.",
                "Please let me know if you need any additional information."
            ],
            "closers": [
                "Thanks for your time on this.",
                "Let me know if you have any questions."
            ]
        },
        "request": {
            "subject": ["Request: {topic}", "Could you help with {topic}?", "Quick request - {topic}"],
            "openers": [
                "I'm reaching out regarding {topic}.",
                "I was hoping you could assist with {topic}.",
                "I have a quick request related to {topic}."
            ],
            "bodies": [
                "Specifically, I need {details}.",
                "Would you be able to help with {details}?",
                "If possible, I'd appreciate {deadline_text}."
            ],
            "closers": [
                "Thanks in advance for your help.",
                "I appreciate your assistance with this."
            ]
        },
        "introduction": {
            "subject": ["Introduction: {topic}", "Introducing myself - {topic}", "Nice to meet you"],
            "openers": [
                "I hope this email finds you well.",
                "My name is {sender_name}, and I wanted to introduce myself.",
                "I'm reaching out because {reason}."
            ],
            "bodies": [
                "I'd love to learn more about {topic}.",
                "I think there might be some synergy between {topic}.",
                "Would you be open to a brief conversation about {common_interest}?"
            ],
            "closers": [
                "Looking forward to connecting.",
                "Hope to hear from you soon."
            ]
        },
        "generic": {
            "subject": ["Regarding {topic}", "Quick note about {topic}", "Update on {topic}"],
            "openers": [
                "I wanted to reach out about {topic}.",
                "Quick update on {topic}.",
                "Just wanted to share some thoughts on {topic}."
            ],
            "bodies": [
                "{key_points}",
                "Here are the details: {key_points}",
                "Let me know your thoughts on {key_points}."
            ],
            "closers": [
                "Let me know if you have any questions.",
                "Happy to discuss further if needed."
            ]
        }
    }
    
    def __init__(self, learner: ContextLearner):
        self.learner = learner
    
    def detect_intent(self, topic: str, key_points: List[str]) -> str:
        """Detect the intent/type of email needed."""
        topic_lower = topic.lower()
        points_text = " ".join(key_points).lower()
        combined = topic_lower + " " + points_text
        
        if any(word in combined for word in ["meet", "schedule", "sync", "call", "zoom", "discuss"]):
            return "meeting"
        elif any(word in combined for word in ["follow up", "following up", "status", "update", "remind"]):
            return "follow_up"
        elif any(word in combined for word in ["request", "need", "help", "could you", "would you"]):
            return "request"
        elif any(word in combined for word in ["introduce", "introduction", "connect", "referred"]):
            return "introduction"
        else:
            return "generic"
    
    def generate_subject(self, intent: str, context: EmailContext) -> str:
        """Generate an appropriate subject line."""
        templates = self.TEMPLATES[intent]["subject"]
        template = random.choice(templates)
        
        # Smart substitutions
        date_str = datetime.now().strftime("%b %d")
        subject = template.format(
            topic=context.topic,
            date=date_str,
            recipient=context.recipient_name.split()[0]
        )
        
        # Learned phrase injection
        learned = self.learner.get_suggested_phrases(context.topic, 1)
        if learned and intent == "follow_up":
            subject = f"Follow-up: {context.topic}"
        
        return subject
    
    def generate_body(self, intent: str, context: EmailContext, sender_name: str) -> str:
        """Generate email body with contextual understanding."""
        templates = self.TEMPLATES[intent]
        
        # Build paragraphs
        paragraphs = []
        
        # Opening
        opener = random.choice(templates["openers"])
        opener = opener.format(topic=context.topic, sender_name=sender_name, reason=context.topic)
        paragraphs.append(opener)
        
        # Context-aware body generation
        body_template = random.choice(templates["bodies"])
        
        # Smart slot filling
        if intent == "meeting":
            body_filled = body_template.format(
                timeframe="sometime this week",
                suggested_time="Tuesday or Wednesday afternoon",
                duration="30-45 minutes"
            )
        elif intent == "follow_up":
            body_filled = body_template.format(item="the documents")
        elif intent == "request":
            deadline_text = "this by Friday" if context.urgency == "high" else "your help when convenient"
            body_filled = body_template.format(details="some assistance", deadline_text=deadline_text)
        else:
            key_points_text = "\n".join(f"- {point}" for point in context.key_points) if context.key_points else "this"
            body_filled = body_template.format(key_points=key_points_text)
        
        paragraphs.append(body_filled)
        
        # Add key points if available (for non-meeting types)
        if context.key_points and intent != "meeting":
            if not any(kp in body_filled for kp in context.key_points):
                points_text = "\n".join(f"- {point}" for point in context.key_points)
                paragraphs.append(f"Here are the key details:\n{points_text}")
        
        # Closing statement
        closing_statement = random.choice(templates["closers"])
        paragraphs.append(closing_statement)
        
        return "\n\n".join(paragraphs)
    
    def inject_urgency(self, body: str, urgency: str) -> str:
        """Adjust tone based on urgency."""
        if urgency == "urgent":
            return body + "\n\nThis is time-sensitive, so I'd appreciate a quick response."
        elif urgency == "high":
            return body.replace(".", " when you have a chance.", 1)
        return body


class IntelligentEmailComposer:
    """
    Main class that orchestrates intelligent email composition.
    Combines tone analysis, learning, and content generation.
    """
    
    def __init__(self, sender_name: str = "Your Name", memory_path: str = "email_memory.json"):
        self.sender_name = sender_name
        self.learner = ContextLearner(memory_path)
        self.tone_analyzer = ToneAnalyzer()
        self.content_generator = ContentGenerator(self.learner)
    
    def compose(self, context: EmailContext) -> GeneratedEmail:
        """
        Compose an intelligent email based on context.
        
        Args:
            context: EmailContext with recipient details, topic, etc.
        
        Returns:
            GeneratedEmail with complete email and metadata
        """
        # Auto-detect or suggest tone
        if not context.tone or context.tone == "auto":
            context.tone = self.tone_analyzer.suggest_tone(
                context.relationship, context.urgency
            )
        
        # Check for learned preferences
        learned_style = self.learner.get_preferred_style(context.relationship)
        if learned_style and learned_style.get("samples", 0) > 3:
            # Override with learned preference if we have enough samples
            context.tone = learned_style.get("tone", context.tone)
        
        # Detect intent
        intent = self.content_generator.detect_intent(context.topic, context.key_points)
        
        # Generate components
        subject = self.content_generator.generate_subject(intent, context)
        body = self.content_generator.generate_body(intent, context, self.sender_name)
        body = self.content_generator.inject_urgency(body, context.urgency)
        
        greeting = self.tone_analyzer.get_greeting(context.tone, context.recipient_name)
        closing = self.tone_analyzer.get_closing(context.tone)
        
        # Calculate confidence score
        tone_score = 0.85 if learned_style else 0.70
        
        email = GeneratedEmail(
            subject=subject,
            body=body,
            greeting=greeting,
            closing=closing,
            tone_score=tone_score,
            context_used=context.to_dict()
        )
        
        return email
    
    def learn(self, context: EmailContext, email: GeneratedEmail, feedback: str = None):
        """Learn from sent emails to improve future compositions."""
        self.learner.learn_from_sent_email(context, email)
        
        if feedback:
            # Could store feedback for reinforcement learning
            pass
    
    def quick_compose(self, 
                      to_name: str,
                      to_email: str,
                      topic: str,
                      relationship: str = "colleague",
                      key_points: List[str] = None) -> GeneratedEmail:
        """Quick compose with minimal parameters."""
        context = EmailContext(
            recipient_name=to_name,
            recipient_email=to_email,
            relationship=relationship,
            topic=topic,
            key_points=key_points or []
        )
        return self.compose(context)
    
    def get_analytics(self) -> Dict:
        """Get insights about learned patterns."""
        return {
            "learned_relationships": list(self.learner.patterns["relationship_templates"].keys()),
            "topic_coverage": list(self.learner.patterns["topic_phrases"].keys()),
            "avg_email_length": round(self.learner.patterns["avg_email_length"], 1),
            "total_emails_learned": sum(
                len(t) for t in self.learner.patterns["relationship_templates"].values()
            )
        }


class EmailSender(ABC):
    """Abstract base class for email sending strategies."""
    
    @abstractmethod
    def send(self, recipient_email: str, subject: str, body: str, greeting: str, closing: str) -> bool:
        """Send an email and return success status."""
        pass


class GmailSender(EmailSender):
    """Send emails via Gmail SMTP."""
    
    def __init__(self, sender_email: str, sender_password: str):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send(self, recipient_email: str, subject: str, body: str, greeting: str, closing: str) -> bool:
        """Send email via Gmail SMTP."""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            
            # Create full email text
            full_body = f"{greeting}\n\n{body}\n\n{closing}"
            
            # Create plain text version
            text_part = MIMEText(full_body, "plain")
            msg.attach(text_part)
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
            return False


class ConsoleEmailSender(EmailSender):
    """Mock sender that prints emails to console (for testing without actual sending)."""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
    
    def send(self, recipient_email: str, subject: str, body: str, greeting: str, closing: str) -> bool:
        """Print email to console instead of sending."""
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"TO: {recipient_email}")
            print(f"SUBJECT: {subject}")
            print(f"{'='*60}")
            print(f"{greeting}\n\n{body}\n\n{closing}")
            print(f"{'='*60}\n")
        return True


class FileEmailSender(EmailSender):
    """Save emails to files for review."""
    
    def __init__(self, output_dir: str = "sent_emails"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def send(self, recipient_email: str, subject: str, body: str, greeting: str, closing: str) -> bool:
        """Save email to file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{recipient_email.split('@')[0]}.txt"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"TO: {recipient_email}\n")
                f.write(f"SENT: {datetime.now().isoformat()}\n")
                f.write(f"SUBJECT: {subject}\n")
                f.write(f"{'-'*60}\n\n")
                f.write(f"{greeting}\n\n{body}\n\n{closing}\n")
            
            print(f"[OK] Email saved to {filepath}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save email: {e}")
            return False


class EmailCampaignManager:
    """Manage batch email sending campaigns for testing."""
    
    def __init__(self, composer: 'IntelligentEmailComposer', sender: EmailSender):
        self.composer = composer
        self.sender = sender
        self.sent_log = []
        self.failed_log = []
    
    def send_email(self, context: EmailContext) -> bool:
        """Send a single email."""
        email = self.composer.compose(context)
        success = self.sender.send(
            context.recipient_email,
            email.subject,
            email.body,
            email.greeting,
            email.closing
        )
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "recipient": context.recipient_email,
            "subject": email.subject,
            "relationship": context.relationship,
            "success": success
        }
        
        if success:
            self.sent_log.append(log_entry)
        else:
            self.failed_log.append(log_entry)
        
        return success
    
    def load_test_recipients(self, csv_file: str) -> List[EmailContext]:
        """Load test recipient list from CSV file.
        
        CSV format: name,email,relationship,topic,urgency,key_points (comma-separated)
        """
        contexts = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    key_points = []
                    if 'key_points' in row and row['key_points']:
                        key_points = [kp.strip() for kp in row['key_points'].split('|')]
                    
                    context = EmailContext(
                        recipient_name=row['name'],
                        recipient_email=row['email'],
                        relationship=row.get('relationship', 'colleague'),
                        topic=row['topic'],
                        urgency=row.get('urgency', 'normal'),
                        key_points=key_points
                    )
                    contexts.append(context)
            print(f"[OK] Loaded {len(contexts)} test recipients")
            return contexts
        except Exception as e:
            print(f"[ERROR] Failed to load CSV: {e}")
            return []
    
    def send_batch(self, contexts: List[EmailContext], delay_seconds: int = 0) -> Dict:
        """Send emails to multiple recipients."""
        import time
        
        print(f"\n[START] Sending {len(contexts)} test emails...")
        for i, context in enumerate(contexts, 1):
            print(f"\n[{i}/{len(contexts)}] Sending to {context.recipient_email}...")
            self.send_email(context)
            
            if delay_seconds > 0 and i < len(contexts):
                time.sleep(delay_seconds)
        
        return self.get_report()
    
    def get_report(self) -> Dict:
        """Get summary report of campaign."""
        total = len(self.sent_log) + len(self.failed_log)
        return {
            "total": total,
            "sent": len(self.sent_log),
            "failed": len(self.failed_log),
            "success_rate": f"{(len(self.sent_log) / total * 100):.1f}%" if total > 0 else "N/A",
            "sent_log": self.sent_log,
            "failed_log": self.failed_log
        }
    
    def save_report(self, output_file: str = "campaign_report.json"):
        """Save campaign report to file."""
        report = self.get_report()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"[OK] Report saved to {output_file}")


def demo():
    """Demonstrate the intelligent email composer."""
    
    print("=" * 60)
    print("INTELLIGENT EMAIL COMPOSER DEMO")
    print("=" * 60)
    
    # Initialize composer
    composer = IntelligentEmailComposer(
        sender_name="Alice Johnson",
        memory_path="demo_email_memory.json"
    )
    
    # Demo 1: Meeting request
    print("\n" + "-" * 60)
    print("SCENARIO 1: Meeting Request to Boss")
    print("-" * 60)
    
    context1 = EmailContext(
        recipient_name="Sarah Chen",
        recipient_email="sarah.chen@company.com",
        relationship="boss",
        topic="Q3 Project Review",
        urgency="normal",
        key_points=["Discuss progress", "Review budget", "Plan next quarter"]
    )
    
    email1 = composer.compose(context1)
    print(f"\n{email1}")
    print(f"\n[Tone Confidence: {email1.tone_score:.0%}]")
    
    # Demo 2: Follow-up to colleague (casual)
    print("\n" + "-" * 60)
    print("SCENARIO 2: Follow-up to Colleague")
    print("-" * 60)
    
    context2 = EmailContext(
        recipient_name="Mike Ross",
        recipient_email="mike.ross@company.com",
        relationship="colleague",
        topic="Design Document Feedback",
        urgency="high",
        key_points=["Need feedback by Friday", "Client presentation on Monday"]
    )
    
    email2 = composer.compose(context2)
    print(f"\n{email2}")
    
    # Demo 3: Client request (formal)
    print("\n" + "-" * 60)
    print("SCENARIO 3: Request to Client (Formal)")
    print("-" * 60)
    
    context3 = EmailContext(
        recipient_name="James Richardson",
        recipient_email="james@clientcorp.com",
        relationship="client",
        topic="Contract Amendment Request",
        urgency="normal",
        tone="formal"
    )
    
    email3 = composer.compose(context3)
    print(f"\n{email3}")
    
    # Demo 4: Quick compose
    print("\n" + "-" * 60)
    print("SCENARIO 4: Quick Compose (Friend)")
    print("-" * 60)
    
    email4 = composer.quick_compose(
        to_name="Emma Watson",
        to_email="emma@gmail.com",
        topic="Weekend Plans",
        relationship="friend"
    )
    print(f"\n{email4}")
    
    # Learn from sent emails
    print("\n" + "-" * 60)
    print("LEARNING FROM EMAILS")
    print("-" * 60)
    
    composer.learn(context1, email1)
    composer.learn(context2, email2)
    composer.learn(context3, email3)
    
    analytics = composer.get_analytics()
    print(f"\nLearned {analytics['total_emails_learned']} email patterns")
    print(f"Relationship types: {', '.join(analytics['learned_relationships'])}")
    print(f"Average preferred length: {analytics['avg_email_length']} words")
    
    # Demo 5: Same scenario with learning
    print("\n" + "-" * 60)
    print("SCENARIO 5: Same request to boss (with learning applied)")
    print("-" * 60)
    
    email5 = composer.compose(context1)
    print(f"\n{email5}")
    print(f"\n[Tone Confidence: {email5.tone_score:.0%} (improved with learning)]")
    
    # Cleanup
    if Path("demo_email_memory.json").exists():
        Path("demo_email_memory.json").unlink()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


def interactive_compose():
    """Interactive mode to compose custom emails."""
    composer = IntelligentEmailComposer(sender_name="Your Name")
    
    print("\n" + "=" * 50)
    print("   INTELLIGENT EMAIL COMPOSER - INTERACTIVE MODE")
    print("=" * 50 + "\n")
    
    name = input("Recipient name: ").strip()
    email = input("Recipient email: ").strip()
    
    print("\nRelationship types: boss, colleague, client, friend, vendor, recruiter, mentor")
    relationship = input("Relationship: ").strip() or "colleague"
    
    topic = input("Topic: ").strip()
    
    print("\nUrgency levels: low, normal, high, urgent")
    urgency = input("Urgency (default: normal): ").strip() or "normal"
    
    print("\nTone options: casual, professional, formal, friendly, auto")
    tone = input("Tone (default: auto): ").strip() or "auto"
    
    key_points = []
    print("\nEnter key points (empty line to finish):")
    while True:
        point = input("  - ").strip()
        if not point:
            break
        key_points.append(point)
    
    context = EmailContext(
        recipient_name=name,
        recipient_email=email,
        relationship=relationship,
        topic=topic,
        urgency=urgency,
        tone=tone,
        key_points=key_points
    )
    
    print("\n" + "=" * 50)
    print("GENERATING EMAIL...")
    print("=" * 50 + "\n")
    
    generated = composer.compose(context)
    
    print(f"To: {name} <{email}>")
    print(f"Subject: {generated.subject}\n")
    print(generated.full_text())
    print(f"\n{'-' * 50}")
    print(f"Tone confidence: {generated.tone_score:.0%}")
    
    save = input("\nSave this email pattern? (y/n): ").strip().lower()
    if save == 'y':
        composer.learn(context, generated)
        print("[OK] Learned from this email.")


def test_send_emails(mode: str = "console", sender_email: str = None, sender_password: str = None):
    """
    Test sending automated emails to multiple recipients.
    
    Args:
        mode: "console" (print to console), "file" (save to files), or "gmail" (send via Gmail)
        sender_email: Gmail account email (required for gmail mode)
        sender_password: Gmail app password (required for gmail mode)
    """
    composer = IntelligentEmailComposer(sender_name="Test Automation System")
    
    # Select sender based on mode
    if mode == "console":
        sender = ConsoleEmailSender(verbose=True)
    elif mode == "file":
        sender = FileEmailSender(output_dir="test_emails")
    elif mode == "gmail":
        if not sender_email or not sender_password:
            print("[ERROR] Gmail mode requires sender_email and sender_password")
            return
        sender = GmailSender(sender_email, sender_password)
    else:
        print("[ERROR] Unknown mode. Use 'console', 'file', or 'gmail'")
        return
    
    manager = EmailCampaignManager(composer, sender)
    
    # Create test recipients (customize as needed)
    test_contexts = [
        EmailContext(
            recipient_name="John Smith",
            recipient_email="john.test@example.com",
            relationship="colleague",
            topic="Test Email - Feature Review",
            urgency="normal",
            key_points=["Feature implementation", "Performance metrics", "Timeline"]
        ),
        EmailContext(
            recipient_name="Sarah Johnson",
            recipient_email="sarah.test@example.com",
            relationship="boss",
            topic="Test Email - Project Status",
            urgency="high",
            key_points=["Current progress", "Blockers", "Next steps"]
        ),
        EmailContext(
            recipient_name="Mike Davis",
            recipient_email="mike.test@example.com",
            relationship="client",
            topic="Test Email - Proposal",
            urgency="normal",
            key_points=["Solution overview", "Pricing", "Implementation timeline"]
        ),
    ]
    
    # Send batch emails
    report = manager.send_batch(test_contexts, delay_seconds=1)
    
    # Print report
    print("\n" + "=" * 60)
    print("CAMPAIGN REPORT")
    print("=" * 60)
    print(f"Total emails: {report['total']}")
    print(f"Successfully sent: {report['sent']}")
    print(f"Failed: {report['failed']}")
    print(f"Success rate: {report['success_rate']}")
    
    # Save report
    manager.save_report("test_email_report.json")


def create_test_recipient_csv(filename: str = "test_recipients.csv"):
    """Create a sample CSV file for batch email testing."""
    test_data = [
        {
            "name": "Alice Cooper",
            "email": "alice@example.com",
            "relationship": "colleague",
            "topic": "Test: Code Review",
            "urgency": "normal",
            "key_points": "Please review PR #123|Feedback needed by Friday|Thanks in advance"
        },
        {
            "name": "Bob Wilson",
            "email": "bob@example.com",
            "relationship": "boss",
            "topic": "Test: Weekly Standup",
            "urgency": "normal",
            "key_points": "Can we sync this week|Discuss Q3 objectives|Team updates"
        },
        {
            "name": "Carol White",
            "email": "carol@example.com",
            "relationship": "client",
            "topic": "Test: Project Proposal",
            "urgency": "high",
            "key_points": "Ready to discuss proposal|Need your feedback|Next steps"
        },
    ]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["name", "email", "relationship", "topic", "urgency", "key_points"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_data)
        print(f"[OK] Test recipients CSV created: {filename}")
        return filename
    except Exception as e:
        print(f"[ERROR] Failed to create CSV: {e}")
        return None


if __name__ == "__main__":
    import sys
    
    parser = argparse.ArgumentParser(description="Intelligent Email Composer with Testing Support")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--test", action="store_true", help="Run test email campaign")
    parser.add_argument("--test-mode", choices=["console", "file", "gmail"], default="console",
                       help="Test email mode (console, file, gmail)")
    parser.add_argument("--create-csv", action="store_true", help="Create sample recipients CSV")
    parser.add_argument("--from-csv", type=str, help="Send emails from CSV file")
    parser.add_argument("--gmail-email", type=str, help="Gmail account email (for gmail mode)")
    parser.add_argument("--gmail-password", type=str, help="Gmail app password (for gmail mode)")
    
    args = parser.parse_args()
    
    if args.create_csv:
        create_test_recipient_csv()
    elif args.from_csv:
        print(f"[INFO] Loading recipients from {args.from_csv}...")
        composer = IntelligentEmailComposer(sender_name="Email Automation")
        sender = ConsoleEmailSender() if args.test_mode == "console" else FileEmailSender()
        manager = EmailCampaignManager(composer, sender)
        contexts = manager.load_test_recipients(args.from_csv)
        if contexts:
            report = manager.send_batch(contexts)
            print(f"\n[REPORT] Sent: {report['sent']}, Failed: {report['failed']}")
    elif args.test:
        test_send_emails(mode=args.test_mode, sender_email=args.gmail_email, sender_password=args.gmail_password)
    elif args.interactive:
        interactive_compose()
    else:
        demo()
        print("\n" + "=" * 60)
        print("ADDITIONAL FEATURES")
        print("=" * 60)
        print("Test email sending:")
        print("  python intelligent_email_composer.py --test [--test-mode console|file|gmail]")
        print("\nCreate sample recipients CSV:")
        print("  python intelligent_email_composer.py --create-csv")
        print("\nSend emails from CSV file:")
        print("  python intelligent_email_composer.py --from-csv test_recipients.csv")
        print("\nInteractive mode:")
        print("  python intelligent_email_composer.py --interactive")
