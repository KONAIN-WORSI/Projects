#!/usr/bin/env python3
"""
Example: Using Intelligent Email Composer Programmatically
Shows how to integrate the enhanced email composer into your own Python scripts
"""

from intelligent_email_composer import (
    IntelligentEmailComposer,
    EmailContext,
    ConsoleEmailSender,
    FileEmailSender,
    GmailSender,
    EmailCampaignManager
)


def example_1_single_email():
    """Example 1: Send a single email to one person"""
    print("=" * 60)
    print("EXAMPLE 1: Send Single Email")
    print("=" * 60)
    
    # Initialize composer
    composer = IntelligentEmailComposer(sender_name="Your Name")
    
    # Create email context
    context = EmailContext(
        recipient_name="Alice Johnson",
        recipient_email="alice@company.com",
        relationship="colleague",
        topic="Feature Proposal",
        urgency="normal",
        key_points=["New feature idea", "Performance benefits", "Timeline"]
    )
    
    # Compose email
    email = composer.compose(context)
    
    # Display email
    print(f"To: {context.recipient_email}")
    print(f"Subject: {email.subject}\n")
    print(email.full_text())
    print()


def example_2_batch_to_console():
    """Example 2: Send batch emails to console (testing)"""
    print("=" * 60)
    print("EXAMPLE 2: Batch Emails to Console")
    print("=" * 60)
    
    composer = IntelligentEmailComposer(sender_name="Test Bot")
    sender = ConsoleEmailSender(verbose=False)  # Set to False to be quieter
    manager = EmailCampaignManager(composer, sender)
    
    # Create multiple contexts
    contexts = [
        EmailContext(
            recipient_name="Bob Wilson",
            recipient_email="bob@company.com",
            relationship="boss",
            topic="Q3 Results",
            urgency="high",
            key_points=["Results", "Metrics", "Next quarter plan"]
        ),
        EmailContext(
            recipient_name="Carol Davis",
            recipient_email="carol@company.com",
            relationship="colleague",
            topic="Code Review",
            urgency="normal",
            key_points=["PR #456", "Ready for feedback"]
        ),
    ]
    
    # Send batch
    report = manager.send_batch(contexts, delay_seconds=0)
    
    print(f"\nReport: {report['sent']} sent, {report['failed']} failed\n")


def example_3_batch_to_files():
    """Example 3: Save batch emails to files"""
    print("=" * 60)
    print("EXAMPLE 3: Batch Emails to Files")
    print("=" * 60)
    
    composer = IntelligentEmailComposer(sender_name="Email System")
    sender = FileEmailSender(output_dir="my_emails")  # Custom directory
    manager = EmailCampaignManager(composer, sender)
    
    contexts = [
        EmailContext(
            recipient_name="David Smith",
            recipient_email="david@company.com",
            relationship="client",
            topic="Project Update",
            urgency="normal",
            key_points=["Progress", "Deliverables", "Timeline"]
        ),
        EmailContext(
            recipient_name="Emma Brown",
            recipient_email="emma@company.com",
            relationship="vendor",
            topic="Quote Request",
            urgency="high",
            key_points=["Specifications", "Deadline: Friday", "Budget info"]
        ),
    ]
    
    report = manager.send_batch(contexts)
    print(f"\nEmails saved! Check 'my_emails' directory")
    print(f"Report: {report['sent']} sent, {report['failed']} failed\n")


def example_4_learning_system():
    """Example 4: Use the learning system"""
    print("=" * 60)
    print("EXAMPLE 4: Learning System")
    print("=" * 60)
    
    composer = IntelligentEmailComposer(
        sender_name="Smart Bot",
        memory_path="company_email_memory.json"
    )
    
    # Create context
    context = EmailContext(
        recipient_name="Frank Johnson",
        recipient_email="frank@company.com",
        relationship="colleague",
        topic="Meeting Scheduling",
        urgency="normal"
    )
    
    # Generate email
    email = composer.compose(context)
    print(f"First email:\n{email}\n")
    
    # Learn from this email
    composer.learn(context, email)
    print("✓ Learned from this email")
    
    # Get analytics
    analytics = composer.get_analytics()
    print(f"\nAnalytics:")
    print(f"  - Learned relationships: {analytics['learned_relationships']}")
    print(f"  - Average email length: {analytics['avg_email_length']} words")
    print(f"  - Total emails learned: {analytics['total_emails_learned']}\n")


def example_5_custom_sender():
    """Example 5: Create custom email sender"""
    print("=" * 60)
    print("EXAMPLE 5: Custom Email Sender")
    print("=" * 60)
    
    from intelligent_email_composer import EmailSender
    
    class SlackNotificationSender(EmailSender):
        """Custom sender that sends to Slack instead of email"""
        
        def send(self, recipient_email: str, subject: str, body: str, 
                greeting: str, closing: str) -> bool:
            # This is just a demo - in reality you'd call Slack API
            print(f"[SLACK] Would send to #{recipient_email}")
            print(f"[SLACK] Message: {greeting}... {body[:50]}...")
            return True
    
    composer = IntelligentEmailComposer("Slack Bot")
    sender = SlackNotificationSender()
    manager = EmailCampaignManager(composer, sender)
    
    context = EmailContext(
        recipient_name="Team",
        recipient_email="team-updates",
        relationship="colleague",
        topic="Daily Standup",
        urgency="normal"
    )
    
    manager.send_email(context)
    print()


