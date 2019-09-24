from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from progress.bar import IncrementalBar
from termcolor import colored
import json

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

userName = 'pedrohlcruz@gmail.com'
password = 'waqfpbvuafucqeyu'
mangaName = ''

name = ''
mainLink = ''
lastLink = ''

volumeName = ''
 
# Creates the lists and then clean them
imagesNames = []
mangas = []

charactersAllowed = 'qweertyuiopasdfghjklzxcvbnm1234567890-." \''


#Specifies the direcotry of the webdriver
driverPath = '/usr/lib/chromium-browser/chromedriver'


# The path to the info file
infoPath = '/home/pi/Desktop/mDownloader/"Raspberry Pi Daily check"/manga.json'


#Add the headless option
options = Options()
options.add_argument('--headless')

print(mainLink)


# Creates the manga Class to store all the necessary values
class manga:
    
    def __init__(self,**kwargs):

        self.name = kwargs.get('name','manga')
        self.mainUrl = kwargs.get('mainUrl')
        self.lastUrl = kwargs.get('lastUrl')

    


def readFile():

    print("Reading file")
    
    # open the json file on the mDownloader
    with open(infoPath,'r') as file:
        
        # get the json data and make it into a list of dictionaries
        data = json.loads(file.read())

        for manga in data:
    
            global name
            global mangas
            global mainLink
            global lastLink
            
            

    

            name = manga.get('title')
            mainLink = manga.get('mainURL')
            lastLink = manga.get('lastURL')

            print(name,mainLink, lastLink)
            # Creates a new instance of the manga class, them add it to the mangas list with its info
            mangas.append(manga(name = name, mainUrl = mainLink, lastUrl = lastLink))        
            
def checkNewVolume():

    global mangas
    global volumeName 
    global charactersAllowed

    print("Checking for new volumes...\n")

    for series in mangas:
            
        #Declare strings used to scrape the site
        xPath  = '//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[1]/a'
        
        # go to the main link
        driver.get(series.mainUrl)

        time.sleep(15)

        # save the link found so it can compre it to the one in the csv file
        latestLink = driver.find_element_by_xpath(xPath).get_attribute('href')
        volumeName = driver.find_element_by_xpath(xPath).text

        # Clean the name
        for letter in volumeName:
            
            # If the character not in the charactersAllowed string, get rid of it
            try:
                if letter.casefold() not in charactersAllowed:
                    volumeName = volumeName.replace(letter,'')

            except Exception as e:
                print(e)

        print(volumeName)
        

        # check if the newest link is the last downloaded volume, if not, it means it is a new volume
        if latestLink == series.lastUrl:
            print('All uptodate\n')

            

        else:
            print('Downloading the new file')
            
            # Updates the instance's lastUrl
            series.lastUrl = latestLink

            print(latestLink)
            downloadVolume(latestLink)

def downloadVolume(link):

    global volumeName

    # Change the directory 
    os.chdir('/media/pi/PEDRO CRUZ')
    

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

    # Delete the pdf since it was already sent
    os.system('rm '+'"'+volumeName+'"')

def sendMail():

    
    global userName
    global password
    global volumeName
    global name

    kindle = 'usa.ale@kindle.com'

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

    # storing the subject  and format the string to add the manga title 
    msg['Subject'] = "New volume added for %s" %(name)
    notification['Subject'] = "New volume added for %s" %(name)
    
    filename = volumeName
    attachment = open(volumeName+'.pdf', "rb") 
    
    # instance of MIMEBase and named as p 
    pdf = MIMEBase('application', 'octet-stream') 

    # To change the payload into encoded form 
    pdf.set_payload((attachment).read()) 
    
    # encode into base64 
    encoders.encode_base64(pdf) 
    
    pdf.add_header('Content-Disposition', "attachment; filename= %s.pdf" % (filename)) 
    
    # attach the instance 'pdf' to instance 'msg' 
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

    
    global infoPath
    
    
    # tell the user the file is being saved 
    print('The json file is being saved')
    


    # Opens the file, write mode
    with open(infoPath,'w') as file:
    
        # dumps the list of dictionary in the json file with 4 as indent
        file.write(json.dumps(mangas,indent=4))
        
        print(colored("File saved","green"))

def logo():
    print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')


while True:

    # Clear the list
    mangas = []

    #Get the current hour
    hour = datetime.datetime.now().hour
    
    os.system("clear")
    logo()    

    # If it is time to check, do so, and then sleep for an hour 
    if hour == 4 or hour == 19:

        try:
            os.system('clear')
            logo()

            # Open the driver and go to the function
            driver = webdriver.Chrome( options = options, executable_path=driverPath)

            readFile()
            checkNewVolume()
            updateFile()



            # close the driver
            driver.quit()

        except Exception as e:
            # if an error occurs, reset the driver, to try to prevent further interruptions, and save the file just in case
            driver.quit()
            driver = webdriver.Chrome( options = options, executable_path=driverPath)

            updateFile()
            print(e)
            continue

        print(colored('That is all Folks','green'))
    
        
    #Sleep for an hour so it doesn't require a lot of cpu from the PI
    print(colored("Checking the time again in an hour...","yellow"))
    time.sleep(3600)
    
