# 🎯 EXACT COMMANDS - Copy and Paste

These are the exact commands you can run right now. Just copy and paste!

## 1. See Test Emails in Terminal (Recommended First Step)

```bash
python intelligent_email_composer.py --test --test-mode console
```

**What it does:**
- Generates 3 sample test emails
- Shows them in your terminal
- Creates a success report
- Takes: ~2 seconds

**Expected Output:**
- 3 emails displayed (John, Sarah, Mike)
- Report: 100% success rate
- Report saved to `test_email_report.json`

---

## 2. Save Test Emails to Files

```bash
python intelligent_email_composer.py --test --test-mode file
```

**What it does:**
- Generates 3 sample test emails
- Saves them as .txt files
- Creates folder: `test_emails/`
- Takes: ~2 seconds

**Check Results:**
```
test_emails/20260331_174025_john.test.txt
test_emails/20260331_174026_sarah.test.txt
test_emails/20260331_174027_mike.test.txt
```

---

## 3. Create Your Recipients List

```bash
python intelligent_email_composer.py --create-csv
```

**What it does:**
- Creates `test_recipients.csv`
- 3 sample recipients included
- Ready to edit with your emails

**Edit the file:**
```
name,email,relationship,topic,urgency,key_points
John Doe,john@company.com,colleague,Code Review,normal,PR #123|Feedback|Thanks
```

---

## 4. Load Recipients and Preview

```bash
python intelligent_email_composer.py --from-csv test_recipients.csv --test-mode console
```

**What it does:**
- Loads recipients from CSV
- Generates personalized emails
- Shows in terminal
- Takes: ~1 second per recipient

---

## 5. Save Your Recipients' Emails to Files

```bash
python intelligent_email_composer.py --from-csv test_recipients.csv --test-mode file
```

**What it does:**
- Loads CSV recipients
- Generates personalized emails
- Saves files to `test_emails/`
- Creates report

**Check the folder:**
```
test_emails/20260331_175000_john@company.com.txt
test_emails/20260331_175000_sarah@company.com.txt
```

---

## 6. Send Real Emails (Gmail)

### Step 1: Get Gmail App Password (One-time setup)

1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification" (if not already)
3. Go to "App Passwords"
4. Select Gmail app
5. Copy the 16-character password

### Step 2: Send Emails

```bash
python intelligent_email_composer.py --test --test-mode gmail --gmail-email your@gmail.com --gmail-password your16charpassword
```

**What it does:**
- Sends 3 actual emails via Gmail
- Each takes ~1-2 seconds
- Creates report with delivery status

**Check Report:**
```
test_email_report.json
```

---

## 7. Interactive Mode (Step-by-Step)

```bash
python intelligent_email_composer.py --interactive
```

**What happens:**
- Asks for recipient name
- Asks for email address
- Asks for relationship type
- Asks for topic
- Asks for urgency level
- Asks for tone preference
- Asks for key points
- Shows generated email
- Optionally saves pattern

---

## 8. Run Full Demo

```bash
python intelligent_email_composer.py
```

**What it does:**
- Runs 5 example scenarios
- Shows learning in action
- Displays analytics
- Educational demonstration

---

## 9. Show Help Menu

```bash
python intelligent_email_composer.py --help
```

**Shows:**
- All available arguments
- Default values
- Usage examples

---

## Windows Users - Easy Menu

```bash
RUN_TESTS.bat
```

**What it does:**
- Opens interactive menu
- 10 options to choose from
- Click and go!

**Menu Options:**
1. Preview test emails
2. Save test emails
3. Create CSV
4. Load from CSV
5. Interactive mode
6. Full demo
7. Help menu
8. View report
9. Open documentation
10. Exit

---

## Advanced: Load Custom CSV

### Create your own recipients.csv:

```csv
name,email,relationship,topic,urgency,key_points
Alice,alice@company.com,boss,Q3 Results,high,Progress|Metrics|Forecast
Bob,bob@company.com,colleague,Code Review,normal,PR #789|Feedback welcome
Carol,carol@company.com,client,Invoice Follow-up,urgent,Payment due|Details|Contact
Dave,dave@company.com,friend,Weekend Plans,normal,Availability|Location|Time
```

