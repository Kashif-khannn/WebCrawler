import os
from pathlib import Path
from bs4 import BeautifulSoup, SoupStrainer
import requests
from newspaper import Article
import sys
import io
import email
import nltk
from os import walk


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from collections import Counter

import string

database = {}
databaseclean = dict()
invertedIndex = database



def spider(array):
    i=0
    outlist = []
    # going through the list of inputs
    while i < len(array):
        # url to take the links from
        url="https://ca.news.search.yahoo.com/search;_ylt=AwrC0F8hlQBhWyYAMA7wFAx.;_ylc=X1MDMjExNDcyMTAwOARfcgMyBGZyAwRmcjIDc2ItdG9wBGdwcmlkAzBJRHJfTjdyUjB5VUNfU2sudFpKUEEEbl9yc2x0AzAEbl9zdWdnAzEEb3JpZ2luA2NhLm5ld3Muc2VhcmNoLnlhaG9vLmNvbQRwb3MDMARwcXN0cgMEcHFzdHJsAzAEcXN0cmwDNgRxdWVyeQNoYW1kYW4EdF9zdG1wAzE2Mjc0MjgxMzY-?p="+array[i]
        sourse_code = requests.get(url)
        plain_text= sourse_code.text
        soup = BeautifulSoup(plain_text,"lxml")
        counter = 0
        innerlist = []

        for link in soup.findAll("a",{'style':'font-size:16px;'}):
            # f = open("dataset/"+array[i]+"/"+array[i]+"{}".format(counter)+".html","w")
            # parsing the html and getting the data from it and append it to a 2D list
            href = link.get('href')
            article = Article(href)
            article.download()
            article.parse()
            innerlist.append(article.text)
            counter+=1
        i+=1
        outlist.append(innerlist)
    return outlist

def delisting(array, naming):
    # removing the data from the array and putting it in the files
    for k in range(len(array)):
        for j in range(len(array[k])):

            with io.open(file="DataSet/"+naming[k]+"/"+naming[k]+ "{}".format(j) + ".txt",mode='w',encoding="utf-8") as f:
                f.write(array[k][j])

    f.close()
    print("printed into file")
    return

def filesOutput(fPath,fName):
    # to clean the data like pantuations, stop words and lemmanization
    doccumentId = fName
    dsfile = open(fPath,"r", encoding="utf8")
    for line in dsfile:
        new_query = word_tokenize(line)
        tokens = [w.lower() for w in new_query]
        punc = str.maketrans('', '', string.punctuation)
        strip = [w.translate(punc) for w in tokens]
        words = [word for word in strip if word.isalpha()]
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]
        lemmatizer = WordNetLemmatizer()
        lemma = [lemmatizer.lemmatize(word) for word in words]

    return doccumentId, lemma
def DTM(fpath, fname):
    docId, lemmword = filesOutput(fpath, fname)
    # store the words and frequency and the docid in the database
    for i in lemmword:
        count = lemmword.count(i)
        database.setdefault(i,[])
        
        if i in database:
            database[i].append((docId,count))
        else:
            database[i]=(docId,count)
    # clean the database from the duplicates
    for i in lemmword:
        result = list(dict.fromkeys(database.get(i)))
        databaseclean[i]=result

    return

if __name__ == "__main__":
   
    new_topic_split=["BasketBall","NBA", "Sports"]
    
    lists = spider(new_topic_split)
    delisting(array=lists, naming=new_topic_split)
    print("DTM For BasketBall dataset:")
    _,_,filename = next(walk("DataSet/BasketBall/"))
    for i in filename:
        DTM("DataSet/BasketBall/" + i,i)
    
    for key, value in databaseclean.items():
        counter = len(value)
        print("Frequency of ’{}’ ----> {}".format(key, counter))
    print("------------------------------------------------------------------------------------------------------------------")
    print("")
    print("DTM For NBA dataset:")
    _,_,filename = next(walk("DataSet/NBA/"))
    for i in filename:
        DTM("DataSet/NBA/" + i,i)
    for key, value in databaseclean.items():
        counter = len(value)
        print("Frequency of ’{}’ ----> {}".format(key, counter))
    print("------------------------------------------------------------------------------------------------------------------")
    print("")
    print("DTM For Sports dataset:")
    _,_,filename = next(walk("DataSet/Sports/"))
    for i in filename:
        DTM("DataSet/Sports/" + i,i)
    for key, value in databaseclean.items():
        counter = len(value)
        print("Frequency of ’{}’ ----> {}".format(key, counter))
    print("-------------------------------------------------------------------------------------------------------------------")
    print("")

