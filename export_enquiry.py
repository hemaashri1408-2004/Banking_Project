import pymysql
import csv

connection = pymysql.connect(
    host="18.136.157.135",
    port=3306,
    user="dm_team1",
    password="DM!$Team&279@20!",
    database="project_banking"
)

cursor = connection.cursor()

print("Database connected. Export starting...")

cursor.execute("SELECT * FROM Cust_Enquiry")

columns = [column[0] for column in cursor.description]

with open(
    "Cust_Enquiry.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as csv_file:

    writer = csv.writer(csv_file)
    writer.writerow(columns)

    total = 0

    while True:
        rows = cursor.fetchmany(10000)

        if not rows:
            break

        writer.writerows(rows)
        total += len(rows)

        print(f"{total} rows exported...")

cursor.close()
connection.close()

print(f"\nExport completed successfully! Total rows: {total}")