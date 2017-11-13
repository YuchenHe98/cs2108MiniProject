from collections import OrderedDict
import face_recognition
import os

def get_picture_result():
    all_pictures = os.listdir("profile_pictures/females")
    all_pictures.pop(0)
    
    #get the feature vector of the uploaded picture.
    image_to_test = face_recognition.load_image_file("temp_upload/temp.jpg")
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
    pic_dict = {}
    for picture in all_females_pictures:
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
    return top_indices


# def get_text_results(indices):