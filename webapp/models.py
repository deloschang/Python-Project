from django.db import models

class Document(models.Model):
    #docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    docfile = models.FileField(upload_to='documents/%Y/%m%d')

    def __unicode__(self):
        return self.docfile.name

class Meme(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m%d')
    # user id
    # which album it goes into

    def __unicode__(self):
        return self.image.name

class Experiences(models.Model):
    # user id
    title = models.CharField(max_length=60)

    def __unicode__(self):
        return self.title
