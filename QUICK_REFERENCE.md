# Intelligent Email Composer - Quick Reference

## Installation
No additional Python packages needed beyond what's in intelligent_email_composer.py

```bash
# Built-in packages used:
# - smtplib, email.mime (for email sending)
# - csv (for data loading)
# - json, re, datetime, pathlib, argparse
```

---

## 🚀 Quick Commands

### 1. See It in Action
```bash
python intelligent_email_composer.py --test --test-mode console
```

### 2. Save to Files
```bash
python intelligent_email_composer.py --test --test-mode file
```

### 3. Create Recipients List
```bash
python intelligent_email_composer.py --create-csv
```

### 4. Load Custom Recipients
```bash
python intelligent_email_composer.py --from-csv test_recipients.csv --test-mode console
```

### 5. Send Real Emails
```bash
python intelligent_email_composer.py --test --test-mode gmail --gmail-email YOUR_EMAIL --gmail-password YOUR_PASS
```

---

## 📊 What Gets Created

| File/Folder | Purpose |
|-------------|---------|
| `test_recipients.csv` | Sample recipient list (edit to customize) |
| `test_emails/` | Folder with saved email files |
| `test_email_report.json` | Campaign statistics and logs |
| `EMAIL_TESTING_GUIDE.md` | Full documentation |
| `ENHANCEMENT_SUMMARY.md` | What was added |
| `USAGE_EXAMPLES.py` | Python code examples |

---

## 🎯 Different Sending Modes

| Mode | Use Case | Command |
|------|----------|---------|
| **console** | Preview emails | `--test-mode console` |
| **file** | Save and review | `--test-mode file` |
| **gmail** | Send real emails | `--test-mode gmail` |

---

## 📋 CSV Format

**File:** `test_recipients.csv`

```csv
name,email,relationship,topic,urgency,key_points
John Doe,john@company.com,colleague,Code Review,normal,PR #123|Feedback|Thanks
Jane Smith,jane@company.com,boss,Status Update,high,Progress|Issues|Timeline
Client Co,contact@client.com,client,Invoice #123,urgent,Payment|Due date|Details
```

**Relationships:** colleague, boss, client, friend, vendor, recruiter, mentor

**Urgency:** low, normal, high, urgent

**Key Points:** Separate with `|` pipe character

---

## 💻 Python Usage

### Simple Email
```python
from intelligent_email_composer import *

composer = IntelligentEmailComposer("Your Name")
context = EmailContext(
    recipient_name="John",
    recipient_email="john@company.com",
    relationship="colleague",
    topic="Meeting",
    key_points=["Discuss timeline"]
)
email = composer.compose(context)
print(email)
```

### Batch Emails
```python
composer = IntelligentEmailComposer("System")
sender = ConsoleEmailSender()  # or FileEmailSender(), GmailSender()
manager = EmailCampaignManager(composer, sender)

contexts = [context1, context2, context3]
report = manager.send_batch(contexts)
print(f"Sent: {report['sent']}, Failed: {report['failed']}")
```

### From CSV
```python
manager = EmailCampaignManager(composer, sender)
contexts = manager.load_test_recipients("recipients.csv")
manager.send_batch(contexts)
```

---

## 🔐 Gmail Setup (One-Time)

1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Generate "App Password" for Gmail
4. Use in commands above

**Never share your app password!**

---

## 🛡️ Safety Workflow

```
STEP 1: Preview
  └─ python intelligent_email_composer.py --test --test-mode console
     ↓ See emails in terminal

STEP 2: Save to Files  
  └─ python intelligent_email_composer.py --test --test-mode file
     ↓ Review files in test_emails/ folder

STEP 3: Load Custom Recipients
  └─ Create/edit test_recipients.csv
     ↓ python intelligent_email_composer.py --from-csv test_recipients.csv --test-mode console
     ↓ Verify emails before sending

STEP 4: Send Real Emails
  └─ python intelligent_email_composer.py --from-csv test_recipients.csv --test-mode gmail
     ↓ Check test_email_report.json for results
```

---

## 📈 Campaign Reports

After each campaign, check `test_email_report.json`:

```json
{
  "total": 3,
  "sent": 3,
  "failed": 0,
  "success_rate": "100.0%",
  "sent_log": [
    {
      "timestamp": "2026-03-31T17:40:25.705007",
      "recipient": "john@example.com",
      "subject": "Meeting: Q3 Review",
      "relationship": "colleague",
      "success": true
    }
  ]
}
```

---

## 🎓 Email Intelligence Features

The composer automatically:
- ✅ Detects email type (meeting, follow-up, request, introduction)
- ✅ Chooses appropriate tone (casual, professional, formal, friendly)
- ✅ Generates personalized subject lines
- ✅ Creates contextual email body
- ✅ Adds urgency markers if needed
- ✅ Learns from sent emails to improve future messages

---

## 📁 File Structure

```
d:\konain\project_1\
├── intelligent_email_composer.py      ← Main enhanced file
├── EMAIL_TESTING_GUIDE.md             ← Full documentation
├── ENHANCEMENT_SUMMARY.md             ← What was added
├── USAGE_EXAMPLES.py                  ← Code examples
├── test_recipients.csv                ← Sample recipients (auto-created)
├── test_emails/                       ← Saved emails (auto-created)
│   ├── 20260331_174025_john.test.txt
│   ├── 20260331_174026_sarah.test.txt
│   └── 20260331_174027_mike.test.txt
└── test_email_report.json             ← Campaign report (auto-created)
```

---

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| "Gmail login failed" | Check app password setup, enable 2FA |
| "File not found" | Use correct path, check CSV exists |
| "Email not sending" | Try `--test-mode console` first to check content |
| "Report not created" | Ensure write permissions in current directory |

---

## ⚡ One-Liners

```bash
# Just test with console
python intelligent_email_composer.py --test

# Generate sample CSV
python intelligent_email_composer.py --create-csv

# Load CSV and preview
python intelligent_email_composer.py --from-csv test_recipients.csv

# Interactive mode
python intelligent_email_composer.py --interactive

# Full demo with examples
python intelligent_email_composer.py
```

---

## 🔄 Relationships & Tone Mapping

| Relationship | Suggested Tone(s) |
|------------|-------------------|
| boss | formal, professional |
| client | professional, formal |
| colleague | professional, friendly |
| friend | casual, friendly |
| vendor | professional |
| recruiter | professional, formal |
| mentor | professional, friendly |

---

## 📚 More Information

- Full guide: See `EMAIL_TESTING_GUIDE.md`
- What changed: See `ENHANCEMENT_SUMMARY.md`
- Code examples: See `USAGE_EXAMPLES.py`
- In-code docs: Read `intelligent_email_composer.py` docstrings

---

## 🎉 You're Ready!

Go to terminal and run:
```bash
python intelligent_email_composer.py --test --test-mode console
```

Enjoy automated intelligent email composition! 🚀
