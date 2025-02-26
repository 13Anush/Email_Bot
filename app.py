from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import threading

app = Flask(__name__)
app.secret_key = "secret_key"

EMAIL_SERVER = "smtp.gmail.com"
EMAIL_PORT = 587


def send_email(to, subject, message, uname, pasw, pdf_paths):
    try:
        msg = MIMEMultipart()
        msg["From"] = uname
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Attach multiple PDFs
        for pdf_path in pdf_paths:
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
                msg.attach(part)

        server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT)
        server.starttls()
        server.login(uname, pasw)
        server.sendmail(uname, to, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error:", e)
        return False


def send_bulk_emails(csv_file, subject, message, uname, pasw, pdf_paths):
    try:
        df = pd.read_csv(csv_file)
        emails = df["Email"].tolist()
        total_emails = len(emails)
        sent_count = 0

        for email in emails:
            if send_email(email, subject, message, uname, pasw, pdf_paths):
                sent_count += 1

        flash(f"Emails Sent: {sent_count}/{total_emails}", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        subject = request.form["subject"]
        message = request.form["message"]

        # Handle multiple PDFs
        pdf_files = request.files.getlist("pdf_files")
        pdf_paths = []
        for pdf in pdf_files:
            if pdf.filename != "":
                pdf_path = os.path.join("uploads", pdf.filename)
                pdf.save(pdf_path)
                pdf_paths.append(pdf_path)

        # Handle Single Email
        if "single_email" in request.form:
            recipient = request.form["recipient"]
            if send_email(recipient, subject, message, email, password, pdf_paths):
                flash("Email Sent Successfully!", "success")
            else:
                flash("Failed to send email.", "danger")

        # Handle Bulk Emails
        elif "bulk_email" in request.form:
            csv_file = request.files["csv_file"]
            if csv_file.filename != "":
                csv_path = os.path.join("uploads", csv_file.filename)
                csv_file.save(csv_path)

                # Run bulk emails in a separate thread for efficiency
                threading.Thread(target=send_bulk_emails, args=(csv_path, subject, message, email, password, pdf_paths)).start()

                flash(f"Sending emails in the background...", "info")

        return redirect(url_for("index"))

    return render_template("index.html")


if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
