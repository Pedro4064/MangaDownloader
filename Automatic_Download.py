from selenium import webdriver
from progress.bar import IncrementalBar
from termcolor import colored
import requests
import time
import sys
import os


################################################################################
#Change:
#   fCounter -> The number of volumes = (number of last volume - number of first volume + 1)
#   nLinks (Depending on the series you want to download and the number of volumes/links on the main page) -> The number of volumes = (number of last volume - number of first volume + 1) and add 2 (The site adds 3 to the xPath for the links...)
#   The diecotry on line 72 for the correct one you want to add the child direcotris and .JPEGs -> To get the full directory path go to it on the terminal and enter "pwd"
#   mainLink -> To the link for the main page of the series you wish to download
#
#Observations:
#   Check the number of pages of all the volumes downloaded
#   Check the number of pages from the volumes to be downloaded and change the range of the for loop to more than necessary  to be sure (The current number is 60 pages)
#   WORKS ONLY WITH THE KISSMANGA SITE -> https://kissmanga.com/
################################################################################


#Declare strings used to scrape the site
xPath  = '//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[%s]/td[1]/a'
imagexPath = '//*[@id="divImage"]/p[%s]/img'
imageName = '%s.JPEG'


print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')
if sys.argv[1] == '-h':
    print(colored( "If an error occurred and the whole programm shuts downs, you can pass the number for the last downloaded volume as an argument so it will skip to that specific volume and move on, no need to start all over again","yellow"))
    print(colored("Example:  python3.7 Automatic_Download.py 39 \n In the case above the programm will skip all the pages already downloaded and star from 39 and move on(the download starts from the newest to the oldest)",'yellow'))
    quit()

#Specifies the direcotry of the webdriver
driver = webdriver.Chrome('/usr/local/bin/chromeDriver')


#Creates lists used as reference
volLinks = []
imgLinks = []
error = []

#directory to which create a directory for each vol and download the images & the final directory for the pdfs
imageDirectory = ''
pdfDirectory = ''

seriesName = ''

userNumberOfPages = 0
fCounter = 0

def User():

    os.system('clear')
    print('\n')
    print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')

    #Specify that the folowing variables are global
    global imageDirectory
    global pdfDirectory
    global userNumberOfPages
    global fCounter
    global seriesName
    global driver

    seriesName = input('The name of the series: ')
    mainLink = input('The main Link: ')
    fCounter = int(input('The number of volumes: '))
    imageDirectory = input('The directory for the images: ')
    pdfDirectory = input('The final destination for the PDFs: ')
    userNumberOfPages = int(input('The estimated number of pages per volume: ')) + 20 #Adds 20 to overshute the number of pages to ensure you got all
    nLinks = fCounter-1

    print('\n')

    GatherVolumeLinks(mainLink,nLinks)

def GatherVolumeLinks(mainLink,nLinks):

    #Specifies global variable
    global volLinks
    global driver
    global fCounter

    #Go to webPage
    driver.get(mainLink)

    #Wait for it to load
    time.sleep(15)

    #Creates a progress bar so the user can check progress
    print('\n')
    volBar = IncrementalBar('Gathering the links for all volumes', max = nLinks)

    #Get the links for the volumes on the main page and adds to the volLinks list
    for i in range(nLinks):

        #The xPath counter on the site starts at 3
        i+=3
        #Get the volume links available on the page
        volLinks.append(driver.find_element_by_xpath(xPath%(i)).get_attribute('href'))
        #updates the progress bar
        volBar.next()

    print("All the volumes' links were collected. Initializing downloads...")
    time.sleep(2)

    GatherImagesLinks()

