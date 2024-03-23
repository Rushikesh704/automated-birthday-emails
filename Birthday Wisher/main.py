from datetime import datetime
import pandas
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

MY_EMAIL_SMTP_SERVER = "smtp.gmail.com"
MY_EMAIL = ""
MY_PASSWORD = ""
MY_NAME = "Harsh Kanoje"

def send_birthday_email(receiver_email, subject, message): 
    try:
        with smtplib.SMTP(MY_EMAIL_SMTP_SERVER, 587) as connection:#Establish a connection with the SMTP server
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=receiver_email,
                msg=message
            )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def send_birthday_emails(): #Function to send birthday emails
    today = (datetime.now().month, datetime.now().day)
    data = pandas.read_csv("birthdays.csv")
    birthdays_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

    if today in birthdays_dict:
        birthday_person = birthdays_dict[today]
        print(f"Found birthday person: {birthday_person['name']}")
        file_path = f"letter_templates/letter_{random.randint(1,3)}.txt" #randomly select the letter template
        with open(file_path) as letter_file:
            contents = letter_file.read() # Read the contents of the letter template
            contents = contents.replace("[NAME]", birthday_person["name"])#
            contents = contents.replace("[MY_NAME]", MY_NAME)
            
            msg = MIMEMultipart()
            msg['From'] = MY_EMAIL
            msg['To'] = birthday_person["email"]
            msg['Subject'] = "Happy Birthday!"
            msg.attach(MIMEText(contents, 'plain'))
            
            print(f"Sending email to: {birthday_person['email']}")
            send_birthday_email(birthday_person["email"], "Happy Birthday!", msg.as_string())
    else:
        print("No birthdays today.")

# Schedule the email sending process to run daily at a specific time (e.g., 9:00 AM)
schedule.every().day.at("00:00").do(send_birthday_emails)

# Main loop to run the scheduler continuously
while True:
    schedule.run_pending()
    time.sleep(60)  # Sleep for 60 seconds before checking for scheduled tasks again
