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
mangaName = ''

name = ''
mainLink = ''
lastLink = ''


#Specifies the direcotry of the webdriver
driverPath = '/Applications/chromedriver'

#Add the headless option
options = Options()
options.add_argument('--headless')

print(mainLink)
driver = webdriver.Chrome( options = options, executable_path=driverPath)


def readFile():

    print("Reading file")
    

    # open the csv file
    with open('info.csv','r') as file:
        info = csv.reader(file,delimiter = ',')

        for line in info:
    
            global name
            global mainLink
            global lastLink

            name = line[0]
            mainLink = line[1]
            lastLink = line[2]

            # Call the check Function
            checkNewVolume()       

def checkNewVolume():

    print("Chekcing new voluems")

    #Declare strings used to scrape the site
    xPath  = '//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[1]/a'
    
    # go to the main link
    driver.get(mainLink)

    time.sleep(15)

    # save the link found so it can compre it to the one in the csv file
    latestLink = driver.find_element_by_xpath(xPath).get_attribute('href')
    

    # check if the newest link is the last downloaded volume, if no, it means it is a new volume
    if latestLink == lastLink:
        print('All uptodate')
        downloadVolume(latestLink)

    else:
        print('Downloading the new file')
        downloadVolume(latestLink)

def downloadVolume(link):

    # Change the directory 
    os.chdir('/Users/pedrocruz/Desktop/MangaDownloader/mangaTest')

    print("Downloading new volume")
    imagexPath = '//*[@id="divImage"]/p[%s]/img'

    driver.get(link)
    # a list with all the pages' links 
    imgLinks = []

    # Creates the progrss bar 
    linkBar = IncrementalBar('Gathering the image links', max = 100)

    # goes and tries to get 100 pages 
    for i in range(1,101):

        try:
            imgLinks.append(driver.find_element_by_xpath(imagexPath%(i)).get_attribute('src'))
        
        except:
            pass

        # update the progrss bar 
        linkBar.next()

    # Downloads the images with the requests library
    page = 1
    for link in imgLinks:

        # Creates a file to save the image in
        fileName = ""
        if page<10:
            fileName = "00%d.png"%(page)

        elif page >=10 and page < 100:
            fileName = "0%d.png"%(page)

        else :
            fileName = "%d.png"%(page)

        response = requests.get(link)
        
        with open(fileName,'wb') as image:
            image.write(response.content)
        
        page+=1


def sendMail():

    global userName
    global password

    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = userName 
    
    # storing the receivers email address  
    msg['To'] = userName 
    
    # storing the subject  and format the string to add the manga title 
    msg['Subject'] = "New volume added for %s" %()
    
    filename = "as-Vol.0092.pdf"
    attachment = open("as-Vol.0092.pdf", "rb") 
    
    # instance of MIMEBase and named as p 
    pdf = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    pdf.set_payload((attachment).read()) 
    
    # encode into base64 
    encoders.encode_base64(pdf) 
    
    pdf.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    
    # attach the instance 'p' to instance 'msg' 
    msg.attach(pdf)

    # Converts the Multipart msg into a string 
    text = msg.as_string()
    
    # Starts the mail connection 
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(userName,password)

    # Send the message adn quit 
    server.sendmail(userName,userName,text)
    server.quit()


# sendMail()
readFile()

