from django.db import models

# Create your models here.
class SayHello(models.Model):
    words = models.TextField()
    
    def __unicode__(self):
        return self.words    
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    
class FbUser(models.Model):
    profile_url = models.CharField(max_length=256)
    id = models.CharField(primary_key=True,max_length=256)
    name = models.CharField(max_length=256)
    access_token = models.CharField(max_length=256)

class Photo(models.Model):
#     user_id = models.CharField(primary_key=True,max_length=256)
    user = models.ForeignKey('FbUser')

    url = models.URLField()
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

