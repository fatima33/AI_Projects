import pandas as pd
import random
import datetime
import mysql.connector

# Load Kaggle dataset (download leads.csv manually first)
df = pd.read_csv("leads.csv", encoding="latin1")

# Connect to your MySQL DB
conn = mysql.connector.connect(
	host="localhost",
	user="root",  # or your user
	password="123",  # replace with your actual root/user password
	database="cold_email_outreach"
)
cursor = conn.cursor()

# Map dataset columns -> your schema
for idx, row in df.iterrows():
	company_name = str(row.get("Company", "Unknown Company"))[:255]
	contact_name = str(row.get("Name", f"Contact {idx}"))[:255]

	# If dataset has no email, generate fake one
	email = str(row.get("Email", f"user{idx}@example.com"))[:255]

	industry = str(row.get("Industry", "General"))[:150]

	# Randomly assign a status for demo
	status = random.choice(["new", "sent", "opened", "replied"])

	# Last contacted = random within last 60 days
	last_contacted = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 60))

	deleted = 0

	cursor.execute("""
		INSERT INTO leads (company_name, contact_name, email, industry, status, last_contacted, deleted)
		VALUES (%s, %s, %s, %s, %s, %s, %s)
	""", (company_name, contact_name, email, industry, status, last_contacted, deleted))

conn.commit()
conn.close()

print("Leads table populated successfully!")
