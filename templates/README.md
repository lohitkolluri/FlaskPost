# Email Templates Documentation

This documentation provides a comprehensive overview of email templates available for use with the FlaskPost Mass Mailer application. The application allows users to select from different email templates while sending mass emails.

## Table of Contents

1. [Overview](#overview)
2. [Available Email Templates](#available-email-templates)
    - [Rich Text Formatting Template](#1-rich-text-formatting-template-rich_text_templatehtml)
    - [Table Formatting Template](#2-table-formatting-template-table_templatehtml)
    - [Styled Template](#3-styled-template-styled_templatehtml)
3. [How to Use Email Templates](#how-to-use-email-templates)

## Overview

Email templates are pre-designed layouts that define the structure and styling of an email. In the context of the FlaskPost Mass Mailer application, these templates serve as a starting point for creating email content for mass emails. Users can choose from a variety of templates to suit their specific communication needs.

## Available Email Templates

### 1. Rich Text Formatting Template (`_rich_text_template.html`)

This template showcases various rich text formatting options, including:

- **Bold**: `<strong>`
- **Italics**: `<em>`
- **Underline**: `<u>`
- **Bulleted and numbered lists**: `<ul>` and `<ol>`
- **Links**: `<a>`
- **Images**: `<img>`

Example Usage:
```html
<p>This is <strong>bold text</strong> and this is <em>italicized text</em>. You can also <u>underline</u> text.</p>
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
</ul>
```

### 2. Table Formatting Template (`_table_template.html`)

This template demonstrates the use of HTML tables to organize content in tabular format.

Example Usage:
```html
<table border="1">
    <tr>
        <th>Header 1</th>
        <th>Header 2</th>
    </tr>
    <tr>
        <td>Data 1</td>
        <td>Data 2</td>
    </tr>
</table>
```

### 3. Styled Template (`_styled_template.html`)

This template applies CSS styling to the email content to create a visually appealing layout.

Example Usage:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        .container {
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello, World!</h1>
        <p>This is a styled email template.</p>
    </div>
</body>
</html>
```

## How to Use Email Templates

1. Choose an email template based on the desired formatting and styling.
2. Select the chosen template while using the FlaskPost Mass Mailer application to send emails.

Users can refer to this documentation to understand the available email templates, their features, and how to use them with the FlaskPost Mass Mailer application. 

---