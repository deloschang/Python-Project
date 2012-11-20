from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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
    source_content = models.ImageField(upload_to='images/%Y/%m%d', null=True)

    creator = models.ForeignKey(User, null=True, blank=True)
    # many-to-many relationship with the experiences

    e = models.ManyToManyField(Experiences, blank=True)
    #created = models.DateTimeField(auto_now_add=True)

    
    # for macromeme generator
    type = models.CharField(max_length=60, blank=True)
    #thumb = models.CharField(max_length=60, blank=True)  # path to relative path
    source = models.CharField(max_length=180, blank=True) # path to relative path


    title = models.CharField(max_length=90, blank=True)
    top_caption = models.CharField(max_length=180, blank=True)
    bottom_caption = models.CharField(max_length=180, blank=True)

    def __unicode__(self):
        return self.image.name

#@receiver(post_delete, sender=Meme)
#def post_delete_user(sender, instance, *args, **kwargs):
    #instance.image.delete(save=False)
    #instance.source_content.delete(save=False)

class MemeLibrary(models.Model):
    type = models.CharField(max_length=60, blank=True)
    thumb = models.CharField(max_length=180, blank=True)
    source = models.CharField(max_length=180, blank=True)
    title = models.CharField(max_length=90, blank=True)
    top_caption = models.CharField(max_length=180, blank=True)
    bottom_caption = models.CharField(max_length=180, blank=True)

    def __unicode__(self):
        return 'Title: '+self.title+' Source: '+self.source

class UserProfile(models.Model):  
    user = models.OneToOneField(User)  
    url_username = models.CharField(max_length=60)
    is_first_login = models.BooleanField(default=True)
    school = models.CharField(max_length=60, blank=True)

    def __str__(self):  
          return "%s's profile" % self.user  

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
        profile, created = UserProfile.objects.get_or_create(user=instance)  

        # add profile information for social auth after registration
        profile.url_username = profile.user.username.replace(' ','-') 
        count_existing = UserProfile.objects.filter(url_username__iexact=profile.url_username).count() # count existing url_username duplicates

        if count_existing !=0:
            profile.url_username = profile.url_username + '-' + str(count_existing)

        profile.save()

post_save.connect(create_user_profile, sender=User) 
