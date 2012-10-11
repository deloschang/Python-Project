from django.db import models
from django.contrib.auth.models import User

class Experiences(models.Model):
    # user id
    title = models.CharField(max_length=60)
    creator = models.ForeignKey(User, null=True, blank=True)


    def __unicode__(self):
        return self.title

class Meme(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m%d')
    creator = models.ForeignKey(User, null=True, blank=True)
    # many-to-many relationship with the experiences

    e = models.ManyToManyField(Experiences, blank=True)
    #created = models.DateTimeField(auto_now_add=True)

    # which album it goes into

    def __unicode__(self):
        return self.image.name
