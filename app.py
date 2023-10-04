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
    template_files = []
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('_template.html'):
                template_files.append(file)
    return template_files

@app.route('/')
def index():
    templates = get_template_files()
    return render_template('index.html', templates=templates)

def fetch_recipient_names():
    csv_file_path = os.path.join(os.getcwd(), 'input.csv')
    names = []

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            names.append(row['Name'])

    return names

@app.route('/send_emails', methods=['POST'])
def send_emails():
    # Get selected template
    selected_template = request.form['template']
    template_path = os.path.join('templates', selected_template)

    # Load email content from the selected template
    with open(template_path, 'r') as file:
        email_content = file.read()

    # Fetch recipient names from the CSV file
    recipient_names = fetch_recipient_names()

    for recipient_name in recipient_names:
        updated_email_content = email_content.replace('{{ name }}', recipient_name)

        # Rest of the code to send emails, using updated_email_content
        with app.app_context():
            mail.init_app(app)
            mail.username = app.config['MAIL_USERNAME']
            mail.password = app.config['MAIL_PASSWORD']
            mail.server = (app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
            mail.use_tls = app.config['MAIL_USE_TLS']
            mail.use_ssl = app.config['MAIL_USE_SSL']

            # Modify the subject as needed
            subject = 'Your Subject'

            # Modify the recipient email as needed
            recipient_email = 'recipient@example.com'

            msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient_email])
            msg.html = updated_email_content

            mail.send(msg)

    return 'Emails sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
