# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from twitstream.models import Tweet, Keyword
from quiz.models import Candidato

from tqdm import tqdm
from unidecode import unidecode


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

        tweets = Tweet.objects.filter(analizado=False)
        for tweet in tqdm(tweets):
            clasificar_tweet(tweet)
