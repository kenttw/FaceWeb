# -*- coding: utf-8 -*-
'''
Created on 2014年10月18日

@author: kent
'''
import facebook
import urllib2
import cv2
import numpy
from django.core.files import File
from django.core.files.base import ContentFile

facebook_app_id = '258318471185'
facebook_app_secret = 'da26ac5b7675c75cc2b9a25d87b6b8af'


class current_user:
    profile_url = None
    id = None
    name = None
    photos = None
    access_token = None
    

def getFBContent(cookies):
#             cookies = dict((n, self.cookies[n].value) for n in self.cookies.keys())
    
    user = current_user()
    cookie = facebook.get_user_from_cookie(
        cookies, facebook_app_id, facebook_app_secret)
    
    if cookie == None :
        return 
    
    graph = facebook.GraphAPI(cookie["access_token"])
    profile = graph.get_object("me")
    user.name = profile['name']
    user.profile_url = profile['link']
    user.id = profile['id']
    user.access_token = cookie['access_token']
    
    photos = graph.get_object('me?fields=photos')
    user.photos = []
        
        
#         photos['photos']['data'][0]['images'][0]['source']
        
    for item in photos['photos']['data'] :
        for item3 in item['images'] :
            user.photos.append(item3['source'])
            
    return user
            
            
def download_photo(img_url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')]
    response = opener.open(img_url)
#     htmlData = response.read()
    return response

def faceDetect(img):
    cascPath = '/Users/kent/Documents/workspace/FaceDetect/src/haarcascade_frontalface_default.xml'
    cascSmile = '/opt/opencv/opencv/data/haarcascades/haarcascade_smile.xml'
    
    
    faceCascade = cv2.CascadeClassifier(cascPath)
    smileCascade = cv2.CascadeClassifier(cascSmile)

    
    file_bytes = numpy.asarray(bytearray(img.read()), dtype=numpy.uint8)
    img_data_ndarray = cv2.imdecode(file_bytes, cv2.CV_LOAD_IMAGE_UNCHANGED)
    
    if img_data_ndarray.shape[1] > 600 :
        fx = float(600) / img_data_ndarray.shape[1]
        fy = fx
        img_data_ndarray = cv2.resize(img_data_ndarray, (0, 0), fx=fx , fy=fy) 
    
    gray = cv2.cvtColor(img_data_ndarray, cv2.COLOR_BGR2GRAY)
    
    faces = detect(gray, faceCascade)
#     vis = img.copy()
    draw_rects(img_data_ndarray, faces, (0, 255, 0))   
    print "Found {0} faces!".format(len(faces))
    
    for x1, y1, x2, y2 in faces:
        roi = gray[y1:y2, x1:x2]
        vis_roi = gray[y1:y2, x1:x2]
        subrects = detect(roi.copy(), smileCascade)
        print "Found {0} smile!".format(len(subrects))
 
        draw_rects(img_data_ndarray, subrects, (255, 0, 0))    
    
    
    
    

#     # Detect faces in the image
#     faces = faceCascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=5,
#         minSize=(img_data_ndarray.shape[1] / 100, img_data_ndarray.shape[1] / 100),
#         flags=cv2.cv.CV_HAAR_SCALE_IMAGE
#     )
#     
#     
#         # Detect faces in the image
#     smiles = smileCascade.detectMultiScale(
#         gray,
#         scaleFactor=1.1,
#         minNeighbors=5,
#         minSize=(img_data_ndarray.shape[1] / 300, img_data_ndarray.shape[1] / 300),
#         flags = cv2.cv.CV_HAAR_SCALE_IMAGE
#     )  
#     
    print "Found {0} faces!".format(len(faces))
    if len(faces) == 0 :
        return None
    
#     # Draw a rectangle around the faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img_data_ndarray, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    
    img_data_ndarray = cv2.imencode('.jpg', img_data_ndarray)[1].tostring()
    file = ContentFile(img_data_ndarray)
    file.name = 'aa.jpg'
    return file

def detect(img, cascade,size=50):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(size, size), flags = cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)