from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema


from .models import *

import logging
logger = logging.getLogger(__name__)


class MyUploadView(APIView):
    parser_class = (JSONParser,)

    @swagger_auto_schema(operation_description="description")
    def post(self, request, format=None):

        obj = request.data

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
            

        logger.error("DONE - %s! - %s",'MyUploadView')




        return Response({'status': 'OK'})
