import os
import sys
from termcolor import colored

if sys.argv[1] == '-h':
    print(colored('The first argument is the directory where all the PDFs are in and the number of PDFs in it','yellow'))
    print(colored('ex: python3.7 renamePDF.py /Volumes/Pedro_Ext/Manga/PDFs/Miss_Kobaiashy 80','yellow'))
    quit()

#Change to the correct directory
os.chdir(sys.argv[1])

for i in range(int(sys.argv[2])):

    i+=1
    
    if i == 1:
        continue

    if i < 10:

        os.system('mv Vol.%d.pdf "Miss kobayashi dragon maid Vol.00%d.pdf" ' %(i,i))

    if i >= 10 and i<100:
        os.system('mv Vol.%d.pdf "Miss kobayashi dragon maid Vol.0%d.pdf" ' %(i,i))
