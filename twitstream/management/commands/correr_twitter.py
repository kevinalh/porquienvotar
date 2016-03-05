# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

import tweepy
import json
from shapely.geometry import Point, Polygon
import logging
from unidecode import unidecode

from twitstream.models import Keyword, Tweet
from django.conf import settings

# Constantes
MIN_PUNTOS = 5
EXTRA_PUNTOS = 2


class Command(BaseCommand):
    help = "Runs the streaming_candidatos script"

    def handle(self, *args, **options):

        class CandidatosStreamListener(tweepy.StreamListener):

            def guardar_db(self, status, puntos_tweet, de_peru_bool):
                tweet, _ = Tweet.objects.get_or_create(text=status.text, id_str=status.id_str,
                                                       user_id_str=status.user.id_str,
                                                       puntos=puntos_tweet,
                                                       de_peru=de_peru_bool)
                tweet.save()

            def verificar_coordenadas(self, status):
                try:
                    coordenadas = status.coordinates.coordinates
                except AttributeError:
                    return False
                else:
                    punto = Point(coordenadas[0], coordenadas[1])
                    if peru_polygon.contains(punto):
                        return True
                    else:
                        return False

            def lugar(self, status):
                try:
                    pais = status.place.country_code
                except AttributeError:
                    return False
                else:
                    return True if pais == 'PE' else False

            def on_status(self, status):

                # print(str(status.text).encode("utf-8"))
                puntos = 0
                de_peru = False
                for keyword in keywords:
                    if unidecode(keyword.key.lower()) in status.text.lower():
                        puntos += keyword.puntos
                if self.verificar_coordenadas(status) or self.lugar(status):
                    puntos += EXTRA_PUNTOS
                    de_peru = True
                if puntos >= MIN_PUNTOS:
                    self.guardar_db(status, puntos, de_peru)

            def on_error(self, status):
                logger = logging.getLogger(__name__)
                logger.critical(status)

        PERU = json.load(open('twitstream/peru.json', 'r'))
        peru_polygon = Polygon(PERU)
        keywords = Keyword.objects.all()
        keywords_filtro = keywords.filter(para_filtro=True)
        track_list = [keyword.key for keyword in keywords_filtro]

        # Autorizacion y llamando a stream
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        api = tweepy.API(auth)

        # Filtros
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
        myStreamCandidatos = CandidatosStreamListener()
        myStream = tweepy.Stream(auth=api.auth, listener=myStreamCandidatos)

        # Activando stream
        myStream.filter(track=track_list, languages=['es'])
