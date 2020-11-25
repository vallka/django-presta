import re
import requests

import logging
logger = logging.getLogger(__name__)

from django.shortcuts import redirect

# Create your views here.
def ig_image(request):
    id=request.GET['id']

    url = ''

    logger.error("ig_image - id:%s",id)
    img = f'https://www.instagram.com/p/{id}/'
    try:
        page = requests.get(img, allow_redirects=True)

        data = re.search(r'window\._sharedData\s*=\s*(\{.*?\});<',page.text)
        url = re.search(r'"display_url":"(https://.*?)"',data[1])
        url = url[1].replace(r'\u0026','&')
        print(url)
        logger.error("ig_image - url:%s",url)

    except Exception as e:
        logger.error(e)
        pass


    return redirect(url)