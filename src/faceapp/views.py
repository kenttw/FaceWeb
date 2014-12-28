import random
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from faceapp.models import Document , Photo
from faceapp.form import DocumentForm

from faceapp import facebookConnect

def list(request):
    
    fbGraph = facebookConnect.getGraph(request.COOKIES)
    current_user = None
    if fbGraph != None :
        access_token = 'todo'
        current_user = facebookConnect.getFBContent(fbGraph,access_token)
        current_user.access_token = access_token
        photos = facebookConnect.getPhotos(fbGraph)
        if current_user != None : 
#             for url in  photos :
#                 photourl = Photo()
#                 photourl.url = url
#                 photourl.user = current_user
#                 dimag = facebookConnect.download_photo(url)
#                 facesresult = facebookConnect.faceDetect(dimag)
#                 if facesresult != None :
#                     photourl.docfile = facesresult
#                     photourl.save()
            current_user.save()
    
    # Handle file upload
    
#     if current_user != None and request.method == 'POST':
#         form = DocumentForm(request.POST, request.FILES)
#         
#         if form.is_valid():
#             newdoc = Document(docfile=facebookConnect.faceDetect(request.FILES['docfile']))
#             newdoc.save()
#             
#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('faceapp.views.list'))
#     else:
#         form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = [] 
    docuemnts2 =[]
    
    for item in Photo.objects.all() :
        if item.docfile != '' :
            documents.append(item)
    for i in range(0,9) :
        docuemnts2.append(random.choice(documents))

    # Render list page with the documents and the form
    return render_to_response(
        'list2.html',
        {'documents': docuemnts2 ,
#          'form': form ,
         'current_user' :current_user ,
         'facebook_app_id' : facebookConnect.facebook_app_id
         },
        context_instance=RequestContext(request)
    )

# def myudf():
#     '''
#     
#     '''
#     
#     pass
#     


def demo_piechart(request):
    """
    pieChart page
    """
    
    
    from impala.dbapi import connect
    conn = connect(host='210.63.38.209', port=21050)
    cur = conn.cursor()
    cur.execute('select cat , count(pid) from abc_item group by cat limit 10')
    
    print cur.description  # prints the result set's schema
    alldata = cur.fetchall()
    
    xdata = []
    ydata = []
    for item in alldata :
        xdata.append(item[0])
        ydata.append(item[1])

    color_list = ['#5d8aa8', '#e32636', '#efdecd', '#ffbf00', '#ff033e', '#a4c639',
                  '#b2beb5', '#8db600', '#7fffd4', '#ff007f', '#ff55a3', '#5f9ea0']
    extra_serie = {
        "tooltip": {"y_start": "", "y_end": " cal"},
        "color_list": color_list
    }
    chartdata = {'x': xdata, 'y1': ydata, 'extra1': extra_serie}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'  # container name

    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render_to_response('piechart.html', data)
