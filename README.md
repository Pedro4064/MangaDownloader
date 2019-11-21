# MangaDownloader

## [Manga.py](Manga.py)
•Download and make PDFs from mangas from [KissManga](https://kissmanga.com/).<br/>
•You can determine the first and last chapter you wish to download.

![Main prompt](https://github.com/Pedro4064/mDownloader/blob/master/Images/Main.png?raw=true)
![-h as an argument](https://github.com/Pedro4064/mDownloader/blob/master/Images/-h.png?raw=true)

## [dailyCheck.py](https://github.com/Pedro4064/MangaDownloader/blob/master/Raspberry%20Pi%20Daily%20check/dailyCheck.py)
•Set a raspberry pi to check every day for new volumes, download them, make a pdf and send to kindle/email automatically.<br/>
•It uses a [json file](https://github.com/Pedro4064/MangaDownloader/blob/develop/Raspberry%20Pi%20Daily%20check/manga.json) to get the last volume's info and update it once it downloades the latest chapter.<br/>

•The json file has the following structure:


|title|mainURL|lastURL|
|-----|-------|-------|



example-> [manga.json](https://github.com/Pedro4064/MangaDownloader/blob/develop/Raspberry%20Pi%20Daily%20check/manga.json)


## Modules

### Python
  •To install all modules run: <br/>
   `python -m pip install -r /path/to/requirements.txt`<br/>
   
-[requirements.txt](requirements.txt)

#### Preinstalled
•os<br/>
•time<br/>
•jsons<br/>
•requests<br/>

#### Needs to be installed separately  
•[termcolor](https://pypi.org/project/termcolor/)<br/>
•[selenium](https://pypi.org/project/selenium/)<br/>
•[requests](https://pypi.org/project/requests/2.7.0/)<br/>


## Chrome Driver

  •You also need to download [chromedriver](http://chromedriver.chromium.org/downloads) to use with selenium module.<br/>
  *If you are on the raspberry pi, follow this [instructions](https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/). <br/>
### Unix based System			
•[Imagemagick ](https://imagemagick.org/index.php)<br/>
	-> Or using the terminal:
	`sudo apt install imagemagick`<br/>



## Notes
-Change the `driverPath = '/Applications/chromedriver'` to fit the location of the webDriver in your system.<br/>
-Make sure you have installed all the necessary libraries.<br/>
-If you are on windows, you will need to change the bash commands to their equivalent on your system. You will also need to download and install Imagemagick separately.