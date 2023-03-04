import os
import warnings
from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText
from openfabric_pysdk.context import OpenfabricExecutionRay
from openfabric_pysdk.loader import ConfigClass
from time import time
import csv
import json
import random
from nltk.chat.util import Chat, reflections


############################################################
# Callback function called on update config
############################################################

import requests

WIKI_API_URL = 'https://en.wikipedia.org/w/api.php'

def wiki_search(query):
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': query,
        'srprop': 'size',
        'utf8': 1,
        'formatversion': 2
    }
    response = requests.get(WIKI_API_URL, params=params).json()
    if len(response['query']['search']) == 0:
        return None
    page_title = response['query']['search'][0]['title']
    page_text = get_wiki_text(page_title)
    return page_text


def get_wiki_text(page_title):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts',
        'exintro': 1,
        'explaintext': 1,
        'titles': page_title,
        'utf8': 1,
        'formatversion': 2
    }
    response = requests.get(WIKI_API_URL, params=params).json()
    if 'extract' not in response['query']['pages'][0]:
        return None
    return response['query']['pages'][0]['extract'].split('\n')[0]

import spacy

# load the English language model
nlp = spacy.load("en_core_web_sm")

# define a function to get the subject of a sentence
def get_subject(text):
    doc = nlp(text)
    subject = ""
    verb = ""
    for token in doc:
        if token.dep_ == "nsubj":
            subject = token.text
        elif token.dep_ == "ROOT":
            verb = token.lemma_
    search_query = f"{subject} {verb}"
    return search_query

def config(configuration: ConfigClass):
    # TODO Add code here
    pass


############################################################
# Callback function called on each execution pass
############################################################

class ListChat(Chat):
    def converse(self,text):
        response = self.respond(text)
        yield response

def execute(request: SimpleText, ray: OpenfabricExecutionRay) -> SimpleText:

    output = []

    for text in request.text:
        # TODO Add code here
        user_input = text
        answer=''
        if 'hi' == text or "Hi" == text:
            output.append("Hi!")
        else:
            answer = wiki_search(get_subject(user_input))
            if answer is not None:
                output.append(answer)
            else:
                output.append("Sorry, I couldn't find an answer to that question.")

    return SimpleText(dict(text=output))
