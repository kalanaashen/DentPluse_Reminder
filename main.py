from db import get_connection, get_customers_for_reminder

conn = get_connection()
print("✅ Database connected")
conn.close()


result = get_customers_for_reminder()
for row in result:
    print(row)