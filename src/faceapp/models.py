from django.db import models

# Create your models here.
class SayHello(models.Model):
    words = models.TextField()
    
    def __unicode__(self):
        return self.words    
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')