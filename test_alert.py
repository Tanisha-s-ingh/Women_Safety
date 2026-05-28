"""
test_alert.py — Run this FIRST to verify your Twilio setup before launching the app.

Usage:
    python test_alert.py +91XXXXXXXXXX

Replace +91XXXXXXXXXX with your own phone number.
"""
import sys
import os
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

print("\n" + "="*55)
print("  RakshaAI — Twilio Diagnostic Test")
print("="*55)

sid   = os.getenv("TWILIO_ACCOUNT_SID", "")
token = os.getenv("TWILIO_AUTH_TOKEN", "")
sms_f = os.getenv("TWILIO_SMS_FROM", "")
wa_f  = os.getenv("TWILIO_WA_FROM", "")

print(f"\n📋 .env values loaded:")
print(f"   TWILIO_ACCOUNT_SID : {'✅ ' + sid[:6] + '…' if sid else '❌ NOT SET'}")
print(f"   TWILIO_AUTH_TOKEN  : {'✅ set (' + str(len(token)) + ' chars)' if token else '❌ NOT SET'}")
print(f"   TWILIO_SMS_FROM    : {sms_f or '❌ NOT SET'}")
print(f"   TWILIO_WA_FROM     : {wa_f or '❌ NOT SET'}")

if not sid or not token:
    print("\n❌ STOP: TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN is missing from your .env file.")
    print("   Open .env and paste your real credentials from https://console.twilio.com/")
    sys.exit(1)

if len(sid) != 34 or not sid.startswith("AC"):
    print(f"\n⚠️  WARNING: TWILIO_ACCOUNT_SID looks wrong.")
    print(f"   Expected 34 chars starting with 'AC', got: '{sid[:10]}…' ({len(sid)} chars)")
    print(f"   Double-check your .env file.")

if len(token) < 20:
    print(f"\n⚠️  WARNING: TWILIO_AUTH_TOKEN looks too short ({len(token)} chars).")
    print(f"   Real tokens are 32 characters. Check your .env.")

to_number = sys.argv[1] if len(sys.argv) > 1 else None
if not to_number:
    print("\n💡 Tip: Pass your phone number to send a real test:")
    print("   python test_alert.py +919876543210")
    print("\n   (Skipping live send — credentials look OK structurally)")
    sys.exit(0)

print(f"\n📤 Sending test SMS to {to_number}…")
from helpers.alert_module import send_sms_alert, send_whatsapp_alert

sms_result = send_sms_alert(to_number, "✅ RakshaAI test SMS — if you received this, SMS is working!")
print(f"   SMS result: {sms_result}")

print(f"\n📲 Sending test WhatsApp to {to_number}…")
print("   ⚠️  WhatsApp sandbox: recipient must first send 'join <keyword>'")
print("       to whatsapp:+14155238886 before they can receive messages.")
wa_result = send_whatsapp_alert(to_number, "✅ RakshaAI test WhatsApp — if you received this, WA is working!")
print(f"   WhatsApp result: {wa_result}")

print("\n" + "="*55)
if sms_result == "sent":
    print("✅ SMS is working correctly!")
else:
    print("❌ SMS failed. Check the error above — likely wrong SID/token or unverified number.")

if wa_result == "sent":
    print("✅ WhatsApp is working correctly!")
else:
    print("⚠️  WhatsApp failed. Did the recipient join the sandbox first?")
    print("   → Have them WhatsApp 'join <your-sandbox-keyword>' to +14155238886")
print("="*55 + "\n")