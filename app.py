import os
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('GMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Load the email template
with open('templates/email_template.html', 'r') as file:
    EMAIL_TEMPLATE = file.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_emails', methods=['POST'])
def send_emails():
    # Read CSV file from the root directory
    csv_file_path = os.path.join(os.getcwd(), 'input.csv')
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            recipient_name = row['Name']
            recipient_email = row['Email']

            msg = Message('Your Subject', sender=app.config['MAIL_USERNAME'], recipients=[recipient_email])
            msg.html = EMAIL_TEMPLATE.replace('{{ name }}', recipient_name)

            # Send the email
            mail.send(msg)

    return 'Emails sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
