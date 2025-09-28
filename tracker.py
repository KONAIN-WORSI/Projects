import phonenumbers
from phonenumbers import geocoder , carrier , timezone
import time , random

number = input('Enter the number along with its country code in it: ')

def start_phone_tracer(target):
    print(f'[+] phoneTracer v2.1 - OSINT')
    print(f'[*] Target: {target}')
    print(f'[*] Initating trace....')
    try:
        p = phonenumbers.parse(target, None)
        r = geocoder.description_for_number(p, "en")
        c = carrier.name_for_number(p, "en")
        tz = timezone.time_zones_for_number(p)
        print(f'[+] Carrier: {c}')
        print(f'[+] Timezone: {tz}')
        print(f'[+] Location: {r}')
    except Exception as e:
        print(f'[!] Error: {e}')
    print(f'[+] Trace complete')

start_phone_tracer(number)