# FlaskPost

FlaskPost is a web application designed for sending personalized emails to multiple recipients using an HTML editor. The application allows real-time previewing of emails and uses Flask-Mail for email delivery. Recipient details can be imported from a CSV file, and emails are sent using SMTP credentials provided in environment variables.

## 🧐 Features

Here are some of the features of this project:

- **Real-Time HTML Editor:** A built-in HTML editor allows users to create or paste email templates with real-time previews.
- **Email Personalization:** Customize email content using placeholders like `{{Name}}` to dynamically insert recipient-specific data.
- **Bulk Email Sending:** Send emails to multiple recipients by importing recipient details (like email and name) from a CSV file.
- **CSV Data Import:** Import recipient data from a CSV file (`input.csv`), ensuring the CSV contains at least 'Email' and 'Name' columns.
- **SMTP Configuration:** Use environment variables for SMTP configuration, allowing flexibility in choosing email providers like Gmail, Outlook, etc.
- **Real-Time Subject and Sender Preview:** Dynamically preview subject lines and sender names as you type them into the form fields.
- **Error Logging:** Logs email sending errors and outputs them to the terminal for debugging.

## 🛠️ Installation Steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/lohitkolluri/FlaskPost.git
   cd FlaskPost
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

Create a `.env` file in the root directory and add the following SMTP configuration:

    ```ini
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USERNAME=your_username@gmail.com
    MAIL_PASSWORD=your_password
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    ```

Replace `your_username@gmail.com` and `your_password` with your Gmail credentials or use your desired SMTP server settings.

5. Prepare a CSV file (`input.csv`) with at least the following two columns:

   - **Email**: The recipient's email address.
   - **Name**: The recipient's name.

   Example CSV file:

   ```csv
   Email,Name
   john@example.com,John Doe
   jane@example.com,Jane Smith
   ```

## ⚙️ Usage:

1. Run the application:

   ```bash
   python app.py
   ```

2. Open the application in your browser:

   ```bash
   http://localhost:3000
   ```

3. In the HTML editor, create or paste your email content. Use `{{Name}}` as a placeholder for recipient names. For example:

   ```html
   <p>Hello {{Name}},</p>
   <p>We are excited to invite you to our event!</p>
   ```

4. Fill in the "Email Subject" and "Sender Name" fields, and upload your recipient CSV file.

5. Click the "Send Emails" button to send personalized emails to all recipients listed in the CSV file.

## 🖥️ Real-Time Email Preview

As you type into the HTML editor, email subject, or sender name fields, the email preview will update automatically on the right side of the screen, showing you exactly what the email will look like.

## 🛡️ Error Handling

- If any required field is missing (HTML content, subject, sender name), the app will display an error.
- If the CSV file is missing or incorrectly formatted, an error will be logged.
- Failed email sends are logged in the terminal along with the recipient's email and the reason for the failure.

## 💻 Built with

Technologies used in the project:

- **Python** for the backend logic.
- **Flask** for building the web application.
- **Flask-Mail** for handling email sending.
- **dotenv** for managing environment variables.
- **HTML/CSS/JavaScript** for the frontend with real-time email preview functionality.

## 🛡️ License:

This project is licensed under the [MIT License](LICENSE).
