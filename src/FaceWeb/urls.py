from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'FaceWeb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('faceapp.urls')),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + static('/images/', document_root='/Users/kent/Documents/workspace/FaceWeb/media/images')
urlpatterns = urlpatterns + static('/js/', document_root='/Users/kent/Documents/workspace/FaceWeb/media/js')
urlpatterns = urlpatterns + static('/css/', document_root='/Users/kent/Documents/workspace/FaceWeb/media/css')
# urlpatterns = urlpatterns + static('/static/', document_root='/Users/kent/Documents/workspace/FaceWeb/src/static')


