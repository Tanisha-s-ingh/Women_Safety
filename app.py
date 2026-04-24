from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone
from helpers.alert_module import send_sms_alert, send_whatsapp_alert

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send-alert', methods=['POST'])
def send_alert():
    try:
        data = request.get_json(force=True)

        alert_type = data.get('type', 'initial')
        contacts   = data.get('contacts', [])
        duration   = data.get('duration', 10)
        timestamp  = data.get('timestamp', datetime.now(timezone.utc).isoformat())
        location   = data.get('location')
        maps_link  = data.get('maps_link')

        ts_human = timestamp[:19].replace('T', ' ') + ' UTC'

        # ───────── MESSAGE BUILDER ─────────
        if alert_type == 'initial':
            message = (
                f"🚨 SOS ALERT\n\n"
                f"Emergency signal triggered.\n"
                f"🕐 Time: {ts_human}\n"
                f"⏱ Window: {duration} min\n"
                f"📍 Location: {maps_link if maps_link else 'Not available'}\n\n"
                f"Please respond immediately."
            )

        elif alert_type == 'cancel':
            message = (
                f"✅ I AM SAFE\n\n"
                f"The SOS alert has been cancelled.\n"
                f"User is safe now.\n"
                f"🕐 Time: {ts_human}"
            )

        elif alert_type == 'escalation':
            message = (
                f"🚨 ESCALATION ALERT\n\n"
                f"SOS NOT CANCELLED within time.\n"
                f"Immediate attention required!\n"
                f"🕐 Time: {ts_human}\n"
                f"📍 Location: {maps_link if maps_link else 'Unknown'}"
            )

        else:
            message = "RakshaAI Alert"

        # ───────── SEND ALERTS ─────────
        results = []

        for contact in contacts:
            name = contact.get('name', 'Contact')
            phone = contact.get('phone', '').strip()

            # 🔥 FIX: auto add country code if missing
            if phone and not phone.startswith('+'):
                phone = '+91' + phone

            if not phone:
                results.append({
                    "name": name,
                    "phone": phone,
                    "sms": "failed",
                    "whatsapp": "skipped"
                })
                continue

            sms_status = send_sms_alert(phone, message)
            wa_status  = send_whatsapp_alert(phone, message)

            results.append({
                "name": name,
                "phone": phone,
                "sms": sms_status,
                "whatsapp": wa_status
            })

        return jsonify({
            "status": "success",
            "type": alert_type,
            "sent_to": len(results),
            "results": results
        }), 200

    except Exception as e:
        print("[ERROR /send-alert]:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)