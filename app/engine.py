#!/usr/bin/env python
# coding: utf-8
import random
import nltk
import string
import numpy as np
import warnings

from app import app
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore")


def download_diseases_and_tokenize(url):
    article = Article(url.rstrip())
    article.download()
    article.parse()
    article.nlp()
    corpus = article.text
    return nltk.sent_tokenize(corpus)

def prepare_corpus(url_file):
    # Download punkt
    nltk.download("punkt", quiet=True)
    # Download as article from the URL
    urls = []
    sentence_list = []
    with open(url_file, "r") as ur:
        for each_url in ur:
            sentence_list.extend(download_diseases_and_tokenize(each_url))
    return sentence_list

def greetings(text):
    text = text.lower()

    bot_greetings = ['hello', 'hai', 'howdy', 'namaste', 'hey']
    user_greetings = ['hey', 'wassap', 'hai', 'hello']

    for each in text.split():
        if each in user_greetings:
            return random.choice(bot_greetings)

def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))
    x  = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

def bot_response(user_input, url_file="url_links.txt"):
    sentence_list = prepare_corpus(url_file)
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    # Similarity between the user input and the sentence_list(the tokenized version of the website)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    # We are not interested in the last item on the sentence_list
    # ( the first one on the index_score as it is the
    # user response)
    index = index[1:]
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            j += 1
            response_flag = 1
        if j > 2:
            break
    if response_flag == 0:
        bot_response = bot_response + " " + "I don't have the answer for you!!!"
    sentence_list.remove(user_input)
    return bot_response

def ask_bot(user_input):
    exit_list = ['exit', 'see you later','bye', 'quit', 'break']
    if(user_input.lower() in exit_list):
      return ("Doc Bot: Chat with you later !")
    else:
      if(greetings(user_input)!= None):
        return greetings(user_input)
      else:
        return bot_response(user_input)
