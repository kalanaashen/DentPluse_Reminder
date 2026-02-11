from db import get_customers_for_reminder,save_reminder_log
from email_service import send_email


def send_reminders():
    customers = get_customers_for_reminder()
    

    for email, name, date, time, treatment in customers:
        subject = "🦷 Appointment Reminder – DentPulse"
        body = f"""
Hello {name},

This is a reminder for your upcoming dental appointment.

📅 Date: {date}
⏰ Time: {time}
🦷 Treatment: {treatment}

Please arrive 10 minutes early.

Thank you,
DentPulse Dental Clinic
"""

        send_email(email, subject, body)
        save_reminder_log(
            email=email,
            reminder_type="EMAIL",
            appointment_date=date
        )
        print(f"✅ Reminder sent to {email}")


if __name__ == "__main__":
    send_reminders()
