import os
import sys
from termcolor import colored

#########################################################################
#Change:
#   directory -> to were the image folders are
#   nVolumes  -> to the number of Volumes
#   The bash command on line 29 -> to the direcoty you wish to send the finished PDF
#
#Needs:
#   imagemagick -> for all unix systems (download with homeBrew)
#########################################################################
if sys.argv[1] == '-h':
    print(colored('The first argument is the directory were all the image folders are and the second one is the number of volumes/direcotries inside it.\n\n ex: python3.7 AutoPDF.py /Volumes/Pedro_Ext/Manga/PDFs/Miss_Kobaiashy 80','yellow'))
    quit()


directory = sys.argv[1]
name = "Vol."
nVolumes = sys.argv[2]

os.chdir(directory)

if sys.argv[1] == '-h':
    print('The first argument is the directory were all the image folders are and the second one is the number of volumes/direcotries inside it')
for i in range(nVolumes):
    i+=1

    os.chdir(directory+"/"+name+str(i))

    print("Changing to:",directory+"/"+name+str(i))

    os.system("convert *.JPEG Vol.%s.pdf"%(str(i)))
    os.system("mv Vol.%s.pdf /Volumes/Pedro_Ext/Manga/PDFs/Miss_Kobaiashy"%(str(i)))
