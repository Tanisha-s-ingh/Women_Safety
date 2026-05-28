import os
from twilio.rest import Client
from dotenv import load_dotenv

# ── Load .env explicitly so it works when imported as a module ──
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def get_client():
    sid   = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()

    if not sid or not token:
        raise ValueError("❌ TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN is missing from .env")

    return Client(sid, token)


def send_sms_alert(to, message):
    try:
        client    = get_client()
        from_num  = os.getenv("TWILIO_SMS_FROM", "").strip()

        if not from_num:
            print("❌ TWILIO_SMS_FROM is not set in .env")
            return "failed"

        print(f"📤 SMS  → TO: {to}  FROM: {from_num}")

        msg = client.messages.create(
            body=message,
            from_='whatsapp:+14155238886',
            to=f'whatsapp:{+919382868507}'
        )

        print(f"✅ SMS sent! SID: {msg.sid}  Status: {msg.status}")
        return "sent"

    except Exception as e:
        print(f"❌ SMS Error: {e}")
        return "failed"


def send_whatsapp_alert(to, message):
    """
    Twilio WhatsApp Sandbox: recipient must first send
    'join <sandbox-keyword>' to whatsapp:+14155238886
    before they can receive messages.
    """
    try:
        client  = get_client()
        wa_from = os.getenv("TWILIO_WA_FROM", "").strip()

        if not wa_from:
            print("❌ TWILIO_WA_FROM is not set in .env")
            return "failed"

        # Ensure 'whatsapp:' prefix on destination
        wa_to = to if to.startswith("whatsapp:") else f"whatsapp:{to}"

        print(f"📲 WA   → TO: {wa_to}  FROM: {wa_from}")

        msg = client.messages.create(
            body=message,
            from_='+19784045160',
            to='+919382868507'
        )

        print(f"✅ WhatsApp sent! SID: {msg.sid}  Status: {msg.status}")
        return "sent"

    except Exception as e:
        print(f"❌ WhatsApp Error: {e}")
        return "failed"