- For Termux Android [Download Here](https://f-droid.org/repo/com.termux_1020.apk) [F-Droid Version]
- For Termux Please Download This [libcurl-impersonate-chrome.so.4](https://github.com/ylasgamers/nodepay/raw/refs/heads/main/libcurl-impersonate-chrome.so.4) To Fix Error
- Copy To Folder /data/data/com.termux/files/usr/lib
- Example Command On Termux :
```
cp libcurl-impersonate-chrome.so.4 /data/data/com.termux/files/usr/lib
```
```
After Install Termux, Make Sure Allowed Permission Storage On Setting Termux
- Install Python 3.10
pkg update && upgrade
pkg install tur-repo
pkg install python-is-python3.10
- Install Requirements
pip install --upgrade pip
pkg install -y rust binutils
CARGO_BUILD_TARGET="$(rustc -Vv | grep "host" | awk '{print $2}')" pip install maturin
pip install requests
pip install asyncio
pip install aiohttp
pip install loguru
pip install cloudscraper
pip install curl_cffi
pip install fake_useragent
```
