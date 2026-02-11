from fastapi import FastAPI
from db import get_customers_for_reminder
from email_service import send_email
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
app = FastAPI()

    
scheduler = BackgroundScheduler()

def send_single_reminder(email, name, date, time, treatment):

   
        subject = "Appointment Reminder"
        body = body = f"""
<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; font-family: Arial, sans-serif; background-color:#f0fdf4;">

  <div style="max-width:600px; margin:auto; background:white; border-radius:10px; overflow:hidden; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
    
    <!-- Header -->
    <div style="background:#16a34a; padding:20px; text-align:center; color:white;">
      <h2 style="margin:0;">DentPulse Dental Clinic</h2>
      <p style="margin:5px 0 0;">Appointment Reminder</p>
    </div>

    <!-- Content -->
    <div style="padding:25px; color:#374151;">
      
      <p style="font-size:16px;">Hello <strong>{name}</strong>,</p>

      <p>This is a friendly reminder for your upcoming appointment.</p>

      <div style="background:#f0fdf4; padding:15px; border-radius:8px; margin:20px 0;">
        <p><strong>Date:</strong> {date}</p>
        <p><strong>Time:</strong> {time}</p>
        <p><strong>Treatment:</strong> {treatment}</p>
      </div>

      <p style="margin-top:20px;">
        Please arrive 10 minutes early.
      </p>

      <div style="margin-top:30px; text-align:center;">
        <a href="http://yourwebsite.com"
           style="background:#16a34a; color:white; padding:12px 25px; text-decoration:none; border-radius:6px;">
           View Appointment
        </a>
      </div>

    </div>

    <!-- Footer -->
    <div style="background:#f9fafb; padding:15px; text-align:center; font-size:12px; color:#6b7280;">
      © 2025 DentPulse Dental Clinic <br>
      Thank you for trusting us with your smile 🦷
    </div>

  </div>

</body>
</html>
"""


        send_email(email, subject, body)
        #save_reminder_log(email)
        print("reminder procesed for:", email)
   

def schedule_reminders():
    customers = get_customers_for_reminder()

    for email, name, date, time, treatment in customers:

        
        appointment_datetime = datetime.combine(date, time)

       
        reminder_time = appointment_datetime - timedelta(days=1)

      
        if reminder_time > datetime.now():
            scheduler.add_job(
                send_single_reminder,
                trigger="date",
                run_date=reminder_time,
                args=[email, name, date, time, treatment]
            )
            print(f"Reminder scheduled for {email} at {reminder_time}")


@app.post("/send-reminders")
def send_reminders():
    schedule_reminders()
    return {"status": "success", "message": "Reminders sent"}
 
 
@app.on_event("startup")
def start_scheduler():
    
    scheduler.start()
    schedule_reminders()
    print("Scheduler started at application startup")