### Then run:

```bash
python intelligent_email_composer.py --from-csv recipients.csv --test-mode console
```

---

## Real World Scenarios

### Scenario 1: Test 10 New Colleagues

```bash
# 1. Create CSV with 10 colleagues
# 2. Preview with console mode:
python intelligent_email_composer.py --from-csv colleagues.csv --test-mode console

# 3. Review in files:
python intelligent_email_composer.py --from-csv colleagues.csv --test-mode file

# 4. Send when ready (if Gmail setup done):
python intelligent_email_composer.py --from-csv colleagues.csv --test-mode gmail --gmail-email YOUR_EMAIL --gmail-password APP_PASS
```

### Scenario 2: Send to All Customers

```bash
# Assuming you have: customers.csv
python intelligent_email_composer.py --from-csv customers.csv --test-mode file
# Review emails in test_emails/ folder
# Then send:
python intelligent_email_composer.py --from-csv customers.csv --test-mode gmail --gmail-email YOUR_EMAIL --gmail-password APP_PASS
```

### Scenario 3: Test Different Tones

```bash
# Create: test_tones.csv
# Column "tone" can be: casual, professional, formal, friendly

python intelligent_email_composer.py --from-csv test_tones.csv --test-mode console
```

---

## Checking Results

### View Campaign Report:

```bash
type test_email_report.json
```

**Shows:**
- Total emails sent
- Number succeeded
- Number failed
- Success percentage
- Detailed log with timestamps

### View Saved Emails:

```bash
cd test_emails
dir
```

**See:**
- All saved email files
- Timestamps in filename
- Ready to review line-by-line

---

## Troubleshooting Commands

### Check if Python is installed:
```bash
python --version
```

### Check if script runs:
```bash
python intelligent_email_composer.py --help
```

### Test console output (safe):
```bash
python intelligent_email_composer.py --test --test-mode console
```

### Check saved emails:
```bash
ls test_emails/
```
or
```bash
dir test_emails\
```

### View report:
```bash
type test_email_report.json
```

---

## Batch Command Examples

### Send to Multiple CSV Files:

```bash
# Campaign 1
python intelligent_email_composer.py --from-csv list1.csv --test-mode file

# Campaign 2
python intelligent_email_composer.py --from-csv list2.csv --test-mode file

# Campaign 3
python intelligent_email_composer.py --from-csv list3.csv --test-mode file
```

### Delay Between Emails (Helpful):

The batch command waits 1 second between emails by default. To check/change this:
- Edit intelligent_email_composer.py
- Find: `manager.send_batch(contexts, delay_seconds=1)`
- Change 1 to your desired delay in seconds

---

## Quick Copy-Paste Reference

| Action | Command |
|--------|---------|
| Test | `python intelligent_email_composer.py --test` |
| Test (save to files) | `python intelligent_email_composer.py --test --test-mode file` |
| Create CSV | `python intelligent_email_composer.py --create-csv` |
| Send from CSV | `python intelligent_email_composer.py --from-csv test_recipients.csv` |
| Interactive | `python intelligent_email_composer.py --interactive` |
| Demo | `python intelligent_email_composer.py` |
| Help | `python intelligent_email_composer.py --help` |
| Windows Menu | `RUN_TESTS.bat` |

---

## Environment Variable Setup (Optional - For Production)

Instead of passing passwords in command line:

```bash
set GMAIL_PASS=your-app-password
python intelligent_email_composer.py --test --test-mode gmail --gmail-email your@gmail.com --gmail-password %GMAIL_PASS%
```

---

## Summary

The simplest path:
1. `python intelligent_email_composer.py --test --test-mode console` (preview)
2. `python intelligent_email_composer.py --test --test-mode file` (save files)
3. Check `test_emails/` folder
4. When ready: Setup Gmail and use `--test-mode gmail`

All commands work right now. No additional installation needed!

Happy emailing! 🚀📧
