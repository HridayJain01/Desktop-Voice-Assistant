import tkinter as tk
from email.message import EmailMessage
import ssl
import smtplib

sender_email = "hridaymjain@gmail.com"
sender_password = 'ohez rzsb nuyj gcxj'

def send_email(receiver_emails, subject, custom_h1):
    # HTML content for the email body with customizable h1
    body = f"""\
    <!DOCTYPE html>
    <html>
    <head>
        <title>Connection Established</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                text-align: center;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 10px;
                padding: 20px;
                width: 80%;
                margin: auto;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            }}
            h1 {{
                color: #333333;
            }}
            p {{
                color: #666666;
                margin-bottom: 20px;
            }}
            .status {{
                color: #1abc9c;
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{custom_h1}</h1>
            <p>The Desktop assistant is ready to deploy messages now.</p>
            <p>This email serves as a demonstration of an innovative UI using HTML.</p>
            <div class="status">Everything is working smoothly!</div>
        </div>
    </body>
    </html>
    """

    # Create EmailMessage object
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = ', '.join(receiver_emails)  # Join receiver addresses into a comma-separated string
    em['Subject'] = subject
    em.add_alternative(body, subtype='html')  # Set email body as HTML

    # SSL context
    context = ssl.create_default_context()

    # Send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_emails, em.as_string())

def open_gui():
    def send_email_from_gui():
        receiver_emails = receiver_email_entry.get().split(",")  # Split receiver emails by comma
        subject = subject_entry.get()
        custom_h1 = h1_entry.get()  
        send_email(receiver_emails, subject, custom_h1)
        root.destroy()

    root = tk.Tk()
    root.title("Quick Email")

    receiver_email_label = tk.Label(root, text="Receiver Emails (comma-separated):")
    receiver_email_label.grid(row=0, column=0, sticky="w")
    receiver_email_entry = tk.Entry(root)
    receiver_email_entry.grid(row=0, column=1)

    subject_label = tk.Label(root, text="Subject:")
    subject_label.grid(row=1, column=0, sticky="w")
    subject_entry = tk.Entry(root)
    subject_entry.grid(row=1, column=1)

    h1_label = tk.Label(root, text="Body")
    h1_label.grid(row=2, column=0, sticky="w")
    h1_entry = tk.Entry(root)
    h1_entry.grid(row=2, column=1)

    send_button = tk.Button(root, text="Send Email", command=send_email_from_gui)
    send_button.grid(row=3, column=0, columnspan=2)

    root.mainloop()

open_gui()