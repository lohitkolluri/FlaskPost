import os
import csv
import re
import logging
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles 
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
import io

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Initialize FastAPI
app = FastAPI()

# Serve static files from the assets directory
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Email regex pattern for validation
email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Global SMTP configuration variable
smtp_config = {}

# Helper function to validate email addresses
def is_valid_email(email: str) -> bool:
    return re.fullmatch(email_regex, email) is not None

# Route for the index page
@app.get("/", response_class=HTMLResponse)
async def index():
    with open('Frontend/index.html', 'r') as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Route to configure SMTP settings
@app.post("/configure_smtp")
async def configure_smtp(smtpHost: str = Form(...), smtpPort: int = Form(...),
                         smtpUser: str = Form(...), smtpPass: str = Form(...)):
    global smtp_config
    smtp_config = {
        'MAIL_SERVER': smtpHost,
        'MAIL_PORT': smtpPort,
        'MAIL_USERNAME': smtpUser,
        'MAIL_PASSWORD': smtpPass,
        'MAIL_STARTTLS': True,
        'MAIL_SSL_TLS': False,
        'USE_CREDENTIALS': True
    }

    logging.info(f"SMTP Config: {smtp_config}")

    return JSONResponse(content={'success': True, 'message': 'SMTP configuration updated successfully!'})

# Route to send emails
@app.post("/send_emails")
async def send_emails(subject: str = Form(...), senderName: str = Form(...),
                      htmlContent: str = Form(...), csvFile: UploadFile = File(...)):
    if not smtp_config:
        raise HTTPException(status_code=400, detail="SMTP configuration is missing")

    if csvFile.filename == '':
        raise HTTPException(status_code=400, detail="Empty CSV file uploaded")

    try:
        # Initialize FastMail with the current SMTP configuration
        conf = ConnectionConfig(
            MAIL_USERNAME=smtp_config['MAIL_USERNAME'],
            MAIL_PASSWORD=smtp_config['MAIL_PASSWORD'],
            MAIL_FROM=smtp_config['MAIL_USERNAME'],
            MAIL_PORT=smtp_config['MAIL_PORT'],
            MAIL_SERVER=smtp_config['MAIL_SERVER'],
            MAIL_STARTTLS=smtp_config['MAIL_STARTTLS'],
            MAIL_SSL_TLS=smtp_config['MAIL_SSL_TLS'],
            USE_CREDENTIALS=smtp_config['USE_CREDENTIALS'],
            MAIL_FROM_NAME=senderName,
        )
        mail = FastMail(conf)

        # Read the uploaded CSV file
        content = await csvFile.read()
        csv_input = csv.DictReader(io.StringIO(content.decode("UTF8")))

        invalid_emails = []
        success_emails = []

        for row in csv_input:
            recipient_email = row['Email'].strip()

            if not is_valid_email(recipient_email):
                invalid_emails.append(recipient_email)
                continue

            # Render HTML content with personalized data
            template = Template(htmlContent)
            personalized_html = template.render(row)

            # Prepare the email message
            message = MessageSchema(
                subject=subject,
                recipients=[recipient_email],
                body=personalized_html,
                subtype="html"
            )

            # Send the email
            await mail.send_message(message)
            success_emails.append(recipient_email)

        if invalid_emails:
            logging.warning(f"Invalid email addresses: {invalid_emails}")

        return JSONResponse(content={
            'success': True,
            'message': f'Emails sent to: {success_emails}. Invalid emails: {invalid_emails}'
        })

    except Exception as e:
        logging.error(f"Error sending emails: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Vercel-specific function handler (for deployment)
@app.get("/vercel")
async def vercel():
    return JSONResponse(content={"message": "FastAPI is running on Vercel!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
