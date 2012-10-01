from django.db import models

class Document(models.Model):
    #docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    docfile = models.FileField(upload_to='documents/%Y/%m%d')

    def __unicode__(self):
        return self.file.name
