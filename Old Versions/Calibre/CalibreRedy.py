import os

direcoty = "/Volumes/Pedro_Ext/Manga/PDFs/Quintenssetional Quintuplets PDF"

os.chdir(direcoty)

for i in range(71):
    i+=1
    if i < 10:

        os.system('mv "Quintessential Quintuplets(Vol.%s).pdf" "Quintessential Quintuplets(Vol.00%s).pdf"'%(str(i),str(i)))
    else:
        os.system('mv "Quintessential Quintuplets(Vol.%s).pdf" "Quintessential Quintuplets(Vol.0%s).pdf"'%(str(i),str(i)))
