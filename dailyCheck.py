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

volumeName = ''
 
# Creates the lists and then clean them, since you can't create empty lists in python
namesList = [None]
mainLinks = [None]
lastLinks = [None]

namesList = []
mainLinks = []
lastLinks = []



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

    print("Checking for new volumes...")

    #Declare strings used to scrape the site
    xPath  = '//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[1]/a'
    
    # go to the main link
    driver.get(mainLink)

    time.sleep(15)

    # save the link found so it can compre it to the one in the csv file
    latestLink = driver.find_element_by_xpath(xPath).get_attribute('href')
    volumeName = driver.find_element_by_xpath(xPath).text
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
        
        page+=1
        imageBar.next()

    # Create the pdf out of all the png using imagemagick -> for unix systems
    print('\nmaking pdf...')
    formula = 'convert *png "%s.pdf"'%(volumeName)
    os.system(formula)
    sendMail()

def sendMail():

    print("ok")
    # global userName
    # global password
    # global volumeName
    # global name

    # print("Sending email...")
    # msg = MIMEMultipart() 
  
    # # storing the senders email address   
    # msg['From'] = userName 
    
    # # storing the receivers email address  
    # msg['To'] = userName 
    
    # # storing the subject  and format the string to add the manga title 
    # msg['Subject'] = "New volume added for %s" %(name)
    
    # filename = volumeName
    # attachment = open(volumeName+'.pdf', "rb") 
    
    # # instance of MIMEBase and named as p 
    # pdf = MIMEBase('application', 'octet-stream') 

    # # To change the payload into encoded form 
    # pdf.set_payload((attachment).read()) 
    
    # # encode into base64 
    # encoders.encode_base64(pdf) 
    
    # pdf.add_header('Content-Disposition', "attachment; filename= %s" % filename+".pdf") 
    
    # # attach the instance 'p' to instance 'msg' 
    # msg.attach(pdf)

    # # Converts the Multipart msg into a string 
    # text = msg.as_string()
    
    # # Starts the mail connection 
    # server = smtplib.SMTP('smtp.gmail.com',587)
    # server.ehlo()
    # server.starttls()
    # server.ehlo()

    # server.login(userName,password)

    # # Send the message and quit, if it fails, send an email with the error
    # try:
    #     server.sendmail(userName,userName,text)
    # except Exception as e:
    #     server.sendmail(userName,userName,e)
    #     server.sendmail(userName,userName,volumeName+" was edded but shit happened")

    # server.quit()

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
            print(name,mainLink[counter],lastLinks[counter])
            counter+=1
            savingBar.next()
        
        print(colored("File saved","green"))



# while True:

    # try:
os.system('clear')
print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')
readFile()

    # except:
    #     pass

    # i = input('->')
