# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import OperationalError
from django.utils.timezone import make_aware, utc
from django.db import connection

import tweepy
import time
import json
from shapely.geometry import Point, Polygon
import logging
from unidecode import unidecode

from twitstream.models import Keyword, Tweet

import socket
import sys

lock_socket = None

# Constantes
MIN_PUNTOS = 5
EXTRA_PUNTOS = 2


class Command(BaseCommand):
    help = "Corre el streaming sobre los keywords en la base de datos y guarda los que pasen el test"

    def handle(self, *args, **options):

        class CandidatosStreamListener(tweepy.StreamListener):

            def guardar_db(self, status, puntos_tweet, pais_alg, tiempo_creacion):
                tweet, _ = Tweet.objects.get_or_create(text=status.text, id_str=status.id_str,
                                                       user_id_str=status.user.id_str,
                                                       puntos=puntos_tweet,
                                                       created_at=tiempo_creacion,
                                                       pais=pais_alg)
                tweet.save()

            def verificar_coordenadas(self, status):
                try:
                    coordenadas = status.coordinates['coordinates']
                except TypeError:
                    return False
                else:
                    punto = Point(coordenadas[0], coordenadas[1])
                    if peru_polygon.contains(punto):
                        return "PE"
                    else:
                        return False

            def lugar(self, status):
                try:
                    pais = status.place.country_code
                except AttributeError:
                    return False
                else:
                    return pais

            def on_status(self, status):

                # print(str(status.text).encode("utf-8"))
                puntos = 0
                for keyword in keywords:
                    if unidecode(keyword.key.lower()) in unidecode(status.text.lower()):
                        puntos += keyword.puntos
                pais = self.lugar(status) or self.verificar_coordenadas(status)
                if pais is False:
                    pais = None
                else:
                    puntos += EXTRA_PUNTOS
                try:
                    ts = make_aware(status.created_at, utc)
                except:
                    ts = None
                if puntos >= MIN_PUNTOS:
                    self.guardar_db(status, puntos, pais, ts)

            def on_error(self, status):
                logger = logging.getLogger(__name__)
                error_twitter = "Twitter on_error codigo = {code}".format(code=status)
                logger.critical(error_twitter)
                print(error_twitter)
                time.sleep(20)
                if status == 420:
                    # returning False in on_data disconnects the stream
                    return False
                else:
                    return True

            def on_timeout(self):
                print("Twitter on_timeout")

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
        def correr_stream():
            try:
                myStream.filter(track=track_list, languages=['es'])
            except OperationalError:
                print("Operational Error!")
                connection.connection.close()
                connection.connection = None
                time.sleep(6)
                return correr_stream()

        def is_lock_free():
            global lock_socket
            lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            try:
                lock_id = "kevinalh.correr_twitter2"   # this should be unique. using your username as a prefix is a convention
                lock_socket.bind('\0' + lock_id)
                logging.debug("Acquired lock %r" % (lock_id,))
                return True
            except socket.error:
                # socket already locked, task must already be running
                logging.info("Failed to acquire lock %r" % (lock_id,))
                return False

        if not is_lock_free():
            sys.exit()
        else:
            correr_stream()
