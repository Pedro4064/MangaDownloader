from selenium import webdriver
from fpdf import FPDF
import requests
import time
import os

################################################################################

#Change:
#   fCounter -> The number of volumes = (number of last volume - number of first volume + 1)
#   nLinks (Depending on the series you want to download and the number of volumes/links on the main page) -> The number of volumes = (number of last volume - number of first volume + 1) and add 3 (The site adds 3 to the xPath for the links...)
#   The diecotry on line 72 for the correct one you want to add the child direcotris and .JPEGs -> To get the full directory path go to it on the terminal and enter "pwd"
#   mainLink -> To the link for the main page of the series you wish to download
#
#Observations:
#   Check the number of pages of all the volumes downloaded
#   Check the number of pages from the volumes to be downloaded and change the range of the for loop to more than necessary  to be sure (The current number is 60 pages)
#   WORKS ONLY WITH THE KISSMANGA SITE -> https://kissmanga.com/

################################################################################


volLinks = []
imgLinks = []


#Link of the mainpage(with all the other links)
mainLink = "https://kissmanga.com/Manga/Go-Toubun-no-Hanayome"
xPath  = '//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[%s]/td[1]/a'
imagexPath = '//*[@id="divImage"]/p[%s]/img'
imageName = '%s.JPEG'

nLinks = 73  #Changes according to the number of volumes... have to see by trieland error
nPages = 0   #Check once on the Volume Page
counter = 0  #To keep track of the image files beeing created (goes back to 0 after the end of each volume)
fCounter =71 #Kepp track of the directories beeing created

driver = webdriver.Chrome('/usr/local/bin/chromeDriver')


#Go to webPage
driver.get(mainLink)
time.sleep(15) #Wait for it to load

#Get the links for the volumes on the main page
for i in range(nLinks):
    i+=3 #The counter in the site starts at 3... Depends on the series I think

    volLinks.append(driver.find_element_by_xpath(xPath%(i)).get_attribute('href'))


#Goes link by link (that was obtained from the main page of the series)
for link in volLinks:


    try:
        driver.get(link)
        time.sleep(15)  #Wait for it to load

        for i in range(60): #tries to get 60 links

            time.sleep(2)
            i+=1

            try:
                imgLinks.append(driver.find_element_by_xpath(imagexPath%(i)).get_attribute('src'))
            except:
                continue


        #Change to the correct directory
        os.chdir('/Volumes/Pedro_Ext/TEST') #Change the destination for other series
        os.system('mkdir Vol.%s'%(fCounter))
        os.chdir('Vol.%s'%(fCounter))
        fCounter-=1

        #Downloads the imageLinks
        for link in imgLinks:

            counter+=1
            response = requests.get(link)
            time.sleep(2)#Waits 2 seconds just to be sure

            #Creates a file and downloads the images
            with open(imageName%(counter),'wb') as image:
                image.write(response.content)

        counter = 0  #Cleans the counter  for the next vol of the series
        imgLinks = []#cleans the imgLinks list for the next volume

        #Goes to the next volLink...

    except:
        print("Failed to get Manga:",link)
        driver.quit()   #Closes the dirver and summons it againf to prevent future failures
        driver = webdriver.Chrome('/usr/local/bin/chromeDriver')
