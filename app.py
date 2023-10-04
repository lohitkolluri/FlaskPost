import os
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env file

# SMTP Configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your_username@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your_password')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'

mail = Mail(app)

# Get a list of available templates
def get_template_files():
    template_files = [file for file in os.listdir('templates') if file.endswith('_template.html')]
    return template_files

def fetch_recipient_data():
    data = []
    with open('input.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if 'Email' in row and 'Name' in row:  # Check if the CSV contains the required columns
                recipient_data = {
                    'email': row['Email'],
                    'name': row['Name']
                }
                data.append(recipient_data)
    return data

@app.route('/')
def index():
    templates = get_template_files()
    return render_template('index.html', templates=templates)

@app.route('/send_emails', methods=['POST'])
def send_emails():
    # Ensure 'template' is present in the form data
    if 'template' not in request.form:
        return 'Bad request. Form data is missing.'

    # Get selected template
    selected_template = request.form['template']
    template_path = os.path.join('templates', selected_template)

    # Load email content from the selected template
    with open(template_path, 'r') as file:
        template_content = file.read().split('\n', 1)

    # Extract subject and body from the template
    subject = template_content[0]
    body = template_content[1] if len(template_content) > 1 else ''

    # Fetch recipient emails and names from the CSV file
    recipient_data = fetch_recipient_data()
    
    for data in recipient_data:
        recipient_email = data['email']
        recipient_name = data['name']
        
        # Substitute variables in the body
        updated_body = body.replace('{{ name }}', recipient_name)

        # Rest of the code to send emails, using updated_body and subject
        with app.app_context():
            mail.init_app(app)
            mail.username = app.config['MAIL_USERNAME']
            mail.password = app.config['MAIL_PASSWORD']
            mail.server = (app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
            mail.use_tls = app.config['MAIL_USE_TLS']
            mail.use_ssl = app.config['MAIL_USE_SSL']

            msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient_email])
            msg.html = updated_body

            mail.send(msg)

    return 'Emails sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
