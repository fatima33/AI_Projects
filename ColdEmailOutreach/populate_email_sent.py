# -*- coding: utf-8 -*-
import random
import datetime
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",  # change to your real password
    database="cold_email_outreach"
)
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT id FROM leads WHERE deleted=0")
leads = cursor.fetchall()

for lead in leads:
    lead_id = lead["id"]

    status = "new"

    # Simulate 1–3 emails per lead
    for _ in range(random.randint(1, 3)):
        subject = random.choice([
            "Boost your sales with our tool",
            "Quick question about your business",
            "Unlock growth opportunities",
            "Collaboration proposal"
        ])
        body = f"Hello! This is a demo email sent to lead {lead_id}."
        sent_at = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))

        opened = random.choice([0, 1])
        replied = 1 if opened and random.random() > 0.5 else 0

        if replied:
            status = "replied"
        elif opened:
            status = "opened"
        else:
            status = "sent"

        cursor.execute("""
            INSERT INTO emails_sent (lead_id, subject, body, sent_at, opened, replied, deleted)
            VALUES (%s, %s, %s, %s, %s, %s, 0)
        """, (lead_id, subject, body, sent_at, opened, replied))

    # Update lead status based on last simulated email
    cursor.execute("UPDATE leads SET status=%s WHERE id=%s", (status, lead_id))

conn.commit()
conn.close()

print("Emails_sent + Leads table synced successfully!")
