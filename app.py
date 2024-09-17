import os
import csv
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import logging

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

# SMTP Configuration using environment variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT', '587')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'

mail = Mail(app)

# Set up logging to output to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Get a list of available templates
def get_template_files():
    template_files = [file for file in os.listdir('templates') if file.endswith('_template.html')]
    return template_files

# Fetch recipient data from CSV
def fetch_recipient_data():
    data = []
    try:
        with open('input.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if 'Email' in row and 'Name' in row:  # Check if the CSV contains the required columns
                    recipient_data = {
                        'email': row['Email'],
                        'name': row['Name']
                    }
                    data.append(recipient_data)
    except FileNotFoundError:
        print('CSV file not found.')
    except Exception as e:
        print(f'Error reading CSV file: {e}')
    return data

# Home page route to display templates
@app.route('/')
def index():
    templates = get_template_files()
    return render_template('index.html', templates=templates)

# Route to send emails
@app.route('/send_emails', methods=['POST'])
def send_emails():
    html_content = request.form.get('htmlContent')
    subject = request.form.get('subject')
    sender_name = request.form.get('senderName')

    # Check if required fields are present
    if not html_content or not subject or not sender_name:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400

    recipient_data = fetch_recipient_data()
    if not recipient_data:
        return jsonify({'success': False, 'error': 'No recipient data found'}), 400

    sent_emails = []
    failed_emails = []

    try:
        with app.app_context():  # Wrap the entire sending process in app context
            for data in recipient_data:
                recipient_email = data['email']
                recipient_name = data['name']

                # Substitute variables in the HTML content
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

if __name__ == '__main__':
    app.run(debug=False)
