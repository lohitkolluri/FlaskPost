# FlaskPost - Mass Mailer

FlaskPost is a web application designed for sending personalized emails to multiple recipients using predefined templates. This project utilizes Flask for the web application and Flask-Mail for email delivery.

## Features

- **Template Selection:** Choose from a variety of predefined email templates for different purposes.
- **Email Personalization:** Customize emails with recipient names, company details, etc., using merge fields.
- **Email Sending:** Send customized emails to multiple recipients at once.
- **CSV Data Import:** Easily import recipient data (email and name) from a CSV file.
- **SMTP Configuration:** Configure SMTP settings for email sending through environment variables or default values.

## Prerequisites

Before running the application, make sure you have the following:

- Python 3.x installed
- Required Python packages installed (see `requirements.txt`)
- Gmail account credentials (if using Gmail for SMTP)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/lohitkolluri/FlaskPost.git
    cd FlaskPost
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root directory and add the following:

    ```plaintext
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USERNAME=your_username@gmail.com
    MAIL_PASSWORD=your_password
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    ```

    Replace `your_username@gmail.com` and `your_password` with your Gmail credentials or appropriate SMTP configuration.

## Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Access the application in your web browser at [http://localhost:5000](http://localhost:5000).

3. Select an email template, customize the template content, and send emails to recipients.
