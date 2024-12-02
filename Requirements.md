- Recomended Using Python 3.10
- For Windows [Download Here x64](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe) [Scrool Down For Other Version]
- Maybe For Windows 10 Or Higher You Can Install Python 3.10 From Microsoft Store
```
- Install Requirements
python -m pip install pip --upgrade
pip install requests
pip install asyncio
pip install aiohttp
pip install loguru
pip install cloudscraper
pip install curl_cffi==0.8.0b7
pip install fake_useragent
```
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
pip install curl_cffi==0.8.0b7
pip install fake_useragent
```
- For Ubuntu 18.04 | 20.04 | 22.04 (VPS)
```
- Install Python 3.10
apt update && sudo apt upgrade -y
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa
apt install python3.10
apt install python3-pip
- Install Requirements
pip install requests
pip install asyncio
pip install aiohttp
pip install loguru
pip install cloudscraper
pip install curl_cffi==0.8.0b7
pip install fake_useragent
```
