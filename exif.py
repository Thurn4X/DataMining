from PIL import Image
from PIL.ExifTags import TAGS

imgfile = Image.open("imgtest.jpg")
exif_data = imgfile._getexif()

if exif_data:  # s'il existe des informations EXIF
    for tag, value in exif_data.items():
        if tag in TAGS:
            print(TAGS[tag], value)