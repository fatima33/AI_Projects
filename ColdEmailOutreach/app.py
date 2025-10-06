from flask import Flask, render_template, request
from db import get_stats, get_leads, log_email
from email_service import send_email
from ai_personalizer import generate_email

app = Flask(__name__)

@app.route("/")
def dashboard():

    '''
    # Example hardcoded data (replace with DB queries later)

    data = {
        "emails_sent": 120,
        "open_rate": 45,
        "reply_rate": 12,
        "leads_status": {
            "new": 50,
            "sent": 40,
            "opened": 20,
            "replied": 10
        }
    }
    return render_template("dashboard.html", **data)
    '''
    stats = get_stats()
    leads_status = get_leads()   # fetch dictionary of lead counts
    return render_template("dashboard.html", **stats, leads_status=leads_status)

@app.route("/send/<int:lead_id>", methods=["POST"])
def send_to_lead(lead_id):
    lead = get_leads(lead_id)
    body = generate_email(lead["company_name"], lead["contact_name"])
    email_id = send_email(lead["email"], "Quick Collaboration?", body)
    log_email(lead_id, email_id, body)
    return f"Sent to {lead['email']}"

if __name__ == "__main__":
    app.run(debug=True)

