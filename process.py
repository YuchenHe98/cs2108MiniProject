from collections import OrderedDict
import face_recognition
import os
import sqlite3
from sqlite3 import Error
import argparse
import nltk
import numpy as np
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity

def get_matched_results(gender, description):
    if gender == 'M':
        all_pictures = os.listdir("profile_pictures/males")
    else:
        all_pictures = os.listdir("profile_pictures/females")
    all_pictures.pop(0)
    
    #get the feature vector of the uploaded picture.
    image_to_test = face_recognition.load_image_file("temp_upload/temp.jpg")
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
    pic_dict = {}
    for picture in all_pictures:
        if gender == 'M':
            current = face_recognition.load_image_file("profile_pictures/males/"+picture)
        else:
            current = face_recognition.load_image_file("profile_pictures/females/"+picture)

        encoding = face_recognition.face_encodings(current)
        
        #compute the face distance.
        face_distance = face_recognition.face_distance(encoding, image_to_test_encoding)
        if len(face_distance) != 0:
            pic_dict[int(picture.replace('.jpg', ''))] = face_distance[0]
        print(face_distance)
        print("this is for",picture)
        
    #extract top 10 indices
    sorted_dict = OrderedDict(sorted(pic_dict.items(), key=lambda x: x[1]))
    top_indices = list(sorted_dict.keys())[:10]
    print(top_indices)
    return get_text_match(gender, description, top_indices)

def get_text_match(gender, description, top_indices):
    database = "database.db"
 
    # create a database connection
    conn = create_connection(database)
    print(top_indices)
    with conn:
        texts = []
        if(gender == 'M'):
            for index in top_indices:
                texts.append(select_male_texts(conn, index)[0][0])
        else:
            for index in top_indices:
                texts.append(select_female_texts(conn, index)[0][0])
    text_dict = {}
    current = 0
    for index in top_indices:
        text_dict[index] = sim(description, texts)[current][0]
        current = current + 1
    sorted_dict = OrderedDict(sorted(text_dict.items(), key=lambda x: x[1]))
    reranked_indices = list(sorted_dict.keys())[:10]
    reversed_indices = reranked_indices[::-1]
    return reversed_indices
    
    
def sim(description, texts):
    descriptions = []
    descriptions.append(description)
    vec_docs, vec_queries, tfidf_model = tf_idf(texts, descriptions, tokenize_text)
    sim_matrix = cosine_similarity(vec_docs, vec_queries)
    return sim_matrix


 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
 
 
def select_male_texts(conn, index):

    cur = conn.cursor()
    cur.execute("SELECT description FROM profile WHERE id = "+str(index)+" and gender = 'M' ")
 
    rows = cur.fetchall()
    return rows
 
 
def select_female_texts(conn, index):

    cur = conn.cursor()
    cur.execute("SELECT description FROM profile WHERE id = "+str(index)+" and gender = 'F' ")
 
    rows = cur.fetchall()
    return rows


def tf_idf(docs, queries, tokenizer):
    """
    performs TF-IDF vectorization for documents and queries
    Parameters
        ----------
        docs : list
            list of documents
        queries : list
            list of queries
        tokenizer : custom tokenizer function

    Returns
    -------
    tfs : sparse array,
        tfidf vectors for documents. Each row corresponds to a document.
    tfs_query: sparse array,
        tfidf vectors for queries. Each row corresponds to a query.
    dictionary: list
        sorted dictionary
    """
    model = str.maketrans(dict.fromkeys(string.punctuation))
    processed_docs = [d.lower().translate(model) for d in docs]
    tfidf = TfidfVectorizer(stop_words='english', tokenizer=tokenizer)
    tfs = tfidf.fit_transform(processed_docs)
    tfs_query = tfidf.transform(queries)
    return tfs, tfs_query, tfidf

def tokenize_text(docs):
    """
    custom tokenization function given a list of documents
    Parameters
        ----------
        docs : string
            a document

    Returns
    -------
    stems : list
        list of tokens
    """

    text = ''
    for d in docs:
        text += '' + d
    stemmer = PorterStemmer()
    tokens = nltk.word_tokenize(text)
    stems = []
    for item in tokens:
        stems.append(stemmer.stem(item))
    return stems


