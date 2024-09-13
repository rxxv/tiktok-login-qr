# Get TikTok Web Session Via QR Code Login

![QR Code Image](https://i.postimg.cc/wvv4J5mg/IMG-9017.jpg)

## Overview

Login into your TikTok account by generating a QR code that you can scan on the TikTok app with your phone. Once scanned and confirmed, it retrieves your session ID, giving you authenticated access to TikTok's web services.

## Key Features

- Generates a TikTok login QR code.
- Provides a shortened URL for easier mobile access.
- Tracks the status of the QR code scan (scanned, confirmed, expired).

## Installation

To get started, you'll need to install a few dependencies. You can do this by running:

```bash
pip install requests qrcode[pil] Pillow
```

## How to Use

1. Clone this repository:

```bash
git clone https://github.com/rxxv/tiktok-login-qr
```

2. Install the necessary dependencies:

```bash
pip install requests qrcode[pil] Pillow
```

3. Run the script with:

```bash
python qr.py
```

The script will generate a QR code, display a shortened URL for easy access, and retrieve the session ID once your login is confirmed.

## Notes

This script is for educational purposes and shows how to interact with TikTok's login system via QR codes. Please ensure your usage complies with TikTok's terms and policies.

---

Created by RXXV.
