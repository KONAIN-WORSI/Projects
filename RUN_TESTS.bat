@echo off
REM Intelligent Email Composer - Windows Batch Script for Testing
REM Quick access to common commands

setlocal enabledelayedexpansion

:menu
cls
echo.
echo ========================================================
echo  INTELLIGENT EMAIL COMPOSER - TESTING MENU
echo ========================================================
echo.
echo  1. Preview test emails (console mode)
echo  2. Save test emails to files
echo  3. Create sample recipients CSV
echo  4. Load recipients from CSV
echo  5. Interactive email composer
echo  6. Run full demo
echo  7. View help menu
echo  8. Show campaign report
echo  9. Open documentation
echo  10. Exit
echo.
set /p choice="Enter your choice (1-10): "

if "%choice%"=="1" goto preview
if "%choice%"=="2" goto savefile
if "%choice%"=="3" goto createcsv
if "%choice%"=="4" goto fromcsv
if "%choice%"=="5" goto interactive
if "%choice%"=="6" goto demo
if "%choice%"=="7" goto help
if "%choice%"=="8" goto report
if "%choice%"=="9" goto docs
if "%choice%"=="10" goto end

echo Invalid choice! Press any key to try again...
pause >nul
goto menu

:preview
echo.
echo [INFO] Generating test emails to console...
echo.
python intelligent_email_composer.py --test --test-mode console
pause
goto menu

:savefile
echo.
echo [INFO] Saving test emails to files...
echo.
python intelligent_email_composer.py --test --test-mode file
echo.
echo [OK] Emails saved to: test_emails\
echo.
pause
goto menu

:createcsv
echo.
echo [INFO] Creating sample recipients CSV...
echo.
python intelligent_email_composer.py --create-csv
echo.
echo [OK] Created: test_recipients.csv
echo [NEXT] Edit the CSV file with your recipients
echo.
pause
goto menu

:fromcsv
echo.
set /p csvfile="Enter CSV filename (default: test_recipients.csv): "
if "%csvfile%"=="" set csvfile=test_recipients.csv

if not exist "%csvfile%" (
    echo [ERROR] File not found: %csvfile%
    pause
    goto menu
)

echo.
echo [INFO] Loading recipients from %csvfile%...
echo.
python intelligent_email_composer.py --from-csv "%csvfile%" --test-mode console
pause
goto menu

:interactive
echo.
echo [INFO] Starting interactive mode...
echo [INFO] Follow the prompts to compose an email
echo.
python intelligent_email_composer.py --interactive
pause
goto menu

:demo
echo.
echo [INFO] Running full demo with learning...
echo.
python intelligent_email_composer.py
pause
goto menu

:help
echo.
echo [INFO] Showing help menu...
echo.
python intelligent_email_composer.py --help
pause
goto menu

:report
echo.
if exist test_email_report.json (
    echo [INFO] Latest campaign report:
    echo.
    type test_email_report.json
) else (
    echo [INFO] No campaign report found yet.
    echo [HINT] Run a test first: --test --test-mode console
)
echo.
pause
goto menu

:docs
echo.
echo Available Documentation:
echo.
if exist QUICK_REFERENCE.md (
    echo [1] QUICK_REFERENCE.md - One-page cheat sheet
)
if exist EMAIL_TESTING_GUIDE.md (
    echo [2] EMAIL_TESTING_GUIDE.md - Complete guide
)
if exist ENHANCEMENT_SUMMARY.md (
    echo [3] ENHANCEMENT_SUMMARY.md - What's new
)
if exist README_ENHANCEMENT.md (
    echo [4] README_ENHANCEMENT.md - Overview
)
if exist USAGE_EXAMPLES.py (
    echo [5] USAGE_EXAMPLES.py - Python code examples
)
echo.
set /p docnum="Enter document number to open (1-5) or press Enter to skip: "

if "%docnum%"=="1" if exist QUICK_REFERENCE.md start notepad QUICK_REFERENCE.md
if "%docnum%"=="2" if exist EMAIL_TESTING_GUIDE.md start notepad EMAIL_TESTING_GUIDE.md
if "%docnum%"=="3" if exist ENHANCEMENT_SUMMARY.md start notepad ENHANCEMENT_SUMMARY.md
if "%docnum%"=="4" if exist README_ENHANCEMENT.md start notepad README_ENHANCEMENT.md
if "%docnum%"=="5" if exist USAGE_EXAMPLES.py start notepad USAGE_EXAMPLES.py

goto menu

:end
echo.
echo [OK] Exiting...
echo.
pause
exit /b 0
