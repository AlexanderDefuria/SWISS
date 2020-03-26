from PIL import Image
from django.conf import settings
import sys
import os


path = os.path.join(os.curdir, str(sys.argv[1]))
colorImage = Image.open(path)
transposed = colorImage.transpose(Image.ROTATE_90)
transposed.save(path, "PNG")

