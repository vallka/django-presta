from datetime import datetime, timedelta
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
    help = 'instagrab'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print (self.help)
        logger.info(self.help)

        today = datetime.today().date() # get a Date object
        logger.info(today)

        headers = {
            'User-Agent': get_random_ua(),
        }

        tag_url = 'https://www.instagram.com/explore/tags/gellifique/'

        r = requests.get(tag_url,headers)

        with open('instagrab_gellifique.html', 'w') as outfile:
            outfile.write(r.text)

        js = re.search(r'window\._sharedData\s*=\s*([^<]*)',r.text)

        js = js.group(1).strip(' ;')

        obj=json.loads(js)

        with open('instagrab_gellifique.json', 'w') as outfile:
            json.dump(obj, outfile)

        nodes = obj['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']
        print(len(nodes))

        for n in nodes:
            print (n['node']['id'])
            print (n['node']['owner']['id'])
            print (n['node']['shortcode'])
            print (n['node']['edge_liked_by']['count'])
            print (n['node']['taken_at_timestamp'])
            print (n['node']['is_video'])
            #print (n['node']['edge_media_to_caption']['edges'][0]['node']['text'])

            try:
                insta = InstagrabGellifiqueGelColour.objects.get(code = n['node']['shortcode'])

                if insta.like_count != n['node']['edge_liked_by']['count']:
                    insta.like_count = n['node']['edge_liked_by']['count']
                    insta.save()
                    logger.error('Updated '+n['node']['shortcode'])

            except InstagrabGellifiqueGelColour.DoesNotExist:
                insta = InstagrabGellifiqueGelColour(
                    taken_at = datetime.utcfromtimestamp(n['node']['taken_at_timestamp']),
                    username = '*',
                    userid = n['node']['owner']['id'],
                    code = n['node']['shortcode'],
                    caption = n['node']['edge_media_to_caption']['edges'][0]['node']['text'],
                    like_count = n['node']['edge_liked_by']['count'],
                    width = n['node']['dimensions']['width'],
                    height = n['node']['dimensions']['height'],
                    media_type = 2 if n['node']['is_video'] else 1,
                    products = '*',
                    created_dt = datetime.today(),
                )

                insta.save()
                logger.error('Added '+n['node']['shortcode'])
            

        logger.error("DONE - %s! - %s",self.help,str(today))






