from selenium import webdriver
from termcolor import colored
from progress.bar import IncrementalBar
import requests
import time
import os

#Specifies the webdriver's directory
driver = webdriver.Chrome('/usr/local/bin/chromeDriver')

imgLinks = []

#Link of the mainpage(with all the other links)
imagexPath = '//*[@id="divImage"]/p[%s]/img'
imageName = '%s.JPEG'
counter = 0

#prints the banner
os.system("clear")
print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     ')
print("\n")

#Asks for the user input
directory = input("Inser the directory to download all the images: ")
pdfDirectory = input("Insert the directory to move the pdf to: ")
volLink = input("Insert the volume's link: ")
volNumber = input("Insert the volume Number: ")
nPages = input('Insert the number of pages in the volume: ')


os.system("clear")
print("\n")

#prompts the user to check if the info is correct
print("Are all the informations correct?\n")
print("Images's direcotry:",directory)
print("Pdf's direcoty:",pdfDirectory)
print("The volume's link:",volLink)
print("The volume number is:",volNumber)

answer = input("[y/n] ")
os.system('clear')

#If answer not correct abort the program
if answer == "n":
    quit()

#Else continue with the operation
else:
    driver.get(volLink) #uses to webdriver to make a request and open a browser window
    time.sleep(15)      #Waits 15 seconds to make sure the page loaded fully

    #Creats the progresses bars for user reference
    gatheringPageBar = IncrementalBar("Gathering the pages' link",max = int(nPages))

    for i in range(int(nPages)):

        i+=1
        time.sleep(5)
        gatheringPageBar.next() #Updates the progress bar

        try: #Adds the link of each page to the imgLinks list
            imgLinks.append(driver.find_element_by_xpath(imagexPath%(i)).get_attribute('src'))

        except:#Print the number of the page it encounterred an error and continues to the next page
            print(colored("[ERROR] Failed to get the link for the "+str(i)+" page",'red'))
            continue

    print("\n")
    print("Gathered all the links, moving to "+directory)
    os.chdir(directory) #move to the directory specified by the user to save the images

    #Creats another progress bar for user reference -> the progress of the image download
    downloadBar = IncrementalBar("Downloading images",max = len(imgLinks))


    for link in imgLinks: #goes through each page/image link

    #counter < 10 because from 0-9 the name is 00x.JPEG, but from 10 onward it's 0x.JPEG ->where x is the number of the page (to make sure the order is correct when making the pdf)
        if counter < 10:
            response = requests.get(link)

            with open("00%s.JPEG"%(counter),'wb') as image:#Creates a .JPEG file and downloads the image from the link
                image.write(response.content)

        elif counter >= 10 and counter < 100:

            response = requests.get(link)
            with open("0%s.JPEG"%(counter),'wb') as image:

                image.write(response.content)
        elif counter >= 100:

            response = requests.get(link)
            with open("%s.JPEG"%(counter),'wb') as image:

                image.write(response.content)

        #updates the progressBar
        downloadBar.next()


        counter+=1


    try: #to make a pdf out of all the .JPEG images with the imagemagick terminal command
        if int(volNumber) < 10:
            os.system("convert *.JPEG Vol.00%s.pdf"%(volNumber))
            os.system('mv Vol.00%s.pdf %s' %(volNumber,pdfDirectory))

        elif int(volNumber) >= 10 and int(volNumber) <100:
            os.system("convert *.JPEG Vol.0%s.pdf"%(volNumber))
            os.system('mv Vol.0%s.pdf %s' %(volNumber,pdfDirectory))

        elif int(volNumber) >=100:
            os.system("convert *.JPEG Vol.%s.pdf"%(volNumber))
            os.system('mv Vol.%s.pdf %s' %(volNumber,pdfDirectory))

    except:
        print(colored("[ERROR] Could not change to the finale/pdf directory",'red'))
