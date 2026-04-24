

import os

# ── Load .env if available ─────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER", "")


def send_sms_alert(to_number: str, message: str) -> str:
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
        print(f"[alert_module] Twilio not configured. Would have sent to {to_number}:\n{message}")
        return "skipped"

    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        if not to_number.startswith("+"):
            to_number = "+" + to_number.replace(" ", "").replace("-", "")

        msg = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to_number
        )
        print(f"[alert_module] SMS sent to {to_number} → SID: {msg.sid}")
        return "sent"

    except Exception as e:
        print(f"[alert_module] Failed to send SMS to {to_number}: {e}")
        return "failed"


def send_whatsapp_alert(to_number: str, message: str) -> str:
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
        print(f"[alert_module] Twilio not configured for WhatsApp.")
        return "skipped"

    try:
        from twilio.rest import Client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        wa_from = "whatsapp:+14155238886"
        wa_to   = f"whatsapp:+{to_number.lstrip('+')}"

        msg = client.messages.create(body=message, from_=wa_from, to=wa_to)
        print(f"[alert_module] WhatsApp sent to {to_number} → SID: {msg.sid}")
        return "sent"

    except Exception as e:
        print(f"[alert_module] WhatsApp failed for {to_number}: {e}")
        return "failed"