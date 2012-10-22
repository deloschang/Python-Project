from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save

class Experiences(models.Model):
    # user id
    title = models.CharField(max_length=60)
    creator = models.ManyToManyField(User, blank=True)

    # add invited field to for users to be added in when invited.

    album_pic = models.ForeignKey('Meme', blank=True, null=True)

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

class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    url_username = models.CharField(max_length=60)

    def __str__(self):  
          return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=User) 
