# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from twitstream.models import Tweet, Keyword
from quiz.models import Candidato

from unidecode import unidecode

import socket
import sys
import logging

lock_socket = None


class Command(BaseCommand):
    help = "Clasifica los tweets"

    def handle(self, *args, **options):

        def clasificar_tweet(tweet_object):
            candidatos = Candidato.objects.filter(entra_candidato=True)
            for x in candidatos:
                keywords_candidato = Keyword.objects.filter(candidato=x.id)
                for keyword in keywords_candidato:
                    if unidecode(keyword.key.lower()) in unidecode(tweet_object.text.lower()):
                        tweet_object.candidatos.add(x.id)
                        continue
            tweet_object.analizado = True
            tweet_object.save()

        def is_lock_free():
            global lock_socket
            lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            try:
                lock_id = "kevinalh.clasificar2"   # this should be unique
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
            tweets = Tweet.objects.filter(analizado=False)
            print(str(len(tweets)))
            for tweet in tweets:
                clasificar_tweet(tweet)
