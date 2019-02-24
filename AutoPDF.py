import os


#########################################################################
#Change:
#   directory -> to were the image folders are
#   nVolumes  -> to the number of Volumes
#   The bash command on line 28 -> to the direcoty you wish to send the finished PDF
#
#Needs:
#   imagemagick -> for all unix systems (download with homeBrew)
#########################################################################


directory = "/Volumes/Pedro_Ext/Manga/Quintessential Quintuplets"
name = "Vol."
nVolumes = 71

os.chdir(directory)

for i in range(nVolumes):
    i+=1

    os.chdir(directory+"/"+name+str(i))

    print("Changing to:",directory+"/"+name+str(i))

    os.system("convert *.JPEG Vol.%s.pdf"%(str(i)))
    os.system("mv Vol.%s.pdf /Volumes/Pedro_Ext/Manga/PDFs"%(str(i)))
