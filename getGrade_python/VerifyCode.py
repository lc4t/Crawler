from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import sys
import urllib
import urllib2

sys.path.append("pytesser")
import pytesser

class showVerifyCode:
    def __init__(self):
        self.imageURL = "http://www.afreesms.com/image.php?o=5336470415350050000"
        self.request = urllib2.Request(url = self.imageURL)
        self.opener = urllib2.build_opener()
        self.result = self.opener.open(self.request)
        print self.result.read()


test = showVerifyCode()