from fastapi import FastAPI, Form, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template
import io
import csv
import re
import logging
import time
from datetime import datetime

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Initialize FastAPI
app = FastAPI()

# Serve static files from the assets directory
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Email regex pattern for validation
email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

# Global SMTP configuration variable
smtp_config = {}

# Rate limiting variables
email_send_interval = 1 
retry_attempts = 3 

# Helper function to validate email addresses
def is_valid_email(email: str) -> bool:
    return re.fullmatch(email_regex, email) is not None

# Helper function to validate CSV format
def validate_csv(file_content: str) -> bool:
    reader = csv.DictReader(io.StringIO(file_content))
    required_columns = {"Email"}
    return required_columns.issubset(reader.fieldnames)

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

# Route to preview CSV
@app.post("/preview_csv")
async def preview_csv(csvFile: UploadFile = File(...)):
    if csvFile.filename == '':
        raise HTTPException(status_code=400, detail="Empty CSV file uploaded")
    
    content = await csvFile.read()
    csv_data = csv.DictReader(io.StringIO(content.decode("UTF-8")))
    preview_data = [row for idx, row in enumerate(csv_data) if idx < 5]  # Preview first 5 rows
    return JSONResponse(content={'preview': preview_data})

# Route to send emails
@app.post("/send_emails")
async def send_emails(subject: str = Form(...), senderName: str = Form(...),
                      htmlContent: str = Form(...), csvFile: UploadFile = File(...),
                      attachment: UploadFile = File(None), schedule_time: str = Form(None),
                      background_tasks: BackgroundTasks = BackgroundTasks()):
    if not smtp_config:
        raise HTTPException(status_code=400, detail="SMTP configuration is missing")

    if csvFile.filename == '':
        raise HTTPException(status_code=400, detail="Empty CSV file uploaded")
    
    # Read and validate the uploaded CSV file
    content = await csvFile.read()
    if not validate_csv(content.decode("UTF-8")):
        raise HTTPException(status_code=400, detail="CSV validation failed: Missing required columns")

    # Schedule email sending if schedule_time is provided
    if schedule_time:
        try:
            scheduled_time = datetime.strptime(schedule_time, "%Y-%m-%d %H:%M:%S")
            delay = (scheduled_time - datetime.now()).total_seconds()
            if delay > 0:
                background_tasks.add_task(schedule_emails, delay, subject, senderName, htmlContent, content, attachment)
                return JSONResponse(content={'success': True, 'message': f'Emails scheduled for {schedule_time}'})
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid schedule time format. Use YYYY-MM-DD HH:MM:SS.")
    
    # Send emails immediately if no scheduling
    await schedule_emails(0, subject, senderName, htmlContent, content, attachment)
    return JSONResponse(content={'success': True, 'message': 'Emails sent successfully'})

async def schedule_emails(delay: float, subject: str, senderName: str, htmlContent: str, csv_content: bytes, attachment: UploadFile):
    time.sleep(delay)
    csv_input = csv.DictReader(io.StringIO(csv_content.decode("UTF-8")))
    invalid_emails = []
    success_emails = []

    # Read attachment if available
    attachment_data = None
    if attachment:
        attachment_data = await attachment.read()
        attachment = UploadFile(filename=attachment.filename, file=io.BytesIO(attachment_data))

    for row in csv_input:
        recipient_email = row['Email'].strip()

        if not is_valid_email(recipient_email):
            invalid_emails.append(recipient_email)
            continue

        # Render HTML content and subject
        template = Template(htmlContent)
        personalized_html = template.render(row)
        subject_template = Template(subject)
        personalized_subject = subject_template.render(row)

        # Prepare the email message
        message = MessageSchema(
            subject=personalized_subject,
            recipients=[recipient_email],
            body=personalized_html,
            subtype="html",
            attachments=[attachment] if attachment else None
        )

        for attempt in range(retry_attempts):
            try:
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
                    VALIDATE_CERTS=False
                )
                mail = FastMail(conf)

                # Send the email
                await mail.send_message(message)
                success_emails.append(recipient_email)
                logging.info(f"Email successfully sent to: {recipient_email}")

                # Wait for the specified interval before sending the next email
                time.sleep(email_send_interval)
                break
            except Exception as e:
                logging.error(f"Attempt {attempt + 1}/{retry_attempts} - Failed to send email to {recipient_email}: {e}")
                if attempt < retry_attempts - 1:
                    time.sleep(email_send_interval) 
                else:
                    logging.error(f"All attempts failed for {recipient_email}")

    if invalid_emails:
        logging.warning(f"Invalid email addresses: {invalid_emails}")

    logging.info("=" * 40)
    logging.info(f"Email send operation complete. Successful: {len(success_emails)}, Failed: {len(invalid_emails)}")
    logging.info("=" * 40)

# Vercel-specific function handler
@app.get("/vercel")
async def vercel():
    return JSONResponse(content={"message": "FastAPI is running on Vercel!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
