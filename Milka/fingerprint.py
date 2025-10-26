import random
import config
import mmh3

def generate_random():
    components = []

    screen_resolution   = random.choice(config.resolutions)
    screen_depth        = random.choice(config.screen_depths)
    language            = random.choice(config.languages)
    platform            = random.choice(config.platforms)
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

    fingerprint_hash = mmh3.hash128(values_string, seed = 31, signed = False)
    fingerprint = hex(fingerprint_hash)[2:]

    print(f"[{datetime.now()}] Generated fingerprint: {fingerprint}")
    return fingerprint