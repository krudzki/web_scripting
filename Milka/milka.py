import time
import random
from datetime import datetime, timedelta
import requests
import mmh3
import chrome_data

MILKA_URL = "https://promocjamilka.pl/"

USER_DATA = {
    "email":    "template@email.com",
    "phone":    "48 000-00-000",
    "name":     "Sweeet Chocolate",
    "street":   "Uhmm",
    "house_nr": "0", # Numer domu/mieszkania albo poprostu np 3 albo 12/19 albo cos nie wiem
    "postal":   "00-000",
    "city":     "Uhmm"
}

chrome_version = random.choice(chrome_data.chrome_versions)
user_agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36"

def generate_fingerprint():
    components = []

    resolutions = [
        "1920x1080", 
        "1920x1200", 
        "2560x1440", 
        "1366x768", 
        "1680x1050", 
        "1440x900"
    ]

    languages = [
        "pl-PL", 
        "pl"
    ]

    screen_depths = [
        "24", 
        "32"
    ]

    platforms = [
        "Win32", 
        "Windows", 
        "Win64"
    ]

    screen_resolution   = random.choice(resolutions)
    screen_depth        = random.choice(screen_depths)
    language            = random.choice(languages)
    platform            = random.choice(platforms)
    cookie_enabled      = random.choice(["true", "true", "true", "false"])
    touch_support       = random.choice(["false", "false", "false", "false", "true"])

    components.append({
        "key": "user_agent", 
        "value": user_agent
    })

    components.append({
        "key": "screen_resolution", 
        "value": screen_resolution
    })

    components.append({
        "key": "screen_depth", 
        "value": screen_depth
    })

    components.append({
        "key": "timezone", 
        "value": "Europe/Warsaw"
    })

    components.append({
        "key": "language", 
        "value": language
    })

    components.append({
        "key": "platform", 
        "value": platform
    })
    
    components.append({
        "key": "cookie_enabled", 
        "value": cookie_enabled
    })

    components.append({
        "key": "touch_support", 
        "value": touch_support
    })

    values_string = ""

    for comp in components:
        values_string += comp["value"]

    fingerprint_hash = mmh3.hash128(values_string, seed=31, signed=False)
    fingerprint = hex(fingerprint_hash)[2:]

    print(f"[{datetime.now()}] Generated fingerprint: {fingerprint}")
    return fingerprint

def wait_for_time(target_time):
    now = datetime.now()
    time_to_wait = (target_time - now).total_seconds()

    if time_to_wait > 0:
        print(f"[{now}] Waiting {time_to_wait:.2f} seconds to {target_time.strftime('%H:%M:%S')}...")
        time.sleep(time_to_wait)

def submit_form_directly():
    try:
        print(f"[{datetime.now()}] Attempt to send the form directly...")

        fingerprint = generate_fingerprint()

        chromium_versions = [
            "120", 
            "119", 
            "121", 
            "118", 
            "140"
        ]

        chromium_version = random.choice(chromium_versions)
        sec_ch_ua = f'"Chromium";v="{chromium_version}", "Not=A?Brand";v="24", "Microsoft Edge";v="{chromium_version}"'

        headers = {
            'Content-Type':                 'multipart/form-data; boundary=----WebKitFormBoundaryTvzPsgqliiPfsthz',
            'Origin':                       'null',
            'Upgrade-Insecure-Requests':    '1',
            'User-Agent':                   user_agent,
            'sec-ch-ua':                    sec_ch_ua,
            'sec-ch-ua-mobile':             '?0',
            'sec-ch-ua-platform':           '"Windows"'
        }

        form_data = {
            "email":            USER_DATA["email"],
            "phone":            USER_DATA["phone"],
            "name":             USER_DATA["name"],
            "street":           USER_DATA["street"],
            "house_nr":         USER_DATA["house_nr"],
            "postal":           USER_DATA["postal"],
            "city":             USER_DATA["city"],
            "data1":            "on",
            "data2":            "on",
            "dodaj_zgloszenie": "correct",
            "fingerprint":      fingerprint
        }

        boundary = '----WebKitFormBoundaryTvzPsgqliiPfsthz'
        body_parts = []

        for key, value in form_data.items():
            body_parts.append(f'--{boundary}')
            body_parts.append(f'Content-Disposition: form-data; name="{key}"')
            body_parts.append('')
            body_parts.append(str(value))

        body_parts.append(f'--{boundary}--')
        body = '\r\n'.join(body_parts)

        response = requests.post('https://promocjamilka.pl/add.php', headers=headers, data=body.encode('utf-8'))

        print(f"[{datetime.now()}] Response status: {response.status_code}")
        print(f"[{datetime.now()}] Response content: {response.text}")

        response_text = response.text.lower()

        if (
            'dziękujemy' in response_text 
            or 'zgłoszenie zostało przyjęte' in response_text
        ):
            print(f"[{datetime.now()}] SUCCESS: Application accepted!")
            return True
        elif 'podane dane zostały już zgłoszone' in response_text:
            print(f"[{datetime.now()}] DATA ALREADY SUBMITTED: {response.text.strip()}")
            return False  # Ponów próbę później
        elif 'dzienna pula wyczerpała się' in response_text:
            print(f"[{datetime.now()}] POOL EXHAUSTED: {response.text.strip()}")
            return False  # Zatrzymaj na dziś
        elif (
            'niepoprawne' in response_text 
            or 'sprawdź poprawność' in response_text
        ):
            print(f"[{datetime.now()}] INCORRECT DATA: {response.text.strip()}")
            return False  # Ponów próbę
        elif (
            'wielokrotnego wysłania' in response_text 
            or 'nie jestem robotem' in response_text
        ):
            print(f"[{datetime.now()}] CAPTCHA ERROR: {response.text.strip()}")
            return False  # Ponów próbę
        else:
            print(f"[{datetime.now()}] UNKNOWN RESULT: {response.text.strip()}")
            return True  # Załóż sukces

    except Exception as e:
        print(f"[{datetime.now()}] Error sending form: {e}")
        return False

def main():
    print("Launching the bot to send the Milka form...")
    print(f"Target URL: {MILKA_URL}")
    print("=" * 60)

    while True:
        now = datetime.now()
        target_run_time = now.replace(hour=8, minute=0, second=0, microsecond=500000)

        if now > target_run_time:
            print(f"[{now}] It's alredy over 8:00. Next try tomorrow.")
            target_run_time += timedelta(days=1)
        
        wait_for_time(target_run_time)
        
        print(f"[{datetime.now()}] Target time achieved! I'm sending the form ...")

        while not submit_form_directly():
            retry_delay = random.randint(1, 3)
            print(f"[{datetime.now()}] Sending failed. I'm trying again for {retry_delay} seconds...")
            time.sleep(retry_delay)

        print(f"[{datetime.now()}] Your submission has been successfully sent. I'm stopping the bot.")
        break

if __name__ == "__main__":
    main()