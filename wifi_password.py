import subprocess

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')

profiles = []
for i in data:
    if 'All User Profile' in i:
        profiles.append(i.split(':')[1][1:-1])

for profile in profiles:
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')

        result = []

        for b in results:
            if 'Key Content' in b:
                result.append(b.split(':')[1][1:-1])

        try:
            print("{:<30} | {:<}".format(profile, result[0]))
        except Exception as e:
            print("{:<30} | {:<}".format(profile, ""))
    except Exception as e:
        print("{:<30} | {:<}".format(profile, "ERROR OCCURED"))

