import urllib.request
from bing_image_urls import bing_image_urls
from PIL import Image


def image_url(name: str) -> 'image_url':
    return bing_image_urls(name, page_counter=1)


def img_download(url: str, name: str) -> 'JPEG':
    img = urllib.request.urlopen(url).read()
    out = open('photo/'+name+'.JPEG', 'wb')
    out.write(img)
    out.close()
    im = Image.open('photo/'+name+'.JPEG', 'r')
    im_resized = im.resize((48, 48))
    im_resized.save('photo/'+name+'_thumb.JPEG')
