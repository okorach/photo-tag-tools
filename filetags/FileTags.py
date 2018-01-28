#!python3


class TagError(Exception):
    pass


class UnknownTagError(TagError):
    pass


class FileTags:

    EXIF_SECTIONS = ("0th", "Exif", "GPS", "1st")  # To do, go through all possible exif_dict keys

    TAGS = {
        'Description': ('0th', 270),
        'Author': ('0th', 315),
        'DateTime': ('0th', 0),
        'Copyright': ('0th', 33432),
        'XPTitle': ('0th', 40091),
        'XPKeywords': ('0th', 40094)
    }
    # exif_dict['0th'][40091] = 'XPTitle Floridaaaaa'
    # exif_dict['0th'][40094] = 'XPKeywords,Olivier,Floride,Vacances'

    def __init__(self, filename):
        self.filename = filename
        self.flat_tags = {}
        self.exif_dict = {}

    def read(self):
        self.exif_dict = piexif.load(self.filename)

    def write(self):
        if self.exif_dict != {}:
            exif_bytes = piexif.dump(self.exif_dict)
            piexif.insert(exif_bytes, file)

    def flatten_tags(self):
        self.flat_tags = []
        self.flat_tags['filename'] = self.filename
        for ifd in FileTags.EXIF_SECTIONS:
            for tag in self.exif_dict[ifd]:
                data = self.exif_dict[ifd][tag]
                if type(data) is bytes:
                    data = data.replace(b"\x00", b"")
                    try:
                        data = data.decode()
                    except UnicodeDecodeError:
                        pass
                self.flat_tags[piexif.TAGS[ifd][tag]["name"]] = data

    def get_flat_tags(self):
        self.flatten_tags()
        return self.flat_tags

    def get_exif_tags(self):
        return self.exif_dict

    def get_tag(self, tag_name):
        if tag_name in FileTags.TAGS.keys():
            return self.exif_dict[FileTags.TAGS[tag_name][0]][FileTags.TAGS[tag_name][1]]
        else:
            raise UnknownTagError

    def set_tag(self, tag_name, tag_value):
        if tag_name in FileTags.TAGS.keys():
            self.exif_dict[FileTags.TAGS[tag_name][0]][FileTags.TAGS[tag_name][1]] = tag_value
        else:
            raise UnknownTagError

    def get_date_picture_taken(self):
        return self.get_tag('DateTime')

    def set_date_picture_taken(self, datetime):
        return self.set_tag('DateTime', datetime)

    def get_author(self):
        return self.get_tag('Artist')

    def set_author(self, author):
        return self.set_tag('Artist', author)

    def get_copyright(self):
        return self.get_tag('Copyright')

    def set_copyright(self, rights):
        self.set_tag('Copyright', rights)

    def get_windows_keywords(self):
        return self.get_tag('XPKeywords')

    def get_tag_array(self):
        tag_array = []
        for ifd in FileTags.EXIF_SECTIONS:
            tag_array.append(self.exif_dict[ifd].keys())
        return tag_array

    def get_tag_list(self):
        tag_dict = {}
        for ifd in FileTags.EXIF_SECTIONS:
            for tag in self.exif_dict[ifd]:
                tag_dict[piexif.TAGS[ifd][tag]["name"]] = 1
        return tag_dict

    def merge_tag_list(self, current_list):
        for ifd in FileTags.EXIF_SECTIONS:
            for tag in self.exif_dict[ifd]:
                current_list[piexif.TAGS[ifd][tag]["name"]] = 1
        return current_list
