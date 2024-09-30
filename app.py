import os
import csv
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import logging
import io

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

smtp_config = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configure_smtp', methods=['POST'])
def configure_smtp():
    global smtp_config
    smtp_config = {
        'MAIL_SERVER': request.form.get('smtpHost'),
        'MAIL_PORT': request.form.get('smtpPort'),
        'MAIL_USERNAME': request.form.get('smtpUser'),
        'MAIL_PASSWORD': request.form.get('smtpPass'),
        'MAIL_USE_TLS': request.form.get('smtpUseTLS', 'True').lower() == 'true',
        'MAIL_USE_SSL': request.form.get('smtpUseSSL', 'False').lower() == 'true'
    }
    
    app.config.update(smtp_config)

    return jsonify({'success': True, 'message': 'SMTP configuration updated successfully!'})

@app.route('/send_emails', methods=['POST'])
def send_emails():
    html_content = request.form.get('htmlContent')
    subject = request.form.get('subject')
    sender_name = request.form.get('senderName')
    csv_file = request.files.get('csvFile')

    # Check if required fields are present
    if not html_content or not subject or not sender_name or not csv_file:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    # Read CSV data
    recipient_data = fetch_recipient_data(csv_file)
    if not recipient_data:
        return jsonify({'success': False, 'error': 'No recipient data found'}), 400

    sent_emails = []
    failed_emails = []

    mail = Mail(app)  

    try:
        with app.app_context(): 
            for data in recipient_data:
                recipient_email = data['email']
                recipient_name = data['name']

                personalized_content = html_content.replace('{{ Name }}', recipient_name)

                msg = Message(subject, sender=(sender_name, app.config['MAIL_USERNAME']), recipients=[recipient_email])
                msg.html = personalized_content

                try:
                    mail.send(msg)
                    sent_emails.append(recipient_email)
                    logging.info(f"Email sent to {recipient_email}")
                except Exception as e:
                    failed_emails.append(recipient_email)
                    logging.error(f"Failed to send email to {recipient_email}: {str(e)}")

        return jsonify({
            'success': True,
            'message': 'Emails processed successfully!',
            'sent': sent_emails,
            'failed': failed_emails
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def fetch_recipient_data(csv_file):
    data = []
    try:
        csv_data = io.StringIO(csv_file.stream.read().decode('utf-8'))
        csv_reader = csv.DictReader(csv_data)
        for row in csv_reader:
            if 'Email' in row and 'Name' in row: 
                recipient_data = {
                    'email': row['Email'],
                    'name': row['Name']
                }
                data.append(recipient_data)
    except Exception as e:
        logging.error(f'Error reading CSV file: {e}')
    return data

if __name__ == '__main__':
    app.run(debug=False)
