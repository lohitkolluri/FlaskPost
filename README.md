<div align="center">

![Banner](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=FlaskPost&fontSize=80&animation=fadeIn&fontAlignY=35)

[![Built with FastAPI](https://img.shields.io/badge/Built%20with-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Email with FastMail](https://img.shields.io/badge/Email%20with-FastMail-4A154B?style=for-the-badge&logo=minutemailer)](https://fastmail.com)
[![Database](https://img.shields.io/badge/Template%20Engine-Jinja2-B41717?style=for-the-badge&logo=jinja)](https://jinja.palletsprojects.com/)

> 📧 Transform your email campaigns with powerful mass mailing capabilities!

<p align="center">
  <a href="#features">Features</a> •
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#installation">Installation</a> •
  <a href="#deployment">Deployment</a> •
  <a href="#usage">Usage</a>
</p>

<p align="center">
<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Envelope.png" alt="Email" width="25" height="25" /> Streamlined mass mailing
<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Page%20with%20Curl.png" alt="Template" width="25" height="25" /> Rich HTML templates
<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Bar%20Chart.png" alt="Analytics" width="25" height="25" /> Delivery analytics
</p>

</div>

## ✨ Features

<details>
<summary>📧 Email Management</summary>

- **Advanced HTML Editor**
  - Rich text formatting
  - Template customization
  - Dynamic content insertion
  - Real-time preview
- **Recipient Management**
  - CSV file upload support
  - Contact list organization
  - Dynamic field mapping
  - Duplicate detection
- **Campaign Tools**
  - Scheduled sending
  - Batch processing
  - Personalization tokens
  - Template variables

</details>

<details>
<summary>🔧 System Features</summary>

- **SMTP Configuration**
  - Multiple provider support
  - Secure connection handling
  - Custom port configuration
  - Authentication management
- **Error Handling**
  - Comprehensive logging
  - Retry mechanisms
  - Failure notifications
  - Invalid email detection
- **Performance**
  - Asynchronous processing
  - Rate limiting
  - Queue management
  - Resource optimization

</details>

<details>
<summary>📊 Analytics & Reporting</summary>

- **Delivery Tracking**
  - Success/failure rates
  - Bounce tracking
  - Delivery timestamps
  - Error categorization
- **Campaign Insights**
  - Batch statistics
  - Processing times
  - Queue status
  - System performance

</details>

## 🚀 Getting Started

```mermaid
graph LR
    A[Upload CSV] --> B[Configure SMTP]
    B --> C[Create Template]
    C --> D[Preview Email]
    D --> E[Send Campaign]
    E --> F[Track Results]
```

### 📋 Prerequisites

<table align="center">
  <tr>
    <td align="center" width="96">
      <img src="https://skillicons.dev/icons?i=python" width="48" height="48" alt="Python" />
      <br>Python 3.8+
    </td>
    <td align="center" width="96">
      <img src="https://skillicons.dev/icons?i=fastapi" width="48" height="48" alt="FastAPI" />
      <br>FastAPI
    </td>
    <td align="center" width="96">
      <img src="https://www.vectorlogo.zone/logos/pocoo_jinja/pocoo_jinja-icon.svg" width="48" height="48" alt="Jinja2" />
      <br>Jinja2
    </td>
  </tr>
</table>

### 🛠️ Installation

1️⃣ **Clone the Repository**
```bash
git clone https://github.com/lohitkolluri/FlaskPost.git
cd FlaskPost
```

2️⃣ **Set Up Environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

4️⃣ **Launch the Application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 💻 Usage

### 📤 Sending Emails

1. Access the web interface at `http://localhost:5000`
2. Configure your SMTP settings in the web UI:
   - SMTP Host (e.g., smtp.gmail.com)
   - SMTP Port (e.g., 587 for TLS)
   - Username and Password
   - TLS/SSL preferences
3. Upload your CSV file with recipient data
4. Create or select an HTML email template
5. Preview your email
6. Send your campaign

Your SMTP settings are securely stored for the session and can be easily modified through the interface.

### 📝 Template Variables

```html
Dear {{recipient_name}},

Your custom message here.

Best regards,
{{sender_name}}
```

### 🔍 CSV Format

```csv
email,name,custom_field
john@example.com,John Doe,Value1
jane@example.com,Jane Smith,Value2
```

## 🛡️ Security Features

- **Email Validation**
  - Syntax checking
  - Domain verification
  - Bounce detection
- **Data Protection**
  - Secure SMTP
  - Environment variables
  - Data encryption
- **Error Prevention**
  - Rate limiting
  - Duplicate detection
  - Format validation

## 📊 System Architecture

```mermaid
flowchart TD
    A[User Interface] --> B[FastAPI Backend]
    B --> C{Processing}
    C --> D[Template Engine]
    C --> E[Email Queue]
    C --> F[CSV Parser]
    E --> G[FastMail]
    G --> H[SMTP Server]
```

## 🔧 Configuration

<details>
<summary>Web UI Configuration</summary>

The application provides a user-friendly interface for configuring:

- **SMTP Settings**
  - Server host and port
  - Authentication credentials
  - Security options (TLS/SSL)
  - Connection testing
- **Email Options**
  - Sender name and email
  - Reply-to address
  - Custom headers
  - Rate limiting
- **Template Settings**
  - HTML editor configuration
  - Preview options
  - Variable mapping
</details>

## 📄 License

<div align="center">

MIT License © [Lohit Kolluri](LICENSE) - feel free to use this project as you wish!

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%"/>

</div>
