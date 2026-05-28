# AlertMe — Setup & Troubleshooting

## Quick Start

```bash
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000
```

---

## ✅ Twilio Fix Checklist

### 1. Fill in your real `.env` credentials

Open `.env` and paste the **full** values from https://console.twilio.com/

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx   ← 34 chars, starts with AC
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx      ← 32 chars
TWILIO_SMS_FROM=+19784045160                            ← your Twilio number
TWILIO_WA_FROM=whatsapp:+14155238886                    ← sandbox number
```

> ⚠️ The credentials in the screenshot look truncated. Verify the full values.

### 2. Verify SMS works

```bash
python test_alert.py +91YOURMOBILENUMBER
```

### 3. WhatsApp Sandbox — one-time setup per recipient

Each person who should receive WhatsApp messages must **first send a message** to the sandbox:

1. Open WhatsApp on their phone
2. Message `+1 415 523 8886`
3. Send the text: `join <your-sandbox-keyword>`
   (Find the keyword at: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)

After they join, they'll receive WhatsApp messages from the sandbox.

### 4. Trial account limitations

On a Twilio **trial account**, SMS can only be sent to **verified phone numbers**.

To verify a number:
→ Twilio Console → Phone Numbers → Verified Caller IDs → Add number

---

## Login / Signup

The app includes a local login/signup system backed by `localStorage`.
Credentials are stored in the browser only (no server needed for auth).

To add a real database backend later, add `/register` and `/login` POST routes
to `app.py` using SQLite + `flask-bcrypt`.

---

## File Structure

```
WOMEN SAFETY.AI/
├── app.py                  ← Flask server (fixed)
├── .env                    ← Your Twilio keys (never commit)
├── .env.example            ← Template
├── requirements.txt
├── test_alert.py           ← Run this to test Twilio
├── helpers/
│   ├── alert_module.py     ← SMS + WhatsApp sender (fixed)
│   ├── location_module.py
│   └── voice_module.py
└── templates/
    └── index.html          ← Full UI with login + sage green theme
```