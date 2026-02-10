import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_customers_for_reminder():
    sql_query="""SELECT 
    p.email,
    p.full_name,
    a.appointment_date,
    a.start_time,
    a.treatment_type
FROM appointment a
INNER JOIN patient p 
    ON a.patient_id = p.patient_id;
"""
    conn=get_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute(sql_query)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result
    
                  