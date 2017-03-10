import os
import re
import threading
from urllib.request import urlopen

from decouple import config
from pushbullet import Device as _device
from pushbullet import PushBullet as _pb

SEC_ETF_URL = 'https://www.sec.gov/rules/sro/batsbzx.htm'
SEC_FTP_URL = 'https://www.sec.gov/rules/sro/batsbzx/2017/?C=M;O=A'


def main():
    if not config('PUSHBULLET_API_KEY'):
        print("You haven't configured PUSH!")

    check_etf(SEC_ETF_URL)
    check_ftp(SEC_FTP_URL)


def send_push(text):
    api_key = config('PUSHBULLET_API_KEY')
    device_id = config('PUSHBULLET_DEVICE_ID', None)
    device_info = {'iden': device_id}
    pb = _pb(api_key=api_key)
    api = _device(account=pb, device_info=device_info)
    title = 'Bitcoin ETF resuls!'
    body = text
    try:
        api.push_note(title, body)
        print('Successfully sent the Push')
    except:
        print('There was a problem sending your Push')


def notify(url):
    text = 'Bitcoin has been detected on ' + url
    print(text)
    send_push(text)


def check_etf(url):
    threading.Timer(15, check_etf, [url]).start()
    data = urlopen(url).read(
        20000)  # number of chars that should catch the announcement

    # Use lower case by default
    each_word = data.lower().split()

    if 'bitcoin' in each_word:
        notify(url)
        os._exit(0)
    else:
        print('No mention of bitcoin has been found yet on ' + url)


def check_ftp(url):
    threading.Timer(15, check_ftp, [url]).start()
    # number of chars that should catch the announcement
    data = urlopen(url).read(20000).decode('utf-8')

    # Use lower case by default
    words = data.lower().split()

    # Check for any new documents during the ten days after March 10th 2017
    matches = [string for string in words if re.match('1.-mar-2017', string)]
    if matches:
        notify(url)
        os._exit(0)
    else:
        print('No mention of bitcoin has been found yet on ' + url)


def test_notify():
    notify('Testing!')


if __name__ == '__main__':
    main()
