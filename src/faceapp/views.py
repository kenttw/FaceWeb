from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from faceapp.models import Document
from faceapp.form import DocumentForm
import cv2
import sys
import numpy
from faceapp.faceDetectHandler import faceDetectHandler
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.files import File
# Create your views here.
# Create your views here.

def home(request):
#     excuses = [
#         "It was working in my head",
#         "I thought I fixed that",
#         "Actually, that is a feature",
#         "It works on my machine",
#     ]

#     excuse = random.choice(SayHello.objects.all())
    return render(request, "index.html", {'excuse': 333,'quantity':22 , 'price':33 })

def faceDetect(img):
    cascPath = '/Users/kent/Documents/workspace/FaceDetect/src/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)
    # Read the image
    
#     for d in img.read():
#         print str(d)
    
    file_bytes = numpy.asarray(bytearray(img.read()), dtype=numpy.uint8)
    img_data_ndarray = cv2.imdecode(file_bytes, cv2.CV_LOAD_IMAGE_UNCHANGED)
    
    if img_data_ndarray.shape[1] > 300 :
        fx = float(300)/img_data_ndarray.shape[1]
        fy = fx
        img_data_ndarray = cv2.resize(img_data_ndarray, (0,0), fx=fx , fy=fy ) 
    
    
#     with open('/test.jpg', 'rb') as img_stream:
#         file_bytes = numpy.asarray(bytearray(img_stream.read()), dtype=numpy.uint8)
#         img_data_ndarray = cv2.imdecode(file_bytes, cv2.CV_LOAD_IMAGE_UNCHANGED)
    #     img_data_cvmat = cv.fromarray(img_data_ndarray) #  convert to old cvmat if needed
    gray = cv2.cvtColor(img_data_ndarray, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(img_data_ndarray.shape[1]/30, img_data_ndarray.shape[1]/30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    
    print "Found {0} faces!".format(len(faces))
    
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img_data_ndarray, (x, y), (x+w, y+h), (0, 255, 0), 2)
     
#     cv2.imshow("Faces found", img_data_ndarray)
#     cv2.waitKey(0)
    cv2.imwrite("/Users/kent/Documents/workspace/FaceWeb/media/documents/2014/10/12/image.jpg" , img_data_ndarray)
    return File(open("/Users/kent/Documents/workspace/FaceWeb/media/documents/2014/10/12/image.jpg"))




def list(request):
    # Handle file upload

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
#             newdoc = Document(docfile = request.FILES['docfile'])
            newdoc = Document(docfile= faceDetect(request.FILES['docfile']))
            newdoc.save()
            
#             faceDetect()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('faceapp.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list2.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )