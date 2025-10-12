import phonenumbers
from phonenumbers import geocoder, carrier, timezone, number_type, PhoneNumberType
import requests, time

def start_phone_tracer(target):
    print(f'[+] phoneTracer v3.0 - OSINT')
    print(f'[*] Target: {target}')
    print(f'[*] Initiating trace...')
    time.sleep(1)

    try:
        p = phonenumbers.parse(target, None)
        if phonenumbers.is_valid_number(p):
            r = geocoder.description_for_number(p, "en")
            c = carrier.name_for_number(p, "en")
            tz = timezone.time_zones_for_number(p)
            nt = number_type(p)

            print(f'[+] Carrier: {c}')
            print(f'[+] Timezone: {tz}')
            print(f'[+] Location: {r}')
            print(f'[+] Type: {PhoneNumberType._VALUES_TO_NAMES[nt]}')

            # Optional IP-based enrichment
            ip_lookup()
        else:
            print("[!] Invalid number.")
    except Exception as e:
        print(f'[!] Error: {e}')
    print(f'[+] Trace complete')

def ip_lookup():
    try:
        ip_data = requests.get("https://ipinfo.io/json").json()
        print(f"[+] IP Location: {ip_data['city']}, {ip_data['region']}, {ip_data['country']}")
        print(f"[+] IP Coordinates: {ip_data['loc']}")
    except:
        print("[!] IP lookup failed.")

number = input('Enter the number with country code: ')
start_phone_tracer(number)