import requests, json, re, time
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from random import randint

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

def save_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

config = load_config()
discord_token = config['discord_token']
session_id = config['session_id']
redeem_token = config['redeem_token']

minestrator_session = requests.Session()
minestrator_session.cookies.set('PHPSESSID', session_id)

def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def log_message(message, level="info"):
    colors = {
        "info": "36",      # Cyan
        "success": "32",   # Green
        "warning": "33",   # Yellow
        "error": "31",     # Red
    }
    color = colors.get(level, "36")  # Default to Cyan for info
    print(f"{color_text(f'[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]', color)} {message}")

def update_session_id(response):
    global session_id
    new_session_id = response.cookies.get('PHPSESSID')
    if new_session_id and new_session_id != session_id:
        log_message(f"Session ID has changed from {session_id} to {new_session_id}. Updating config...", "warning")
        session_id = new_session_id
        config['session_id'] = session_id
        save_config(config)
        return True
    return False

def getLastCodes():
    log_message("Fetching the latest codes from Discord...", "info")
    discord_url = "https://discord.com/api/v9/channels/630777266187534347/messages?limit=50"
    discord_payload = {}
    discord_headers = {
        'accept': '*/*',
        'accept-language': 'fr,fr-FR;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'authorization': discord_token,
        'priority': 'u=1, i',
        'referer': 'https://discord.com/channels/301334764768722945/374620561080582145',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        'x-debug-options': 'bugReporterEnabled',
        'x-discord-locale': 'fr',
        'x-discord-timezone': 'Europe/Paris',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImZyIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNy4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMjcuMC4wLjAiLCJicm93c2VyX3ZlcnNpb24iOiIxMjcuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MzE2Mzk3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
    }

    try:
        discord_response = minestrator_session.get(discord_url, headers=discord_headers, data=discord_payload)
        messages = discord_response.json()

        time_limit = datetime.now(timezone.utc) - timedelta(hours=1)

        def parse_timestamp(timestamp):
            return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

        code_pattern = r'\|\|([A-Z0-9\-]+)\|\|'

        recent_messages = [
            message for message in messages
            if parse_timestamp(message['timestamp']) > time_limit
        ]

        messages_with_codes = [
            message for message in recent_messages
            if re.search(code_pattern, message['content'])
        ]

        latest_message_with_codes = max(
            messages_with_codes,
            key=lambda x: parse_timestamp(x['timestamp']),
            default=None
        )

        if latest_message_with_codes:
            content = latest_message_with_codes['content']
            codes = re.findall(code_pattern, content)
            log_message(f"Found {len(codes)} code(s) in the latest message.", "success")
            return codes
        else:
            log_message("No codes found in the recent messages.", "warning")
            return []

    except Exception as e:
        log_message(f"Error fetching codes: {e}", "error")
        return []

def getAirDropTime():
    log_message("Fetching the next airdrop time...", "info")
    airdrop_url = "https://minestrator.com/panel/code/cadeau"
    headers = {
        'Cookie': f'PHPSESSID={session_id}',
    }
    try:
        airdrop_response = requests.get(airdrop_url, headers=headers)
        if update_session_id(airdrop_response):
            # Re-fetch airdrop time if session ID has changed
            airdrop_response = requests.get(airdrop_url, headers=headers)

        soup = BeautifulSoup(airdrop_response.text, 'html.parser')
        spans = soup.find_all('span', class_='font-size-30')

        if len(spans) >= 2:
            date_format = "%d/%m/%Y à %H:%M"
            dt = datetime.strptime(spans[1].text, date_format)
            log_message(f"Next airdrop is scheduled for {dt.strftime('%Y-%m-%d %H:%M:%S')}.", "success")
            return dt.timestamp()
        else:
            log_message("Failed to find the airdrop time on the page.", "warning")
            return False

    except Exception as e:
        log_message(f"Error fetching airdrop time: {e}", "error")
        return False

def redeemCodes():
    codes = getLastCodes()
    redeem_url = "https://minestrator.com/panel/action.php?action=codecadeau"
    headers = {
        'Cookie': f'PHPSESSID={session_id}',
    }

    for code in codes:
        log_message(f"Attempting to redeem code: {code}", "info")
        time.sleep(randint(3, 7))
        payload = {
            'code': code,
            'token': redeem_token,
        }

        try:
            redeem_response = requests.post(redeem_url, data=payload, headers=headers)
            if update_session_id(redeem_response):
                # Re-attempt redemption if session ID has changed
                redeem_response = requests.post(redeem_url, data=payload, headers=headers)

            response_data = redeem_response.json()

            if response_data["result"] != 500:
                log_message(f"Code redeemed successfully: {code}", "success")
                break
            else:
                log_message(f"Failed to redeem code: {code}. Trying next code if available.", "warning")

        except Exception as e:
            log_message(f"Error redeeming code {code}: {e}", "error")

def main():
    airdrop_time = getAirDropTime()
    
    while airdrop_time:
        current_time = int(time.time())
        sleep_time = airdrop_time - current_time
        
        if sleep_time > 1800:
            log_message(f"Sleeping for 30 minutes. {int(sleep_time//3600)} hours and {int((sleep_time%3600)//60)} minutes remaining until airdrop.", "info")
            time.sleep(1800)
        else:
            log_message(f"Sleeping for {sleep_time} seconds until airdrop time.", "info")
            time.sleep(sleep_time)
            log_message("Airdrop is happening now!", "warning")
            redeemCodes()

        airdrop_time = getAirDropTime()

if __name__ == "__main__":
    while True:
        main()
