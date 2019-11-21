from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from termcolor import colored
import requests
import json
import time
import os


class kissManga(webdriver.Chrome,webdriver.chrome.options.Options,webdriver.common.by.By,webdriver.support.ui.WebDriverWait):

    def __init__(self, executable_path='/Applications/chromedriver'):

        self.executable_path = executable_path
        
        # Added the headless option 
        self.options = webdriver.chrome.options.Options()
        self.options.add_argument('--headless')

        # Initiate an instance of the webdriver class
        self.driver = webdriver.Chrome(executable_path= self.executable_path, options=self.options)

        # The wait for elements config -> 10 seconds
        self.wait = webdriver.support.ui.WebDriverWait(self.driver,10)
  
    def close_webdriver(self):

        # close the webdriver
        self.driver.quit()

    def __wait_for_element(self,element_xPath:'xPath for element'):        
        # Private method, to be used only by other methods of class, not by users

        try:
            ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, element_xPath)))

            # If the driver finds the element in the time limit, return true, else return false
            return True
        
        except:
            return False

    def get_chapters(self,main_url:'The Url from the main page of the manga',number_of_chapters:'Rough estimate of the number of chapters'):

        loaded = False
        chapters = []

        # while the site does not load fully, retry every 10 seconds
        while loaded == False:
                
            # Go to the specified url
            self.driver.get(main_url)

            # wait for the first element to load, if it does not load, retry
            if self.__wait_for_element('//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[3]/td[1]/a'):
                loaded = True

            else:
                print('Retrying')

        # Once the webpage fully loaded, get the url and name of chapters (number of chapters + 50 to make sure it gets al the urls)
        

        # Make an iterable object for the FOR loop, It starts at 3 because the site's xPaths do so
        chapter_number = range(3,number_of_chapters+51)

        # The quintessential xPath 
        base_xpath = '//*[@id="leftside"]/div[2]/div[2]/div[2]/table/tbody/tr[%d]/td[1]/a'

        # Iterate reversed because the first title actually has the largest number, and the latest volume has 3(the lowest),  so it returs a list in the released order
        for i in reversed(chapter_number):

            try:

                xpath = base_xpath %(i)

                # Find the element
                element = self.driver.find_element_by_xpath(xpath)

                # get the title
                title = element.get_attribute('title').replace('Read ', '').replace(' online', '')

                # Get the url for the chapter
                url = element.get_attribute('href')

                # Make a dictionary out of the info
                chapter_info = {'title':title, 'url':url}

                # Add the dictionary to the chapters list
                chapters.append(chapter_info)
              
            except:

                continue
            
            
        # return the list with the data
        return chapters

    def download_pages(self, chapter_data:'json data containing its title and url', average_page_number):

        # Parse the json data
        title = chapter_data.get('title')
        main_url = chapter_data.get('url')

        pages = []
        loaded = False
        base_xPath = '//*[@id="divImage"]/p[%d]/img'

        # Try to go to the url, if it takes too long retry
        while loaded == False:

            # Go to the url 
            self.driver.get(main_url)

            # wait for the first page to load, if it does, exit the loop
            if self.__wait_for_element('//*[@id="divImage"]/p[1]/img'):
                loaded = True

        # Wait for 3 seconds to make sure the other pages will load as well
        time.sleep(3)

        # Tries to get the average number page for the series +50 pages 
        number_of_pages = average_page_number+50

        # Get the url for each page
        for page in range(number_of_pages):
            
            # Try to find the element
            try:
                element = self.driver.find_element_by_xpath(base_xPath %(page))
                page_url = element.get_attribute('src')
                pages.append(page_url)
                
                print(page_url)
            
            except:
                continue


        # Download all the pages 
        for page_number,url in enumerate(pages):

            # format the the file name
            if page_number<10:
                page_file = '00'+str(page_number)+'.png'

            elif page_number<100:
                page_file = '0'+str(page_number)+'.png'

            else:
                page_file = str(page_number)+'.png'
        

            # make a file to save the image -> wb = write binary
            with open(page_file, 'wb') as image:

                # make a get request
                request = requests.get(url)
                
                # save the content of the response in the file
                image.write(request.content)

        
        # make the pdf
        command = 'convert *.png '+'"'+ title+'"'+ '.pdf'
        os.system(command)
        print('\n\n\n\nPDF DONE\n\n\n\n')

        # return the name of the pdf file, it will be moved to the correct directory
        return title+'.pdf'
    
    def download_chapters(self,chapters_data,directory,average_page_number,series_name,starting_chapter = None ,last_chapter = None):

        # starting_chapters -> the title of the chapter you want to start the download 
        # last_chapter -> the title of the last chapter you wnat to download
        
        # If none of the above is specified, they are the first and last chapter in the series   
        if starting_chapter == None:
            starting_chapter = chapters_data[0]['title']

        if last_chapter == None:
            last_chapter = chapters_data[-1]['title']

        
        print('1-',starting_chapter,'2-',last_chapter)

        # get the position of the first and last chapter in the data
        positions = [position for position,manga in enumerate(chapters_data) if manga.get('title') == starting_chapter or manga.get('title') == last_chapter]

        print(json.dumps(positions, indent=4))
        

        # create a sublist made up of only the chapters wanted
        formatted_data = [data for position,data in enumerate(chapters_data) if position >= int(positions[0]) and position<= int(positions[1])]

        print(json.dumps(formatted_data,indent=4))

        # Change to the desired directory
        os.chdir(directory)

        # Create 2 new directories, one for the finished pdfs and another for the raw images
        raw_directory = directory+'/raw_images'
        pdf_directory = directory+'/pdf_directory'

        # try, if it exists just continue
        try:
            os.mkdir(raw_directory)
            os.mkdir(pdf_directory)
        
        except:
            print(colored('Directory already exists', 'yellow'))
            pass

        # Change to raw_directory
        os.chdir(raw_directory)

        # Make a directory for each chapter and download it
        for chapter in formatted_data:

            message = 'Downloadign '+chapter.get('title')+'\n\n\n'
            print(colored(message, 'green'))

            # make a directory with the chapter's name 
            target_directory = chapter.get('title')
            
            # try, if it exists just continue
            try:
                os.mkdir(target_directory)
            except:
                print(colored('Directory already exists', 'yellow'))

            # change to it
            os.chdir(target_directory)
                   

            # Download the chapter
            new_pdf = self.download_pages(chapter_data =  chapter, average_page_number = average_page_number)

            # move the pdf to the pdf_directory
            command = 'mv '+'"'+new_pdf+'"'+' '+pdf_directory 
            os.system(command)

            # Go back to the raw_directory
            os.chdir(raw_directory)

 
