# -*- coding: utf-8 -*-
import tweepy
import json
from shapely.geometry import Point, Polygon
import logging

from twitstream.models import Keyword, Tweet
from quiz.models import Candidato

from django.conf import settings

# auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)


class CandidatosStreamListener(tweepy.StreamListener):

    def guardar_db(self, status, entra, candidato_id):
        tweet = Tweet.objects.get_or_create(text=status.text, id_str=status.id_str, user_id_str=status.user_id_str)
        if entra:
            tweet.entra = True
            tweet.candidato_set.add(candidato_id)
        tweet.save()

    def verificar_coordenadas(self, coordenadas):
        punto = Point(coordenadas[0], coordenadas[1])
        if peru_polygon.contains(punto):
            return True
        else:
            return False

    def on_status(self, status):
        print(str(status.text).encode("utf-8"))
        for candidato in Candidato.objects.filter(entra_candidato=True):
            keywords_candidato = [x for x in keywords if x.candidato.id == candidato.id]
            keywords_CS = [x for x in keywords_candidato if x.seguridad == 'CS']
            keywords_hash = [x for x in keywords_candidato if x.hashtag is True and x.seguridad == 'S']
            if any([x.key in status.text for x in keywords_CS]) or any([x.key in status.entities.hashtags.text
                                                                        for x in keywords_hash]):
                self.guardar_db(status, True, candidato.id)
                continue
            elif status.place.country_code == 'PE' or self.verificar_coordenadas(status.coordinates.coordinates):
                keywords_S = [x for x in keywords_candidato if x.seguridad == 'S']
                keywords_hash = [x for x in keywords_candidato if x.hashtag is True and x.seguridad == 'N']
                if any([x.key in status.text for x in keywords_S]) or any([x.key in status.entities.hashtags.text
                                                                           for x in keywords_hash]):
                    self.guardar_db(status, True, candidato.id)
                else:
                    self.guardar_db(status, False, 0)

    def on_error(self, status):
        logger = logging.getLogger(__name__)
        logger.critical(status)

if __name__ == '__main__':
    PERU = json.load(open('peru.json', 'r'))
    peru_polygon = Polygon(PERU)
    keywords = Keyword.objects.all()
    track_list = [keyword.key for keyword in keywords]

    # Autorizacion y llamando a stream
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
    api = tweepy.API(auth)

    # Filtros
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    myStreamCandidatos = CandidatosStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamCandidatos)

    # Activando stream
    myStream.filter(track=track_list, language=['es'])
