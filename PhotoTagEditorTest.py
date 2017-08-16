import piexif
import os

from os.path import join

taglist = {}
arraytags = []
separator=";"
for root, dirs, files in os.walk(r'C:\Users\Olivier\Pictures\Test'):
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
            exif_dict['0th'][270] = 'This is a description'
            exif_dict['0th'][315] = 'Artist is Olivier KORACH'
            exif_dict['0th'][33432] = '(c) Olivier Korach 2017'
            #exif_dict['0th'][40091] = 'XPTitle Floridaaaaa'
            #exif_dict['0th'][40094] = 'XPKeywords,Olivier,Floride,Vacances'
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, file)

            for ifd in ("0th", "Exif", "GPS", "1st"):
                for tag in exif_dict[ifd]:
                    taglist[piexif.TAGS[ifd][tag]["name"]] = 1
                    #checktaglist = [ 'ImageDescription', 'Artist', 'Copyright', 'XPComment', 'XPTitle', 'XPKeywords' ]
                    #for checktag in checktaglist:
                    #    if piexif.TAGS[ifd][tag]["name"] == checktag:
                    #        print (checktag, ' in ', ifd, ' id ', tag)

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
for tag in taglist:
    print(tag, end=separator)
    print("")

    for filetags in arraytags:
        print(filetags["filename"], end=separator)
        for tag in taglist:
            if tag in filetags.keys():
                print(filetags[tag], end=separator)
                else:
                print('', end=separator)
            print("")