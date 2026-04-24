from helpers.alert_module import send_sms_alert ,send_whatsapp_alert
print("Sending SMS...")

status = send_sms_alert(
    "+919382868507",   # 👉 put your real number
    "🚨 IT IS AN EMERGENCY!!!"
)
status1 = send_whatsapp_alert(
    "+919382868507",   # your number
    "🚨 WhatsApp test from RakshAI"
)
print("Status:", status)
print("Status",status1)