import os
import csv
import re
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import logging
import io
from jinja2 import Template

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

smtp_config = {}

email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

def is_valid_email(email):
    """ Validate email format using regex. """
    return re.fullmatch(email_regex, email) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure_smtp', methods=['POST'])
def configure_smtp():
    global smtp_config
    smtp_config = {
        'MAIL_SERVER': request.form.get('smtpHost'),
        'MAIL_PORT': int(request.form.get('smtpPort')),
        'MAIL_USERNAME': request.form.get('smtpUser'),
        'MAIL_PASSWORD': request.form.get('smtpPass'),
        'MAIL_USE_TLS': True, 
        'MAIL_USE_SSL': False  
    }
    
    logging.info(f"SMTP Config: {smtp_config}")
    app.config.update(smtp_config)
    
    return jsonify({'success': True, 'message': 'SMTP configuration updated successfully!'})

@app.route('/send_emails', methods=['POST'])
def send_emails():
    html_content = request.form['htmlContent']
    subject = request.form['subject']
    sender_name = request.form['senderName']
    
    if 'csvFile' not in request.files:
        return jsonify({'success': False, 'error': 'No CSV file uploaded'}), 400

    file = request.files['csvFile']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Empty CSV file uploaded'}), 400
    
    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)  
        
        mail = Mail(app)
        mail.init_app(app)

        invalid_emails = []
        success_emails = []

        with mail.connect() as conn:
            for row in csv_input:
                recipient_email = row['Email'].strip()

                if not is_valid_email(recipient_email):
                    invalid_emails.append(recipient_email)
                    continue 
                
                template = Template(html_content)
                personalized_html = template.render(row) 
                
                msg = Message(
                    subject=subject,
                    sender=(sender_name, smtp_config['MAIL_USERNAME']),
                    recipients=[recipient_email]
                )
                msg.html = personalized_html
                conn.send(msg)
                success_emails.append(recipient_email)

        if invalid_emails:
            logging.warning(f"Invalid email addresses: {invalid_emails}")
        
        return jsonify({'success': True, 'message': f'Emails sent to: {success_emails}. Invalid emails: {invalid_emails}'})
    
    except Exception as e:
        logging.error(f"Error sending emails: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Vercel specific function handler
if __name__ == "__main__":
    app.run()
