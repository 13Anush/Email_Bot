# Bulk Email Sender

## Overview
This is a Flask-based web application that allows users to send single or bulk emails with attachments. Users can provide email credentials, compose messages, attach PDF files, and send emails either individually or in bulk using a CSV file containing recipient email addresses.

## Features
- Send single emails with attachments
- Send bulk emails using a CSV file
- Background processing for bulk email sending
- Flash messages for user notifications
- Secure login handling

## Project Structure
```
project_root/
|-- app.py                # Main Flask application
|-- requirements.txt      # Required Python dependencies
|-- .gitignore            # Git ignore file
|-- templates/
|   |-- index.html        # HTML file for frontend
|-- static/
|   |-- css/              # CSS files for styling
```

## Installation
### Prerequisites
- Python 3.x installed
- Flask installed (see `requirements.txt`)

### Steps
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd project_root
   ```
2. Create a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate   # On macOS/Linux
   .venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```sh
   python app.py
   ```

## Usage
- Open `http://127.0.0.1:5000/` in your browser.
- Enter your email credentials and compose an email.
- Attach PDF files if necessary.
- To send bulk emails, upload a CSV file containing recipient email addresses under a column named `Email`.
- Click `Send` to send emails.

## .gitignore
The `.gitignore` file ensures the following files and folders are ignored:
```
# IDE-specific files
.idea/
```

## License
This project is open-source. Feel free to modify and use it as needed.

