import os
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone
from dotenv import load_dotenv

# ── Load .env FIRST before anything else ──
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from helpers.alert_module import send_sms_alert, send_whatsapp_alert

app = Flask(__name__)


# ── CORS — allow browser fetch() from any origin ──
@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin']  = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/send-alert', methods=['OPTIONS'])
def preflight():
    return '', 204


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ping')
def ping():
    sid = os.getenv("TWILIO_ACCOUNT_SID", "NOT SET")
    return jsonify({
        "status": "ok",
        "message": "RakshaAI server is running",
        "twilio_sid_loaded": bool(sid and sid != "NOT SET"),
        "twilio_sid_prefix": sid[:6] + "…" if sid and len(sid) > 6 else sid
    })


@app.route('/send-alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json(force=True)

        alert_type = data.get('type', 'initial')
        contacts   = data.get('contacts', [])
        duration   = data.get('duration', 10)
        timestamp  = data.get('timestamp', datetime.now(timezone.utc).isoformat())
        maps_link  = data.get('maps_link', '')
        location   = data.get('location', 'Location unavailable')

        print(f"\n{'='*50}")
        print(f"[/send-alert] type={alert_type}  contacts={len(contacts)}")
        print(f"  location : {location}")
        print(f"  maps_link: {maps_link}")

        # ── Format readable timestamp ──
        try:
            ts_human = datetime.fromisoformat(
                timestamp.replace('Z', '+00:00')
            ).strftime('%d %b %Y %H:%M UTC')
        except Exception:
            ts_human = timestamp

        # ── Build message per alert type ──
        if alert_type == 'initial':
            message = (
                f"SOS ALERT — RakshaAI\n\n"
                f"Emergency signal triggered!\n"
                f"Time   : {ts_human}\n"
                f"Window : {duration} min\n"
            )
            if maps_link:
                message += f"📍 Live Location:\n{maps_link}\n"
            elif location and location != 'Location unavailable':
                message += f"📍 Coordinates: {location}\n"
            else:
                message += "📍 Location: Could not be captured\n"
            message += "\nPlease respond immediately or call 112."

        elif alert_type == 'cancel':
            message = (
                f"✅ SHE IS SAFE — RakshaAI\n\n"
                f"The SOS alert has been cancelled.\n"
                f"She is safe now. No action needed.\n"
                f"Time: {ts_human}"
            )

        elif alert_type == 'escalation':
            message = (
                f"⚠️ ESCALATION ALERT — RakshaAI\n\n"
                f"SOS was NOT cancelled in time!\n"
                f"Immediate attention required!\n"
                f"Time   : {ts_human}\n"
            )
            if maps_link:
                message += f"📍 Last Known Location:\n{maps_link}"
            elif location and location != 'Location unavailable':
                message += f"📍 Coordinates: {location}"

        else:
            message = f"RakshaAI Safety Alert — {ts_human}"

        print(f"\nMessage preview:\n{message[:120]}…\n")

        results = []

        for contact in contacts:
            name  = contact.get('name', 'Contact')
            phone = str(contact.get('phone', '')).strip()

            # ── Normalise phone number ──
            phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if phone and not phone.startswith('+'):
                phone = '+91' + phone        # default to India

            if not phone or len(phone) < 10:
                print(f"❌ Invalid phone for {name}: '{phone}'")
                results.append({"name": name, "phone": phone, "sms": "failed", "whatsapp": "failed"})
                continue

            print(f"\n📤 Sending to {name} ({phone})")

            sms_status = send_sms_alert(phone, message)
            wa_status  = send_whatsapp_alert(phone, message)

            print(f"   SMS={sms_status}  WA={wa_status}")

            results.append({
                "name": name,
                "phone": phone,
                "sms": sms_status,
                "whatsapp": wa_status
            })

        return jsonify({"status": "success", "type": alert_type, "results": results})

    except Exception as e:
        print(f"\n[ERROR in /send-alert] {e}")
        import traceback; traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🌸 RakshaAI Server Starting")
    print(f"   TWILIO_ACCOUNT_SID : {os.getenv('TWILIO_ACCOUNT_SID', 'NOT LOADED')[:8]}…")
    print(f"   TWILIO_SMS_FROM    : {os.getenv('TWILIO_SMS_FROM', 'NOT LOADED')}")
    print(f"   TWILIO_WA_FROM     : {os.getenv('TWILIO_WA_FROM', 'NOT LOADED')}")
    print("="*50 + "\n")
    app.run(debug=True, port=5000, use_reloader=False)