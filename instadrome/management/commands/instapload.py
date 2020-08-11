from datetime import datetime, timedelta
import time
import requests
import re
import json

from django.core.management.base import BaseCommand, CommandError
from instadrome.models import *
from django.conf import settings

from instadrome.randomua import get_random_ua

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'instapload'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print (self.help)
        logger.info(self.help)

        today = datetime.today().date() # get a Date object
        logger.info(today)


        with open('instagrab_gellifique.json', 'r') as infile:
            obj=json.load(infile)
    
    
        #res = requests.post('http://localhost:8000/api/v1/upload/',json=obj)
        res = requests.post('https://www2.gellifique.co.uk/pypy/api/v1/upload/',json=obj)

        print(res)
        print(res.status_code)
        print(res.headers)
        print(res.text)

        logger.error("DONE - %s! - %s",self.help,str(today))






