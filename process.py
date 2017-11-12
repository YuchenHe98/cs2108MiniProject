from collections import OrderedDict
import face_recognition
import os
import sqlite3
from sqlite3 import Error

def get_matched_results(gender, description):
    if gender == 'Female':
        all_pictures = os.listdir("profile_pictures/females")
    else:
        all_pictures = os.listdir("profile_pictures/males")
    all_pictures.pop(0)
    
    #get the feature vector of the uploaded picture.
    image_to_test = face_recognition.load_image_file("temp_upload/temp.jpg")
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
    pic_dict = {}
    for picture in all_pictures:
        if gender == 'Female':
            current = face_recognition.load_image_file("profile_pictures/females/"+picture)
        else:
            current = face_recognition.load_image_file("profile_pictures/males/"+picture)

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
    return get_text_match(gender, description, top_indices)

def get_text_match(gender, description, top_indices):
    database = "database.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        texts = []
        if(gender = 'Male'):
            for index in top_indices:
                texts.append(select_male_texts(conn, index)[0][0])
        else:
            for index in top_indices:
                texts.append(select_female_texts(conn, index)[0][0])
        return sim(description, texts)
    
def get_text_match(gender, description, top_indices):
            

 
 
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
    cur.execute("SELECT description FROM profile WHERE profile_image_id = "+index+"and gender = male")
 
    rows = cur.fetchall()
    return rows
 
 
def select_female_text(conn, index):

    cur = conn.cursor()
    cur.execute("SELECT description FROM profile WHERE profile_image_id = "+index+"and gender = female")
 
    rows = cur.fetchall()
    return rows
 
 
 
 

