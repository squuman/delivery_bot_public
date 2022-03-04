from pyzbar.pyzbar import decode
from PIL import Image


def read_barcode(photo_path):
    img = Image.open(photo_path)
    res = decode(img)
    if res:
        return res[0]
    else:
        return False
