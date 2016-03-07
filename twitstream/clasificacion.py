from twitstream.models import Tweet, Keyword
from quiz.models import Candidato


def clasificar_tweet(tweet_object):
    candidatos = Candidato.objects.filter(entra_candidato=True)
    for candidato in candidatos:
        keywords_candidato = Keyword.objects.filter(candidato=candidato)
        
