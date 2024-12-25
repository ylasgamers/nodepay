import requests
import time

print(f'For Active New Account Nodepay | Multiple Account!')

with open('token_list.txt', 'r') as file:
    try:
        local_data = file.read().splitlines()
        for tokenlist in local_data:
            url = f"http://api.nodepay.ai/api/auth/active-account?"
            headers = {
                "Authorization": f"Bearer {tokenlist}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "Content-Type": "application/json",
                "Origin": "chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm",
                "Accept": "application/json",
                "Accept-Language": "en-US,en;q=0.5",
            }
            
            data = {}

            response = requests.post(url, headers=headers, json=data)
            result = response.json().get('msg')
            if result == 'Account is already activated':
                print(f'np_token {tokenlist}')
                print(f'{result}')
                print(f'------------------------------------')
            else:
                print(f'np_token {tokenlist}')
                print(f'{result}')
                print(f'------------------------------------')
    except Exception as e:
        print(str(e))