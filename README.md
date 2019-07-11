# mDownloader
•Download and make PDFs from mangas from [KissManga](https://kissmanga.com/)
•Set a raspberry pi to check every day for new volumes, download, make pdf and send to kindle/email automatically
•It only works on Unix based systems
## Modules

### Python

#### Preinstalled
•os<br/>
•time<br/>
•sys<br/>
•requests<br/>

#### Needs to be installed separately  
•[termcolor](https://pypi.org/project/termcolor/)<br/>
•[selenium](https://pypi.org/project/selenium/)<br/>
•[progressBar](https://progressbar-2.readthedocs.io/en/latest/installation.html)<br/>

obs-> You also need to download [chromedriver](http://chromedriver.chromium.org/downloads)<br/><br/>
			If you are on the raspberry pi, follow this [instructions](https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/) <br/>

### Unix based System			
•[Imagemagick ](https://imagemagick.org/index.php)<br/>
	-> Or using the terminal:
	`sudo apt install imagemagick`<br/>



## Notes
	-Make sure you have installed all the necessary libraries
	-It only works on UNIX based systems(macosx/linux), although you can change the bash commands to the equivalent prompt commads for Windos
