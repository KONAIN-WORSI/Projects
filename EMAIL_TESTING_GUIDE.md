# Intelligent Email Composer - Testing & Automation Guide

This guide explains how to use the enhanced `intelligent_email_composer.py` file to send automated test emails.

## Features Added

### 1. **Email Sending Capabilities**
- **ConsoleEmailSender**: Print emails to console (mock testing)
- **FileEmailSender**: Save emails to files for review
- **GmailSender**: Send real emails via Gmail SMTP

### 2. **Campaign Management**
- Batch send emails to multiple recipients
- Load recipients from CSV files
- Campaign reporting and logging

### 3. **Command-Line Interface**
Easy testing with command-line arguments

---

## Quick Start

### 1. **Test with Console Output** (Recommended for First Test)
```bash
python intelligent_email_composer.py --test --test-mode console
```
This will generate and display 3 test emails in the console without actually sending them.

### 2. **Save Emails to Files**
```bash
python intelligent_email_composer.py --test --test-mode file
```
Emails will be saved to the `test_emails/` directory.

### 3. **Create Sample Recipients CSV**
```bash
python intelligent_email_composer.py --create-csv
```
This creates `test_recipients.csv` with sample recipient data.

### 4. **Send Emails from CSV File**
```bash
python intelligent_email_composer.py --from-csv test_recipients.csv --test-mode console
```

---

## Advanced Usage

### Send Real Emails via Gmail

1. **Enable Gmail App Password**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification
   - Generate an "App Password" for Gmail

2. **Send test emails:**
```bash
python intelligent_email_composer.py --test --test-mode gmail --gmail-email your@gmail.com --gmail-password your-app-password
```

### Create Custom Recipients CSV

Create a `recipients.csv` file with this format:

```csv
name,email,relationship,topic,urgency,key_points
John Smith,john@company.com,colleague,Test: Code Review,normal,Review PR #123|Feedback needed|Thanks
Sarah CEO,sarah@company.com,boss,Test: Status Update,high,Progress update|Timeline|Blockers
Client Name,client@company.com,client,Test: Proposal,normal,Solution overview|Pricing|Timeline
```

Then run:
```bash
python intelligent_email_composer.py --from-csv recipients.csv
```

---

## CSV File Format

| Field | Required | Options | Example |
|-------|----------|---------|---------|
| name | Yes | Any text | John Smith |
| email | Yes | Valid email | john@example.com |
| relationship | No | colleague, boss, client, friend, vendor, recruiter, mentor | colleague |
| topic | Yes | Any text | Test: Feature Review |
| urgency | No | low, normal, high, urgent | normal |
| key_points | No | Items separated by \| | Item1\|Item2\|Item3 |

---

## Email Sender Classes

### ConsoleEmailSender
```python
sender = ConsoleEmailSender(verbose=True)
# Prints emails to console
```

### FileEmailSender
```python
sender = FileEmailSender(output_dir="sent_emails")
# Saves emails to files in the specified directory
```

### GmailSender
```python
sender = GmailSender("your@gmail.com", "app_password")
# Sends real emails via Gmail SMTP
```

---

## Python API Usage

Use these classes directly in your Python code:

```python
from intelligent_email_composer import (
    IntelligentEmailComposer,
    EmailContext,
    ConsoleEmailSender,
    EmailCampaignManager
)

# Initialize
composer = IntelligentEmailComposer(sender_name="Your Name")
sender = ConsoleEmailSender()
manager = EmailCampaignManager(composer, sender)

# Create test contexts
context = EmailContext(
    recipient_name="John Doe",
    recipient_email="john@example.com",
    relationship="colleague",
    topic="Test Email",
    urgency="normal",
    key_points=["Point 1", "Point 2"]
)

# Send email
manager.send_email(context)

# Get report
report = manager.get_report()
print(f"Sent: {report['sent']}, Failed: {report['failed']}")
```

---

## Campaign Workflow

```
1. Create recipients CSV file
     ↓
2. Run with --from-csv and --test-mode console (preview emails)
     ↓
3. Review generated emails
     ↓
4. Switch to --test-mode file (save to disk)
     ↓
5. Final review of saved emails
     ↓
6. Switch to --test-mode gmail (send real emails)
     ↓
7. Check campaign_report.json for results
```

---

## Output Files

After running campaigns, check these files:

- **test_emails/**: Saved emails (if using FileEmailSender)
- **campaign_report.json**: Campaign statistics and logs
- **test_email_report.json**: Alternative report format

---

## Examples

### Example 1: Quick Test (3 Predefined Recipients)
```bash
python intelligent_email_composer.py --test --test-mode console
```

### Example 2: Load Your Recipients and Preview
```bash
python intelligent_email_composer.py --create-csv
# Edit test_recipients.csv with your email addresses
python intelligent_email_composer.py --from-csv test_recipients.csv --test-mode console
```

### Example 3: Save Email Files for Review
```bash
python intelligent_email_composer.py --from-csv test_recipients.csv --test-mode file
# Check test_emails/ directory for generated files
```

### Example 4: Interactive Mode
```bash
python intelligent_email_composer.py --interactive
# Manually enter recipient details
```

### Example 5: Demo/Tutorial
```bash
python intelligent_email_composer.py
# Runs the complete demo with learning examples
```

---

## Troubleshooting

### Gmail Authentication Failed
- Ensure you're using an **App Password**, not your regular password
- Enable 2-Step Verification first
- Try with `--test-mode file` to verify email content first

### CSV File Not Found
- Make sure the CSV file exists in the current directory
- Use absolute paths if needed: `python intelligent_email_composer.py --from-csv /full/path/to/recipients.csv`

### Emails Not Sending
- Test with `--test-mode console` first to see email content
- Check email format in CSV (spaces around separators)
- Verify recipient email addresses are valid

---

## Tips for Testing

1. **Always start with console mode** to preview emails before sending
2. **Use test email addresses** (test@example.com) initially
3. **Save to files** before sending real emails
4. **Review the generated reports** after each campaign
5. **Test different relationships** (boss, colleague, client) to see tone variations
6. **Use key_points** to customize email content

---

## Safety Notes

- **Never commit passwords** to version control
- Use environment variables for sensitive data
- Test with mock recipients first
- Review emails in file mode before sending via Gmail
- Keep API credentials secure

---

## Enhancements Made

✅ Added 3 email sender classes (Console, File, Gmail)
✅ Created EmailCampaignManager for batch operations
✅ Added CSV loading functionality
✅ Implemented campaign reporting
✅ Added comprehensive CLI argument parsing
✅ Created test data generation
✅ Added email logging and tracking
