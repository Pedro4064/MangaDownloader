import os



#########################################################################
#Change:
#   directory -> to were the image folders are
#   nVolumes  -> to the number of Volumes
#   The range on line 29 (If the manga has more than 60 pages)
#########################################################################



directory = "/Volumes/Pedro_Ext/Manga/Miss_Kobaiashi"
name = ".JPEG"
nVolumes = 71

#Changes to the main direcotry
os.chdir(directory)

#Loops trough all the Vol files
for i in range(nVolumes):

    i+=1
    #Changes to the direcotry
    os.chdir(directory+"/Vol."+str(i))

    #Loops trough all the .JPEG (pages) of a volume and renames it
    for n in range(30):
        n+=1

        if n < 10:
            os.system("mv "+str(n)+name+" "+"00"+str(n)+name)

        else:
            os.system("mv "+str(n)+name+" "+"0"+str(n)+name)
