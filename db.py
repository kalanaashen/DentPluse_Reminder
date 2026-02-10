import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_customers_for_reminder():
    sql_query="""SELECT 
    u.email,
    u.user_name,
    a.appointment_date,
    a.start_time,
    a.treatment_type 
FROM `user` u
INNER JOIN appointment a ON u.user_id = a.patient_id;"""
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(sql_query)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result
    
                  