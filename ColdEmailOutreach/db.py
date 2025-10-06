import mysql.connector
from mysql.connector import Error

# Database connection helper
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",              # or your user1
        password="123",  # change to your actual password
        database="cold_email_outreach"
    )

# Fetch high-level stats for dashboard
def get_stats():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # total emails sent
    cursor.execute("SELECT COUNT(*) AS total_sent FROM emails_sent WHERE deleted=0")
    total_sent = cursor.fetchone()["total_sent"]

    # open rate
    cursor.execute("SELECT COUNT(*) AS opened FROM emails_sent WHERE opened=1 AND deleted=0")
    opened = cursor.fetchone()["opened"]

    open_rate = round((opened / total_sent) * 100, 2) if total_sent > 0 else 0

    # reply rate
    cursor.execute("SELECT COUNT(*) AS replied FROM emails_sent WHERE replied=1 AND deleted=0")
    replied = cursor.fetchone()["replied"]

    reply_rate = round((replied / total_sent) * 100, 2) if total_sent > 0 else 0

    conn.close()

    return {
        "emails_sent": total_sent,
        "open_rate": open_rate,
        "reply_rate": reply_rate
    }

# Get count of leads by status (for Chart.js pie chart)
def get_leads():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    statuses = {}
    for status in ["new", "sent", "opened", "replied"]:
        cursor.execute("SELECT COUNT(*) AS cnt FROM leads WHERE status=%s AND deleted=0", (status,))
        statuses[status] = cursor.fetchone()["cnt"]

    conn.close()
    return statuses

# Log a new email sent into DB
def log_email(lead_id, subject, body, opened=False, replied=False):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO emails_sent (lead_id, subject, body, opened, replied, deleted)
        VALUES (%s, %s, %s, %s, %s, 0)
    """, (lead_id, subject, body, int(opened), int(replied)))

    conn.commit()
    conn.close()
