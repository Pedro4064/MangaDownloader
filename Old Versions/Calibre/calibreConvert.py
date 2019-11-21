import os
from termcolor import colored


def CalibreConvert():

    #macOSX only
    calibrePath = '/Applications/calibre.app/Contents/console.app/Contents/MacOS/'

    #file to boot to be converted -> path where you want the conversion to be in(+ name)
    convertFormula = './ebook-convert %s %s '
    #./ebook-convert /Users/pedrocruz/Desktop/e-books/PDFs/"Le-Morte-dArthur.pdf" /Users/pedrocruz/Desktop/e-books/PDFs/"Le-Morte-dArthur.mobi"

    #The path to the converted book, the Author of the book
    metaDataFormula = './ebook-convert %s -a "%s" '
    #./ebook-convert /Users/pedrocruz/Desktop/e-books/PDFs/"Le-Morte-dArthur.pdf" /Users/pedrocruz/Desktop/e-books/PDFs/"Le-Morte-dArthur.mobi"


    print(' ________  ________  ___       ___  ________  ________  _______      \n|\\   ____\\|\\   __  \\|\\  \\     |\\  \\|\\   __  \\|\\   __  \\|\\  ___ \\     \n\\ \\  \\___|\\ \\  \\|\\  \\ \\  \\    \\ \\  \\ \\  \\|\\ /\\ \\  \\|\\  \\ \\   __/|    \n \\ \\  \\    \\ \\   __  \\ \\  \\    \\ \\  \\ \\   __  \\ \\   _  _\\ \\  \\_|/__  \n  \\ \\  \\____\\ \\  \\ \\  \\ \\  \\____\\ \\  \\ \\  \\|\\  \\ \\  \\\\  \\\\ \\  \\_|\\ \\ \n   \\ \\_______\\ \\__\\ \\__\\ \\_______\\ \\__\\ \\_______\\ \\__\\\\ _\\\\ \\_______\\\n    \\|_______|\\|__|\\|__|\\|_______|\\|__|\\|_______|\\|__|\\|__|\\|_______|\n                                                                    \n\n')

    bookPath = input('The path to the book-> ')
    conversionPath = input('The desired path for the conversion+"name" -> ')
    author = input('The author of the Book-> ')

    #Changes to the directory where the calibre tools are
    os.chdir(calibrePath)

    #Issue the convert command 
    os.system(convertFormula %(bookPath,conversionPath))
    os.system(metaDataFormula %(conversionPath,author))




while True:

    CalibreConvert()
    answer = input('')

    if answer == 'q':
        quit()
