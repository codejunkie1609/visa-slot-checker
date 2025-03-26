# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:26:36 2023

@author: Sricharan
"""
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body):
    # Replace these values with your email and SMTP server details
    sender_email = 'kscuniadmission@gmail.com'
    sender_password = 'hagclsswppwheqpj'
    receiver_email = 'sricharan596@gmail.com, kscuniadmission@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Create a message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the HTML body of the email
    msg.attach(MIMEText(body, 'html'))

    try:
        # Establish a connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Log in to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Quit the server
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
        
        
url = 'https://visaslots.info'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

req = Request(url, headers=headers)

try:
    page = urlopen(req)
    print(page)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    # Find the details section
    details_section = soup.find('details', {'id': 'vsloc-f1-f2'})
    
    # Find all the rows in the table body
    table_rows = details_section.select('tbody tr')
    
    # Extract information from the desired section
    for row in table_rows:
        location = row.select_one('td a').text.strip()
        visa_type = row.select_one('td:nth-child(2)').text.strip()
        updated_time = row.select_one('td.updated')['data-ts'].strip()
        earliest = row.select_one('td.earliest').text.strip()
        slots = row.select_one('td:nth-child(5)').text.strip()
        if "CONSULAR" in location:
            if "N/A" not in earliest:
                earliest = datetime.strptime(earliest, '%Y %b %d').date() 
                print(earliest)
                start_date = datetime.strptime('2024 Feb 01', '%Y %b %d').date()
                end_date = datetime.strptime('2024 Apr 15', '%Y %b %d').date()
               
                if start_date < earliest <= end_date:
                    print(f"Location: {location}")
                    print(f"Visa Type: {visa_type}")
                    print(f"Updated Time: {updated_time}")
                    print(f"Earliest: {earliest}")
                    print(f"Slots: {slots}")
                    print("------")
                    subject = "Update on availability of F1 visa slots"
                    body = f"<p>Hurry! {slots} slot(s) are available from the date <b>{earliest.strftime('%B %d, %Y')}</b> at <b>{location}</b></p>"
                    send_email(subject, body)
            else:
                print(f"The date {earliest} (slots - {slots}) is not between 01st Debruary 2024 and 15th April 2024.")
                    
except Exception as e:
    print(f"An error occurred: {e}")
