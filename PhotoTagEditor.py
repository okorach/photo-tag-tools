import piexif
import os

taglist = {}
arraytags = []
separator=";"
for root, dirs, files in os.walk(r'C:\Users\Olivier\Pictures'):
    #print("Current directory", root)
    # print("Sub directories", dirs)

    for file in files:
        # file = r'C:\Users\Olivier\Pictures\Photos Floride\20160101_030907A.JPG'
        file = root + "\\" + file
        #print('-------------------------------------')
        #print(file)
        #print('-------------------------------------')

        filetags = {}

        try:
            filetags['filename'] = file
            exif_dict = piexif.load(file)
            for ifd in ("0th", "Exif", "GPS", "1st"):
                for tag in exif_dict[ifd]:
                    taglist[piexif.TAGS[ifd][tag]["name"]] = 1

            #for tag, val in taglist.items():
            #    print(tag, sep=',')
            #print('')

            for ifd in ("0th", "Exif", "GPS", "1st"):
                for tag in exif_dict[ifd]:
                    data = exif_dict[ifd][tag]
                    if type(data) is bytes:
                        data = data.replace(b"\x00", b"")
                        try:
                            data = data.decode()
                        except UnicodeDecodeError:
                            data = data
                    filetags[piexif.TAGS[ifd][tag]["name"]] = data
                    # print("%20s: %s" % (piexif.TAGS[ifd][tag]["name"],data))

            arraytags.append(filetags)

        except piexif.InvalidImageDataError:
            pass


print("Filename", end=separator)
for outtag in taglist:
    print(outtag, end=separator)
    print("")

    for filetags in arraytags:
        print(filetags["filename"], end=separator)
        for intag in taglist:
            if intag in filetags.keys():
                print(filetags[intag], end=separator)
            else:
                print('', end=separator)
            print("")
