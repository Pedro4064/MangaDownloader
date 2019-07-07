from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from progress.bar import IncrementalBar
from termcolor import colored

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

import requests
import time
import sys
import csv
import os

userName = 'pedrohlcruz@gmail.com'
password = 'waqfpbvuafucqeyu'

def readFile():
    print("Reading file")

def checkNewVolume():
    print("Chekcing new voluems")

def downloadVolume():
    print("Downloading new volume")

def sendMail():

    global userName
    global password

    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = userName 
    
    # storing the receivers email address  
    msg['To'] = userName 
    
    # storing the subject  
    msg['Subject'] = "new Manga volume added"
    
    filename = "as-Vol.0092.pdf"
    attachment = open("as-Vol.0092.pdf", "rb") 
    
    # instance of MIMEBase and named as p 
    p = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    p.set_payload((attachment).read()) 
    
    # encode into base64 
    encoders.encode_base64(p) 
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    
    # attach the instance 'p' to instance 'msg' 
    msg.attach(p)

    # Converts the Multipart msg into a string 
    text = msg.as_string()
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(userName,password)

    # message = 'Subject: python Test'

    server.sendmail(userName,userName,text)
    server.quit()


sendMail()