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
import datetime
import time
import sys
import csv
import os

userName = 'xxxxxxxxx'
password = 'xxxxxxxxx'
mangaName = ''

name = ''
mainLink = ''
lastLink = ''

volumeName = ''

# Creates the lists and then clean them, since you can't create empty lists in python
namesList = [None]
mainLinks = [None]
lastLinks = [None]
imagesNames = [None]

namesList = []
mainLinks = []
lastLinks = []
imagesNames = []

charactersAllowed = 'qweertyuiopasdfghjklzxcvbnm1234567890-." \''




#Specifies the direcotry of the webdriver
driverPath = '/Applications/chromedriver'

#Add the headless option
options = Options()
options.add_argument('--headless')


def readFile():

    print("Reading file")

    # open the csv file
    with open('info.csv','r') as file:
        info = csv.reader(file,delimiter = ',')

        for line in info:

            global name
            global mainLink
            global lastLink
            global namesList
            global mainLinks




            name = line[0]
            mainLink = line[1]
            lastLink = line[2]

            # Add the info to the lists so it can be updated afterwards
            namesList.append(line[0])
            mainLinks.append(line[1])

            # Call the check Function
            checkNewVolume()

        #update the info file
        updateFile()

def checkNewVolume():

    global volumeName
    global lastLink
    global lastLinks
    global charactersAllowed

    print("Checking for new volumes...")

    #Declare strings used to scrape the site
    xPath  = '//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[1]/a'

    # go to the main link
    driver.get(mainLink)

    time.sleep(15)

    # save the link found so it can compre it to the one in the csv file
    latestLink = driver.find_element_by_xpath(xPath).get_attribute('href')
    volumeName = driver.find_element_by_xpath(xPath).text

    # Clean the name
    for letter in volumeName:

        # If the character not in the charactersAllowed string, get rid of it
        if letter not in charactersAllowed:
            volumeName = volumeName.replace(letter,'')

    print(volumeName)


    # check if the newest link is the last downloaded volume, if no, it means it is a new volume
    if latestLink == lastLink:
        print('All uptodate')

        lastLinks.append(latestLink)

    else:
        print('Downloading the new file')
        # Add the last link to the list so it can be transffered to the info.csv file
        lastLinks.append(latestLink)
        print(latestLink)
        downloadVolume(latestLink)

def downloadVolume(link):

    global volumeName
    global imagesNames

    # Change the directory
    os.chdir('/Users/pedrocruz/Desktop/MangaDownloader/mangaTest')

    print("Downloading new volume")
    imagexPath = '//*[@id="divImage"]/p[%s]/img'

    driver.get(link)

    # a list with all the pages' links
    imgLinks = []

    # Clears the imagesName list for the following part
    imagesNames = []

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
    imageBar = IncrementalBar('Downloading Images', max = len(imgLinks))
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

        # update the image number and the progress bar
        page+=1
        imageBar.next()

        # Add the filename to the imagesName list, so we can delete it later, so there is no "contamination" in the next volume download
        imagesNames.append(fileName)

    # Create the pdf out of all the png using imagemagick -> for unix systems
    print('\nmaking pdf...')
    formula = 'convert *png "%s.pdf"'%(volumeName)
    os.system(formula)

    # Delete the images, since the pdf was already
    for file in imagesNames:
        os.system("rm "+file)

    sendMail()

    # Delete the pdf since it was already sent via email
    os.system('rm '+volumeName)

def sendMail():


    global userName
    global password
    global volumeName
    global name

    kindle = 'xxxxxxxxx'

    print("Sending email...")
    msg = MIMEMultipart()
    notification = MIMEMultipart()

    # Send email to both the kindle and personal email, as notification
    # storing the senders email address
    msg['From'] = userName
    notification['From'] = userName

    # storing the receivers email address
    msg['To'] = kindle
    notification['To'] = userName

    filename = volumeName

    # storing the subject  and format the string to add the manga title
    msg['Subject'] = "New volume added for %s, %s" %(name,filename)
    notification['Subject'] = "New volume added for %s,%s" %(name,filename)


    print(volumeName+'.pdf')
    attachment = open(volumeName+'.pdf', "rb")

    # instance of MIMEBase and named as p
    pdf = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    pdf.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(pdf)

    pdf.add_header('Content-Disposition', "attachment; filename= %s.pdf" % (filename)  )

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

    # Send the message and quit, if it fails, send an email with the error
    try:
        server.sendmail(userName,kindle,text)
        server.sendmail(userName,userName,notification.as_string())

    except Exception as e:
        server.sendmail(userName,userName,e)
        server.sendmail(userName,userName,volumeName+" was added but shit happened")

    server.quit()

def updateFile():

    global namesList
    global lastLinks
    global mainLinks

    print(namesList,lastLinks,mainLinks)
    # Creates the progress bar
    savingBar = IncrementalBar("Saving file",max = len(namesList))

    # The path to the info file
    path = '/Users/pedrocruz/Desktop/MangaDownloader/info.csv'

    # Opens the file, write mode
    with open(path,'w',newline ='') as file:
        info = csv.writer(file,delimiter = ',')

        counter = 0
        for name in namesList:
            info.writerow([name,mainLinks[counter],lastLinks[counter]])

            counter+=1
            savingBar.next()

        print(colored("File saved","green"))



while True:


    # Clear the lists for the next iteration
    namesList = []
    mainLinks = []
    lastLinks = []
    
    # Get the current hour
    hour = datetime.datetime.now().hour

    # If it is time to check, do so, and then sleep for an hour
    if hour == 4 or hour == 19:

        try:
            os.system('clear')
            print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')

            # Open the driver and go to the function
            driver = webdriver.Chrome( options = options, executable_path=driverPath)
            readFile()

            # close the driver
            driver.quit()

        except:
            # if an error occurs, reset the driver, to try to prevent further interruptions
            driver.quit()
            driver = webdriver.Chrome(options = options, executable_path=driverPath)

            pass

        print(colored('That is all Folks','green'))

    time.sleep(3600)
