from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from progress.bar import IncrementalBar
from termcolor import colored
import smtplib 
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

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(userName,password)

    message = 'Subject: python Test'

    server.sendmail(userName,userName,message)
    server.quit()


sendMail()