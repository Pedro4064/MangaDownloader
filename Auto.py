from selenium import webdriver
from progress.bar import IncrementalBar
from termcolor import colored
import requests
import time
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


volLinks = []
imgLinks = []
error = []


#Link of the mainpage(with all the other links)
xPath  = '//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[%s]/td[1]/a'
imagexPath = '//*[@id="divImage"]/p[%s]/img'
imageName = '%s.JPEG'

counter = 0  #To keep track of the image files beeing created (goes back to 0 after the end of each volume)

#Specifies the google Chrome's driver directory
driver = webdriver.Chrome('/usr/local/bin/chromeDriver')

#prints the banner
print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')

mainLink = input('The main Link: ')
fCounter = int(input('The number of volumes: '))
nLinks = fCounter-1  #Changes according to the number of volumes...

print('\n')

#Go to webPage
driver.get(mainLink)
time.sleep(15) #Wait for it to load

#Creats a progress bar so the user can check progress
volBar = IncrementalBar('Gathering the links for all volumes', max = nLinks)

#Get the links for the volumes on the main page
for i in range(nLinks):

    i+=3 #The counter in the site starts at 3... Depends on the series I think
    volLinks.append(driver.find_element_by_xpath(xPath%(i)).get_attribute('href'))
    volBar.next()#updates the progress bar

print("All the volumes' links were collected. Initializing downloads...")
time.sleep(2)

os.system('clear')
print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')


downloadBar = IncrementalBar('Donwloading volumes: ',max = len(volLinks))

#Goes link by link (that was obtained from the main page of the series)
for link in volLinks:
    print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')


    try:
        driver.get(link)
        time.sleep(15)  #Wait for it to load
        linkBar = IncrementalBar('Gathering the image links', max = 30)

        for i in range(30): #tries to get 30 links ->change so it overshoots the number of pages ----> Change the linkBar max if the 30 is altered

            time.sleep(1)
            i+=1

            try:
                imgLinks.append(driver.find_element_by_xpath(imagexPath%(i)).get_attribute('src'))
                #update the progress bar
                linkBar.next()
            except:
                #update the progress bar
                linkBar.next()
                continue



        #Change to the correct directory
        os.chdir('/Volumes/Pedro_Ext/Manga/Miss_Kobaiashi') #Change the destination for other series
        os.system('mkdir Vol.%s'%(fCounter))#The number of the volume (from the latest to the oldest -> decreasing )
        os.chdir('Vol.%s'%(fCounter))
        fCounter-=1 #The number of the volume (from the latest to the oldest -> decreasing )

        print('\n')
        imageBar = IncrementalBar('Downloading the images',max = len(imgLinks))

        #Downloads the imageLinks
        for image_link in imgLinks:

            counter+=1
            response = requests.get(image_link)
            time.sleep(2) #Waits 2 seconds just to be sure

            #Creates a file and downloads the images
            with open(imageName%(counter),'wb') as image:
                image.write(response.content)

            #updates the progress bar
            imageBar.next()


        counter = 0  #Cleans the counter  for the next vol of the series --->Comment this line if you want to make one big volume
        imgLinks = []#cleans the imgLinks list for the next volume

        #Goes to the next volLink...

    except:
        error.append(link)
        driver.quit()   #Closes the dirver and summons it againf to prevent future failures
        driver = webdriver.Chrome('/usr/local/bin/chromeDriver')

    #clears the screen/updates the progress bar
    os.system('clear')
    downloadBar.next()

#Prints the failed downloads (if any)
if len(error) != 0:

    print('\n')
    print(colored("[ERROR] Unable to download the folowing volumes: ",'red'))
    for link in error:
        print('•',link)
