import asyncio
import time
import uuid
from curl_cffi import requests
from loguru import logger
from fake_useragent import UserAgent

def show_warning():
    confirm = input("By using this tool means you understand the risks. do it at your own risk! \nPress Enter to continue or Ctrl+C to cancel... ")

    if confirm.strip() == "":
        print("Continuing...")
    else:
        print("Exiting...")
        exit()

# Constants
PING_INTERVAL = 60
RETRIES = 60

DOMAIN_API = {
    "SESSION": "http://api.nodepay.ai/api/auth/session",
    "PING": "https://nw.nodepay.org/api/network/ping"
}

CONNECTION_STATES = {
    "CONNECTED": 1,
    "DISCONNECTED": 2,
    "NONE_CONNECTION": 3
}

status_connect = CONNECTION_STATES["NONE_CONNECTION"]
browser_id = None
account_info = {}
last_ping_time = {}

def uuidv4():
    return str(uuid.uuid4())

def valid_resp(resp):
    if not resp or "code" not in resp or resp["code"] < 0:
        raise ValueError("Invalid response")
    return resp

async def render_profile_info(token):
    global browser_id, account_info

    try:
        np_session_info = load_session_info()

        if not np_session_info:
            # Generate new browser_id
            browser_id = uuidv4()
            response = await call_api(DOMAIN_API["SESSION"], {}, token)
            valid_resp(response)
            account_info = response["data"]
            if account_info.get("uid"):
                save_session_info(account_info)
                await start_ping(token)
            else:
                handle_logout()
        else:
            account_info = np_session_info
            await start_ping(token)
    except Exception as e:
        logger.error(f"Error in render_profile_info: {e}")
        error_message = str(e)
        if any(phrase in error_message for phrase in [
            "sent 1011 (internal error) keepalive ping timeout; no close frame received",
            "500 Internal Server Error"
        ]):
            logger.info("Removing error session and retrying")
            return None
        else:
            logger.error(f"Connection error: {e}")
            return None

async def call_api(url, data, token):
    user_agent = UserAgent(os=['windows', 'macos', 'linux'], browsers='chrome')
    random_user_agent = user_agent.random
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": random_user_agent,
        "Content-Type": "application/json",
        "Origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
    }

    try:
        response = requests.post(url, json=data, headers=headers, impersonate="chrome110", timeout=30)

        response.raise_for_status()
        return valid_resp(response.json())
    except Exception as e:
        logger.error(f"Error during API call: {e}")
        raise ValueError(f"Failed API call to {url}")

async def start_ping(token):
    try:
        while True:
            await ping(token)
            await asyncio.sleep(PING_INTERVAL)
    except asyncio.CancelledError:
        logger.info("Ping task was cancelled")
    except Exception as e:
        logger.error(f"Error in start_ping: {e}")

async def ping(token):
    global last_ping_time, RETRIES, status_connect

    current_time = time.time()

    if (current_time - last_ping_time.get(token, 0)) < PING_INTERVAL:
        logger.info(f"Skipping ping, not enough time elapsed")
        return

    last_ping_time[token] = current_time

    try:
        data = {
            "id": account_info.get("uid"),
            "browser_id": browser_id,
            "timestamp": int(time.time()),
            "version": "2.2.7"
        }

        response = await call_api(DOMAIN_API["PING"], data, token)
        if response["code"] == 0:
            logger.info(f"Ping successful: {response} with id: {account_info.get('uid')}")
            RETRIES = 0
            status_connect = CONNECTION_STATES["CONNECTED"]
        else:
            handle_ping_fail(response)
    except Exception as e:
        logger.error(f"Ping failed: {e}")
        handle_ping_fail(None)

def handle_ping_fail(response):
    global RETRIES, status_connect

    RETRIES += 1
    if response and response.get("code") == 403:
        handle_logout()
    elif RETRIES < 2:
        status_connect = CONNECTION_STATES["DISCONNECTED"]
    else:
        status_connect = CONNECTION_STATES["DISCONNECTED"]

def handle_logout():
    global status_connect, account_info

    status_connect = CONNECTION_STATES["NONE_CONNECTION"]
    account_info = {}
    save_status(None)
    logger.info("Logged out and cleared session info")

def load_tokens(token_file):
    try:
        with open(token_file, 'r') as file:
            tokens = file.read().splitlines()
        return tokens
    except Exception as e:
        logger.error(f"Failed to load tokens: {e}")
        raise SystemExit("Exiting due to failure in loading tokens")

def save_status(status):
    pass

def save_session_info(data):
    data_to_save = {
        "uid": data.get("uid"),
        "browser_id": browser_id
    }
    pass

def load_session_info():
    return {}

async def main():
    all_tokens = load_tokens('token_list.txt')  # Load tokens from file

    if not all_tokens:
        print("No tokens found in token_list.txt. Exiting the program.")
        exit()

    tasks = []
    for token in all_tokens:
        tasks.append(asyncio.create_task(render_profile_info(token)))

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    show_warning()
    print("\nAlright, we here! Running the script with tokens from token_list.txt.")
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Program terminated by user.")
