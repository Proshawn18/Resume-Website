from flask import Flask, render_template, request, redirect
import smtplib
import os

def sendNoto(first_name, last_name, phone_num, email_address, message_body):
    # Environment variables — make sure these are set in your deployment
    sender_email    = os.environ.get('MY_EMAIL_FROM_SECRET')
    recipient_email = os.environ.get('EMAIL_FROM_SECRET')
    password        = os.environ.get('PASSWORD_FROM_SECRET')
    
    if not sender_email or not recipient_email or not password:
        raise RuntimeError("Missing one of SENDER_EMAIL, RECIPIENT_EMAIL, or EMAIL_PASSWORD in environment")

    # Build the message payload
    header = f"From: {sender_email}\r\nSubject: Message from Resume Website\r\n\r\n"
    footer = "\r\n"
    
    # Compose the “body” of the message
    body_lines = [
        f"Name: {first_name} {last_name}"
    ]
    if phone_num:
        body_lines.append(f"Phone: {phone_num}")
    if email_address:
        body_lines.append(f"Email: {email_address}")
    body_lines.append("")  # blank line before the user’s message
    body_lines.append(message_body)
    
    full_message = header + "\r\n".join(body_lines) + footer

    # Send via SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, full_message)
        print(f"Email sent to {recipient_email}")
    finally:
        server.quit()


app = Flask(__name__)
# Pull your Flask session secret from env; default is fine for local/dev
app.secret_key = "secret_key"


@app.route('/')
def hello_world():
    return render_template("resume.html")


@app.route('/message', methods=['POST'])
def handle_message():
    # Only accept POST requests here
    first_name    = request.form.get('firstname', '').strip()
    last_name     = request.form.get('lastname', '').strip()
    phone_num     = request.form.get('phone', '').strip()
    email_address = request.form.get('emailAddress', '').strip()
    message_body  = request.form.get('messages', '').strip()

    # You may want to validate these fields before sending
    sendNoto(first_name, last_name, phone_num, email_address, message_body)
    return redirect('/')


if __name__ == '__main__':
    # In production you’d use gunicorn/uwsgi instead of Flask’s built-in server
    app.run(host='0.0.0.0', port=8080)
