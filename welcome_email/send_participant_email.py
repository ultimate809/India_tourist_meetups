import json
import os
import smtplib
import boto3
import urllib.parse
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sender_email = os.getenv('SENDER_EMAIL')
email_password = os.getenv('EMAIL_PASSWORD')

def get_registration_email_body(name, title,location,date,description):
  return f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    padding: 20px;
                }}
                .email-container {{
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 30px;
                    max-width: 600px;
                    margin: auto;
                }}
                h1 {{
                    color: #4CAF50;
                    font-size: 24px;
                    text-align: center;
                }}
                p {{
                    font-size: 16px;
                    line-height: 1.5;
                    margin: 20px 0;
                }}
                .highlight {{
                    font-weight: bold;
                    color: #4CAF50;
                }}
                .footer {{
                    font-size: 12px;
                    color: #777;
                    text-align: center;
                    margin-top: 30px;
                }}
                .button {{
                    display: inline-block;
                    padding: 12px 20px;
                    margin-top: 20px;
                    background-color: #4CAF50;
                    color: white;
                    text-align: center;
                    text-decoration: none;
                    border-radius: 5px;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <h1>Successful Registration!</h1>
                <p>Dear <span class="highlight">{name}</span>,</p>
                <p>Thank you for registering for the <span class="highlight">{title}</span> vacation meetup!</p>
                <p>We are thrilled to have you on board for this amazing journey. Get ready to explore new places, meet fellow travelers, and create unforgettable memories!</p>
                <p><strong>Details:-</strong></p>
                <p><strong>Location:</strong> {location}</p>
                <p><strong>Date:</strong> {date}</p>
                <p><strong>Description:</strong> {description}</p>
                <p><strong>What's next?</strong></p>
                <p>We will send you further information about the itinerary and travel details shortly. In the meantime, make sure to check out our website for travel tips and preparation.</p>
                
                <p><a href="mailto:shauryakhurana500@gmail.com" class="button">Know More</a></p>
                
                <p class="footer">If you have any questions, feel free to contact us at shauryakhurana500@gmail.com</p>
            </div>
        </body>
    </html>
    """

# Define the send_email function
def send_email(email,subject,body):
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = email
  message["Subject"] = subject

  # Attach the email body
  message.attach(MIMEText(body, "html"))

  # Send the email via SMTP
  try:
    print("Sending email will now initiate connection")
    with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Using Gmail's SMTP server
      print("SMTP connection established")
      server.starttls()  # Upgrade to a secure connection
      server.login(sender_email, email_password)  # Log in to your email account
      server.sendmail(sender_email, email, message.as_string())
      print("Email sent successfully!")
  except Exception as e:
    print(f"Failed to send email: {e}")

def lambda_handler(event, context):

  s3 = boto3.client('s3')
  bucket_name = "meetupwelcomeemail"
  print(event['Records'])
  file_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

  try:
    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = response['Body'].read().decode('utf-8')
    data = json.loads(file_content)

    # Extract fields into variables
    name = data.get("name")
    email = data.get("email")
    title = data.get("title")
    location = data.get("location")
    date = data.get("date")
    description = data.get("description")

    date_obj = datetime.strptime(date, "%d/%m/%Y")
    formatted_date = date_obj.strftime("%B %d, %Y")

    subject = f"Successful Registration for {title} Vacation Meetup"
    email_body = get_registration_email_body(name,title,location,formatted_date,description)

    print(name, email, title, location, formatted_date, description)
    send_email(email,subject,email_body)
    print("Email code completed!")

    return {
      "statusCode": 200,
      "body": {
        "name": name,
        "email": email,
        "title": title,
        "location": location,
        "date": date,
        "description": description
      }
    }

  except Exception as e:
    print(f"Error retrieving file: {e}")
    return {
      "statusCode": 500,
      "body": f"Error retrieving file: {e}"
    }