def example_6_load_from_csv():
    """Example 6: Load recipients from CSV file"""
    print("=" * 60)
    print("EXAMPLE 6: Load from CSV File")
    print("=" * 60)
    
    composer = IntelligentEmailComposer(sender_name="CSV Mailer")
    sender = ConsoleEmailSender(verbose=False)
    manager = EmailCampaignManager(composer, sender)
    
    # Assuming you have a recipients.csv file
    # Format: name,email,relationship,topic,urgency,key_points
    
    # For demo, let's create one
    import csv
    csv_content = [
        ["name", "email", "relationship", "topic", "urgency", "key_points"],
        ["Grace Lee", "grace@company.com", "colleague", "Feedback", "normal", 
         "Code review|Performance|Architecture"],
        ["Henry Zhang", "henry@company.com", "boss", "Monthly Review", "high", 
         "Accomplishments|Challenges|Goals"],
    ]
    
    with open("demo_recipients.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_content)
    
    # Load and send
    contexts = manager.load_test_recipients("demo_recipients.csv")
    if contexts:
        report = manager.send_batch(contexts)
        print(f"\nLoaded {len(contexts)} recipients")
        print(f"Sent: {report['sent']}, Failed: {report['failed']}\n")


def example_7_advanced_context():
    """Example 7: Use advanced context features"""
    print("=" * 60)
    print("EXAMPLE 7: Advanced Context Features")
    print("=" * 60)
    
    composer = IntelligentEmailComposer(sender_name="Advanced System")
    
    context = EmailContext(
        recipient_name="Iris Martinez",
        recipient_email="iris@company.com",
        relationship="client",
        topic="Contract Negotiation",
        urgency="urgent",  # Note: urgent urgency level
        tone="formal",      # Explicit formal tone
        key_points=[
            "Terms and conditions update",
            "Required by April 5th",
            "Legal review pending"
        ],
        previous_threads=[
            "Initial proposal sent March 15",
            "Feedback received March 28"
        ]
    )
    
    email = composer.compose(context)
    
    print(f"To: {context.recipient_email}")
    print(f"Subject: {email.subject}")
    print(f"Tone: {context.tone}")
    print(f"Urgency: {context.urgency}")
    print(f"Confidence: {email.tone_score:.0%}\n")
    print(email.full_text())
    print()


def example_8_full_workflow():
    """Example 8: Complete workflow - preview, then save"""
    print("=" * 60)
    print("EXAMPLE 8: Full Workflow - Preview → Save")
    print("=" * 60)
    
    composer = IntelligentEmailComposer(sender_name="Workflow Manager")
    
    # Step 1: Preview with console
    print("\n[STEP 1] Preview emails to console...")
    sender_console = ConsoleEmailSender(verbose=False)
    manager_console = EmailCampaignManager(composer, sender_console)
    
    contexts = [
        EmailContext(
            recipient_name="Jack Ryan",
            recipient_email="jack@company.com",
            relationship="colleague",
            topic="Project Kickoff",
            urgency="high",
            key_points=["Team assembly", "Resource allocation", "Timeline"]
        ),
    ]
    
    report = manager_console.send_batch(contexts)
    print(f"Preview complete: {report['sent']} emails\n")
    
    # Step 2: Save to files
    print("[STEP 2] Saving emails to files for final review...")
    sender_file = FileEmailSender(output_dir="final_emails")
    manager_file = EmailCampaignManager(composer, sender_file)
    
    report = manager_file.send_batch(contexts)
    print(f"Saved: {report['sent']} emails to 'final_emails' directory\n")
    
    # Step 3: In production, you would send with GmailSender
    print("[STEP 3] Ready to send real emails with GmailSender")
    print("  → Requires: Gmail app password\n")


# Run all examples
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("INTELLIGENT EMAIL COMPOSER - USAGE EXAMPLES")
    print("=" * 60 + "\n")
    
    try:
        example_1_single_email()
        input("Press Enter to continue...\n")
        
        example_2_batch_to_console()
        input("Press Enter to continue...\n")
        
        example_3_batch_to_files()
        input("Press Enter to continue...\n")
        
        example_4_learning_system()
        input("Press Enter to continue...\n")
        
        example_5_custom_sender()
        input("Press Enter to continue...\n")
        
        example_6_load_from_csv()
        input("Press Enter to continue...\n")
        
        example_7_advanced_context()
        input("Press Enter to continue...\n")
        
        example_8_full_workflow()
        
        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
