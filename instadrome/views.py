import re
import requests

import logging
logger = logging.getLogger(__name__)

from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def ig_image(request):
    id=request.GET['id']

    url = ''

    logger.error("ig_image - id:%s",id)
    img = f'https://www.instagram.com/p/{id}/'

    text = img

    try:
        page = requests.get(img, allow_redirects=True)

        data = re.search(r'window\._sharedData\s*=\s*(\{.*?\});<',page.text)
        url = re.search(r'"display_url":"(https://.*?)"',data[1])
        url = url[1].replace(r'\u0026','&')
        print(url)

        text += "\n" + url

        logger.error("ig_image - url:%s",url)

    except Exception as e:
        logger.error(e)
        text += "\nError:" + e

    return HttpResponse(text)


    return redirect(url)