# print the logo
def logo():
    print('              ____                      __                __         \n   ____ ___  / __ \____ _      ______  / /___  ____ _____/ /__  _____\n  / __ `__ \/ / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/\n / / / / / / /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    \n/_/ /_/ /_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     \n')

def komiLogo():

    komi = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣶⣶⣦⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⣻⣽⣿⣿⣿⣿⣿⣿⡿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠋⣸⣿⣿⣿⣿⣿⣿⠟⠁⢀⣿⣿⡀⣟⣿⣿⣿⠿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⢋⣾⣾⣿⣿⣯⡿⣽⡟⠁⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣼⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⣾⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠙⣟⢿⣿⣿⣿⣿⣿⣿⡌⠿⣿⣿⣿⣿⣿⡷⣦⣄⢹⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    All Done!!!!            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⠏⠀⡠⠖⠛⠉⠉⠙⠛⠦⠀⠈⠙⠛⠛⠿⠛⠛⠉⠉⠛⠛⢿⣧⠘⣿⣿⣿⡏⡀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⡟⠀⠞⠀⢀⣴⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⣿⣶⡀⠀⠹⡄⢸⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠩⠛⢿⣿⣿⣇⠀⠀⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢹⣿⣿⡏⠁⠀⠀⠀⠙⠛⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⡈⠙⠛⠛⠋⠀⠀⠀⠀⠀⠈⣠⣄⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣼⣿⣿⡇⠀⠀⠀⠁⠒⠀⠀⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠒⠈⠀⠀⠀⠀⣐⠀⠁⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠊⣀⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⡇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⡄⠀⠀⠀⣠⣤⣶⣾⣿⣿⣿⣿⣿⣿⡿⢃⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣤⣄⡿⠁⣿⠛⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣛⣻⣏⣁⢸⠸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⣸⣿⣿⣿⣿⣿⣿⣿⡟⠁⡇⠀⠀⠀⣿⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣾⡄⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣧⣿⣿⣿⣿⠿⠿⢛⠏⠀⠀⠸⡀⠀⢠⠇⠀⠀⠹⡛⠻⠿⣿⣿⣿⣿⣿⣷⠸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠛⠋⠉⠀⠀⠀⡌⠀⠀⠀⠀⠳⣀⠏⢀⠀⠀⠀⢱⠀⠀⠀⠈⠉⠛⣿⣿⡆⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣧⠂⠀⠀⠀⠀⣜⡠⣴⣶⢥⣍⠲⡋⠒⣡⣼⣳⢢⣄⣣⠀⠀⠀⠀⠀⠘⣿⣷⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⡘⡀⠀⠀⠀⢠⢣⢣⢿⣏⣞⣿⣹⡿⣽⣻⣻⣣⢻⡇⠀⠀⠀⢠⠁⠀⢹⣿⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠷⠥⡀⠀⠀⠘⡞⡎⡞⣟⡿⡟⠉⢿⣷⣣⢧⢻⣻⠁⠀⠀⢀⠂⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

    print(komi)
   
if __name__ == '__main__':

    # prompt the user for input
    os.system('clear')
    logo()
    
    print('\n\n')

    main_url = input('•The main Url - ')
    n_chapters = int(input('•An Estimate of the number of chapters - '))
    n_pages = int(input('•An average number of pages per chapter - '))
    s_name = input('•The manga name - ')
    f_chapter = input('•The chapter you want to start the download from (enter ⏎ if you want to start from the first one) - ')
    l_chapter = input('•The last chapter you want download (enter ⏎ if you want to download up until the last one) - ')
    d_path = input('•The directory you wish to save the files - ')

    # Check to see if any chapters were passed, if no, make the variables None
    if f_chapter == '':
        f_chapter = None
    
    if l_chapter == '':
        l_chapter = None

    manga = kissManga()
    chapters = manga.get_chapters(main_url=main_url, number_of_chapters=n_chapters)
    
    # print(json.dumps(chapters, indent=4))

    manga.download_chapters(chapters_data = chapters, directory = d_path, average_page_number = n_pages, series_name= s_name, starting_chapter=f_chapter,last_chapter=l_chapter)

    # clean up
    manga.close_webdriver()

    komiLogo()