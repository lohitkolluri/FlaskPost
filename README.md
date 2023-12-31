<h1 align="center" id="title">FlaskPost</h1>

<p id="description">FlaskPost is a web application designed for sending personalized emails to multiple recipients using predefined templates. This project utilizes Flask for the web application and Flask-Mail for email delivery.</p>

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Template Selection: Choose from a variety of predefined email templates for different purposes.
*   Email Personalization: Customize emails with recipient names company details etc. using merge fields.
*   Email Sending: Send customized emails to multiple recipients at once.
*   CSV Data Import: Easily import recipient data (email and name) from a CSV file.
*   SMTP Configuration: Configure SMTP settings for email sending through environment variables or default values.

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the repository:</p>

```
git clone https://github.com/lohitkolluri/FlaskPost.git cd FlaskPost
```

<p>2. Create and activate a virtual environment:</p>

```
python -m venv venv source
venv/bin/activate   # On Windows use: venv\Scripts\activate
```

<p>3. Install dependencies:</p>

```
pip install -r requirements.txt
```

<p>4. Set up environment variables:</p>

Create a `.env` file in the root directory and add the following:

    
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=587
    MAIL_USERNAME=your_username@gmail.com
    MAIL_PASSWORD=your_password
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    
Replace ``` your_username@gmail.com ``` and `your_password` with your Gmail credentials or appropriate SMTP configuration.

<h2>⚙️ Usage:</h2>

<p>1. Run the application:</p>

```
python app.py
```

<p>2. Open localhost in your browser:</p>

  https://localhost:3000

<p>3. Select an email template customize the template content and send emails to recipients.</p>
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Python
*   Flask
*   Flask-Mail
*   Dotenv

<h2>🛡️ License:</h2>

This project is licensed under the [MIT License](LICENSE)