def GatherImagesLinks():

    #Define global variables
    global volLinks
    global imgLinks
    global error
    global userNumberOfPages
    global seriesName
    global driver
    global fCounter


    os.system('clear')

    #Create a progress bar
    print('\n')
    downloadBar = IncrementalBar('Donwloading volumes: ',max = len(volLinks))
    skip = fCounter
    #Goes link by link (that was obtained from the main page of the series)
    for link in volLinks:

        if len(sys.argv) != 1:

            #If an error occurred and the whole programm shuts downs, you can pass the number for the last downloaded volume as an argument so it will skip to that specific volume and move on, no need to start all over again
            if skip >int (sys.argv[1]):

                print("Skipping volume %d" %(skip))
                skip -= 1
                fCounter-=1
                continue

            if skip <=int(sys.argv[1]):

                print("Downloading volume %d" %(skip))
                skip -= 1






        os.system('clear')
        print('\n')
        print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')

        try:

            #Goes to the volume page
            driver.get(link)

            #wait to ensure the dynamic javascript loaded
            time.sleep(15)

            #Creates a progress bar
            print('\n')
            linkBar = IncrementalBar('Gathering the image links', max = userNumberOfPages)

            #Get the link for each page from volume
            for i in range(userNumberOfPages):

                #The images' links start at 1, not at 0
                i+=1

                try:

                    imgLinks.append(driver.find_element_by_xpath(imagexPath%(i)).get_attribute('src'))

                    #update the progress bar
                    linkBar.next()

                except:

                    #update the progress bar and continue
                    linkBar.next()
                    continue

        except:
            error.append(link)

            #Closes the dirver and summons it againf to prevent future failures
            driver.quit()
            driver = webdriver.Chrome('/usr/local/bin/chromeDriver')


        downloadImages()
        #Clears the imgLinks list so the next volume's ones can be added
        imgLinks = []

        #After that go to the next Volume link on the list
        downloadBar.next()

def downloadImages():

    global imgLinks
    global imageDirectory
    global pdfDirectory
    global driver
    global fCounter

    counter = 0
    #Change to the images' directory
    os.chdir(imageDirectory)

    #Creates the directory for the images (The name has to have 3 digits, do it checks to see the number of digits of the volume to name it correctly)
    if fCounter < 10:
        os.system('mkdir Vol.00%s' %(fCounter))
        os.chdir('Vol.00%s' %(fCounter))

    elif fCounter >= 10 and fCounter < 100:
        os.system('mkdir Vol.0%s' %(fCounter))
        os.chdir('Vol.0%s' %(fCounter))

    elif fCounter >= 100:
        os.system('mkdir Vol.%s' %(fCounter))
        os.chdir('Vol.%s' %(fCounter))



    print('\n')

    #Creates a progress bar
    imageBar = IncrementalBar('Downloading images' , max = len(imgLinks))

    #Downloads the image and writes it on a JPEG file
    for image_link in imgLinks:

        counter +=1
        response = requests.get(image_link)

        #Waits 2 seconds t be sure (i do not know)
        time.sleep(2)

        try:
            if counter < 10:

                with open('00%s.JPEG' %(counter), 'wb') as image:
                    image.write(response.content)

            elif counter >=10 and counter <100:

                with open('0%s.JPEG' %(counter), 'wb') as image:
                    image.write(response.content)

            elif counter >=100:

                with open('%s.JPEG' %(counter),'wb') as image:
                    image.write(response.content)


            #updates the progress bar
            imageBar.next()

        except:
            imageBar.next()
            continue

    #I do not think it is necessary; however, set the counter variable to zero again so there are no problens
    counter = 0

    #Creates a pdf from all images on the directory and moves it to the pdf directory
    if fCounter < 10:
        os.system('convert *.JPEG "%s-Vol.00%d.pdf"' %(seriesName,fCounter))
        os.system('mv "%s-Vol.00%d.pdf" %s' %(seriesName,fCounter,pdfDirectory))

    elif fCounter >= 10 and fCounter < 100:
        os.system('convert *.JPEG "%s-Vol.0%d.pdf" ' %(seriesName,fCounter))
        os.system('mv "%s-Vol.0%d.pdf" %s' %(seriesName,fCounter,pdfDirectory))

    elif fCounter >= 100:
        os.system('convert *.JPEG "%s-Vol.%d-.pdf"' %(seriesName,fCounter))
        os.system('mv "%s-Vol.%d-.pdf" %s' %(seriesName,fCounter,pdfDirectory))

    #Decreases the fCounter number to keep track of the volume it's creating(it downloads from the newest to the oldest)
    fCounter-=1


while True:

    User()

    if len(error) != 0:

        print('\n')
        print(colored("[ERROR] Unable to download the folowing volumes: ",'red'))

        for link in error:
            print('•',link)
