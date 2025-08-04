from flask import Flask, render_template, request, redirect, session
import smtplib
import os


def sendNoto(name1, name2, phoneNum, emailAddress, message):
    sender_email = os.environ.get('MY_EMAIL_FROM_SECRET')
    rec_email = os.environ.get('EMAIL_FROM_SECRET')
    password= os.environ.get('PASSWORD_FROM_SECRET')
    
    finalMessage = str("From: ")+ str(name1)+ str(" ")+ str(name2)+ str("\n")
    if phoneNum != "":
        if emailAddress != "":
            finalMessage = str(finalMessage)+ str(phoneNum)+ str(" ")+ str(emailAddress)+ str("\n")
        else:
            finalMessage = str(finalMessage)+ str(phoneNum)+ str("\n")
    elif emailAddress != "":
        finalMessage = str(finalMessage)+ str(emailAddress)+ str("\n")


    finalMessage = str(finalMessage)+ str(message)
    
    
    msg = f"""Subject: From Resume Website\n
{str(finalMessage)}
"""

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success")
    server.sendmail(sender_email, rec_email, msg)
    print("Email has been sent to ", rec_email)


app = Flask(__name__)
app.secret_key = "secret_key"



@app.route('/')
def hello_world():
  return render_template("resume.html")

# Login page
@app.route('/message', methods=['GET', 'POST'])
def login():
    # Get form fields
    firstName = request.form['firstname']
    lastName = request.form['lastname']
    phoneNum = request.form['phone']
    emailAddress = request.form['emailAddress']
    message = request.form['messages']
    
    sendNoto(firstName, lastName, phoneNum, emailAddress, message)
    
    return redirect("/")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
