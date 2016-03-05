from django.core.management.base import BaseCommand
# import subprocess
import pdb


class Command(BaseCommand):
    help = "Runs the streaming_candidatos script"

    def handle(self, *args, **options):
        # cmd = 'python streaming_candidatos.py'
        # subprocess.Popen(cmd)
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

            def guardar_db(self, status, entra):
                pdb.set_trace()
                tweet, _ = Tweet.objects.get_or_create(text=status.text, id_str=status.id_str,
                                                       user_id_str=status.user.id_str)
                if entra:
                    tweet.entra = True
                tweet.save()

            def verificar_coordenadas(self, coordenadas):
                punto = Point(coordenadas[0], coordenadas[1])
                if peru_polygon.contains(punto):
                    return True
                else:
                    return False

            def on_status(self, status):

                def verificar_texto(texto, lista, es_lista_de_hashtags):
                    if texto:
                        if not es_lista_de_hashtags:
                            for x in lista:
                                if x.key in texto:
                                    pdb.set_trace()
                                    return True
                            return False
                        else:
                            for y in texto:
                                for x in lista:
                                    if y.key in texto:
                                        pdb.set_trace()
                                        return True
                            return False
                    else:
                        return False
                    # No funcionan por cuestiones de scope:
                    # return any(x.key in texto for x in lista)
                    # any(x.key in status.text for x in keywords_CS)
                    # any([x.key in status.entities.hashtags.text for x in keywords_hash])

                print(str(status.text).encode("utf-8"))
                keywords_CS = [x for x in keywords if x.seguridad == 'CS']
                keywords_hash = [x for x in keywords if x.hashtag is True and x.seguridad == 'S']
                try:
                    hashtags = status.entities.hashtags
                except AttributeError:
                    hashtags = False
                if (verificar_texto(status.text, keywords_CS, False) or
                        verificar_texto(hashtags, keywords_hash, True)):
                    self.guardar_db(status, True)
                '''
                    elif status.place or status.coordinates:
                        if status.place.country_code == 'PE' or self.verificar_coordenadas(status.coordinates.coordinates):
                            keywords_S = [x for x in keywords_candidato if x.seguridad == 'S']
                            keywords_hash = [x for x in keywords_candidato if x.hashtag is True and x.seguridad == 'N']
                            if any([x.key in status.text for x in keywords_S]) or any([x.key in status.entities.hashtags.text
                                                                                       for x in keywords_hash]):
                                self.guardar_db(status, True, candidato.id)
                            else:
                                self.guardar_db(status, False, 0)
                '''
            def on_error(self, status):
                logger = logging.getLogger(__name__)
                logger.critical(status)

        PERU = json.load(open('twitstream/peru.json', 'r'))
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
        myStream.filter(track=track_list, languages=['es'])
