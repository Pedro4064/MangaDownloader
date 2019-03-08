from selenium import webdriver
from termcolor import colored
import requests
import time
import os

driver = webdriver.Chrome('/usr/local/bin/chromeDriver')
imgLinks = []


#Link of the mainpage(with all the other links)
imagexPath = '//*[@id="divImage"]/p[%s]/img'
imageName = '%s.JPEG'
counter = 0

os.system("clear")
print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     ')
print("\n")

directory = input("Inser the directory to download all the images: ")
pdfDirectory = input("Insert the directory to move the pdf to: ")
volLink = input("Insert the volume's link: ")
volNumber = input("Insert the volume Number: ")
nPages = input('Insert the number of pages in the volume: ')


os.system("clear")
print("\n")

print("Are all the informations correct? ")
print("Images's direcotry:",directory)
print("Pdf's direcoty:",pdfDirectory)
print("The volume's link:",volLink)
print("The volume number is:",volNumber)

answer = input("[y/n] ")

if answer == "n":
    quit()

else:
    driver.get(volLink)
    time.sleep(15)

    for i in range(int(nPages)+1): #adds one so it overshoots the user input to make sure
        i+=1
        time.sleep(5)

        try: #Adds the link of each page to the imgLinks list
            imgLinks.append(driver.find_element_by_xpath(imagexPath%(i)).get_attribute('src'))

        except:#Print the number of the page it encounterred an error
            print(colored("[ERROR] Failed to get the link for the "+str(i)+" page",'red'))
            continue

    print("Gathered all the link, moving to "+directory)
    os.chdir(directory) #move to the directory specified by the user to save the images

    for link in imgLinks: #goes through each page/image link


    #counter < 10 because from 0-9 the name is 00x.JPEG, but from 10 onward it's 0x.JPEG ->where x is the number of the page (to make sure the order is correct when making the pdf)
        if counter < 10:
            response = requests.get(link)

            with open("00%s.JPEG"%(counter),'wb') as image:#Creates a .JPEG file and downloads the image from the link
                image.write(response.content)

        if counter >= 10:
            response = requests.get(link)

            with open("0%s.JPEG"%(counter),'wb') as image:

                image.write(response.content)


        counter+=1

    try:
        if int(volNumber) < 10:
            os.chdir(pdfDirectory)
            os.system("convert *.JPEG Vol.00%s.pdf"%(volNumber))

        else:
            os.chdir(pdfDirectory)
            os.system("convert *.JPEG Vol.0%s.pdf"%(volNumber))

    except:
        print(colored("[ERROR] Could not change to the finale/pdf directory",'red'))
