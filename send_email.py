#!/usr/bin/env python3
"""
Send actual email to Saba Khan for testing
"""

from intelligent_email_composer import (
    IntelligentEmailComposer,
    EmailContext,
    GmailSender
)

# ============ CONFIGURE THESE ============

# Your Gmail account details
GMAIL_EMAIL = "konainworsi@gmail.com"  # CHANGE: Your Gmail address
GMAIL_PASSWORD = "uvyvifnhznahrvlo"  # CHANGE: Your 16-char app password
                                       # Get from: https://myaccount.google.com/apppasswords

# Recipient details
RECIPIENT_NAME = "Saba Khan"
RECIPIENT_EMAIL = "sabakhatun906@gmail.com"
RELATIONSHIP = "sister"  # colleague, boss, client, friend, sister, etc.
TOPIC = "Test Email - Project Update"
URGENCY = "normal"  # low, normal, high, urgent
KEY_POINTS = [
    "Testing automated email system",
    "Making sure everything works",
    "Will send more detailed email soon"
]

# Your name (sender)
SENDER_NAME = "Test Automation"

# ========================================

def main():
    print("=" * 60)
    print("SENDING EMAIL TO SABA KHAN")
    print("=" * 60)
    
    # Initialize composer
    composer = IntelligentEmailComposer(sender_name=SENDER_NAME)
    
    # Create email context
    context = EmailContext(
        recipient_name=RECIPIENT_NAME,
        recipient_email=RECIPIENT_EMAIL,
        relationship=RELATIONSHIP,
        topic=TOPIC,
        urgency=URGENCY,
        key_points=KEY_POINTS
    )
    
    # Generate email
    print(f"\n[1] Generating email...")
    email = composer.compose(context)
    
    # Show what will be sent
    print(f"\n[2] Email preview:")
    print(f"\nTo: {RECIPIENT_EMAIL}")
    print(f"Subject: {email.subject}")
    print(f"\n{'-'*60}")
    print(email.full_text())
    print(f"{'-'*60}\n")
    
    # Ask for confirmation
    confirm = input("Send this email? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("\n[CANCELLED] Email not sent.")
        return
    
    # Send email
    print(f"\n[3] Connecting to Gmail...")
    sender = GmailSender(GMAIL_EMAIL, GMAIL_PASSWORD)
    
    print(f"[4] Sending email...")
    success = sender.send(
        recipient_email=RECIPIENT_EMAIL,
        subject=email.subject,
        body=email.body,
        greeting=email.greeting,
        closing=email.closing
    )
    
    # Show result
    print(f"\n{'='*60}")
    if success:
        print(f"✅ SUCCESS! Email sent to {RECIPIENT_EMAIL}")
        print(f"[INFO] Saba Khan should receive it shortly")
    else:
        print(f"❌ FAILED! Could not send email")
        print(f"[HINT] Check your Gmail credentials")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"\nTroubleshooting:")
        print(f"  1. Did you enable 2-Step Verification? (https://myaccount.google.com/security)")
        print(f"  2. Did you generate an App Password? (https://myaccount.google.com/apppasswords)")
        print(f"  3. Is the 16-character password correct?")
        print(f"  4. Check GMAIL_EMAIL and GMAIL_PASSWORD in this script")
