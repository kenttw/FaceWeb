from django.contrib import admin

# Register your models here.

# Register your models here.
from faceapp.models import Document , Photo , FbUser

admin.site.register(Document)
admin.site.register(FbUser)
admin.site.register(Photo)

# admin.site.register(Choice)