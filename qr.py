import re
import time
import requests
import qrcode
from PIL import Image, ImageDraw, ImageFont
import random

def GET(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Accept': 'application/json, text/javascript',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    return requests.get(url, headers=headers)

def GET_h(url, ttwid, passport_csrf_token):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Accept': 'application/json, text/javascript',
        'Content-Type': 'application/x-www-form-urlencoded',
        'cookie': f'ttwid={ttwid}; passport_csrf_token={passport_csrf_token};',
        'x-tt-passport-csrf-token': f'{passport_csrf_token}'
    }
    return requests.get(url, headers=headers)

def convert_escape_sequence(s):
    return s.encode().decode('unicode_escape')

def short_url(url_to_short):
    url = "https://www.tiktok.com/shorten/?aid=1988"
    payload = {
        'targets': url_to_short,
        'belong': 'tiktok-webapp-qrcode'
    }
    response = requests.post(url, data=payload)
    url_shorten_list = re.findall(r'"short_url":"(.*?)"', response.text)
    url_shorten = url_shorten_list[0] if url_shorten_list else None
    return url_shorten

def get_qrcode_url():
    url = "https://www.tiktok.com/passport/web/get_qrcode/?next=https://www.tiktok.com&aid=1459"
    response = requests.post(url)
    cookies = response.cookies

    passport_csrf_token = cookies.get('passport_csrf_token')
    ttwid = GET('https://www.tiktok.com/login/qrcode')
    ttwid = ttwid.cookies.get('ttwid')

    token_match = re.search(r'"token":"(.*?)"', response.text)
    qrcode_index_url_match = re.search(r'"qrcode_index_url":"(.*?)"', response.text)

    token = token_match.group(1) if token_match else None
    qrcode_index_url = qrcode_index_url_match.group(1) if qrcode_index_url_match else None
    qrcode_index_url = convert_escape_sequence(qrcode_index_url)

    shorten_url = short_url(qrcode_index_url)
    
    if shorten_url:
        print(f"Enter URL on your browser: {shorten_url}")
        gen(shorten_url)
    return token, ttwid, passport_csrf_token, shorten_url

def get_session_id():
    try:
        token, ttwid, passport_csrf_token, shorten_url = get_qrcode_url()
        while True:
            qr_check = GET_h(f'https://web-va.tiktok.com/passport/web/check_qrconnect/?next=https%3A%2F%2Fwww.tiktok.com&token={token}&aid=1459', ttwid, passport_csrf_token)
            if "scanned" in qr_check.text:
                print("Waiting for your confirmation!")
            elif "confirmed" in qr_check.text:
                sessionid = qr_check.cookies.get('sessionid')
                break
            elif "expired" in qr_check.text:
                token, ttwid, passport_csrf_token, shorten_url = get_qrcode_url()
                print("URL has been updated!")
            time.sleep(0.7)

        if sessionid:
            print(f"Session ID: {sessionid}")
            print("\n\033[91mCoded By RXXV\033[0m")
        else:
            print("Failed to retrieve session ID.")
    except Exception as error:
        print(f"ERROR: {error}")

def gen(qr_data_url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data_url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    image = img.convert("RGB")
    width, height = image.size

    hex_digits = "0123456789abcdef"
    hex_code = "#" + "".join(random.choices(hex_digits, k=6))
    rgb_code = tuple(int(hex_code[i:i+2], 16) for i in (1, 3, 5))

    for x in range(width):
        for y in range(height):
            current_color = image.getpixel((x, y))
            if current_color == (0, 0, 0):
                image.putpixel((x, y), rgb_code)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("font.ttf", 15)
    position = (50, height - 30)
    draw.text(position, "t.me/@ryuna", font=font, fill=(0, 0, 0))

    image.show()

def main():
    get_session_id()

if __name__ == '__main__':
    main()
