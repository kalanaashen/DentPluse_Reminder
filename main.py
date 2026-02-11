from fastapi import FastAPI
from db import get_customers_for_reminder
from email_service import send_email
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
app = FastAPI()

    
scheduler = BackgroundScheduler()

def send_single_reminder(email, name, date, time, treatment):

   
        subject = "Appointment Reminder"
        body = f"""
Hello {name},

This is a reminder for your appointment.

Date: {date}
Time: {time}
Treatment: {treatment}

Thank you,
DentPulse
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