# required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q

# for login required
from django.contrib.auth.decorators import login_required

# exempt csrf
from django.views.decorators.csrf import csrf_exempt

# for meme uploading
from django.http import HttpResponseRedirect

# temp to test AJAX
from django.http import HttpResponse


# for models and forms
from webapp.models import *
from webapp.forms import *
from email_usernames.forms import EmailRegistrationForm

# for registration
from registration.views import register

# for invitation 
from invitation.views import invite
from django.conf import settings
from invitation.models import InvitationKey

# for messages
from django.contrib import messages

# for generator
import json
import base64
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files import File
from django.utils.html import strip_tags # sanitize
import urllib2
from django.core.files.temp import NamedTemporaryFile


# Home URL and Profile Page
def index(request, backend, success_url=None, 
        form_class=EmailRegistrationForm, profile_callback=None,
        template_name='landing.html',
        extra_context=None, invitation_key=None):

    # Show landing page with registration 
    if not request.user.is_authenticated():
        # Check invite mode 
        if hasattr(settings, 'INVITE_MODE') and settings.INVITE_MODE:
            is_key_valid = InvitationKey.objects.is_key_valid
            # check key with email and pull email.


            #### HANDLE INVITATION PROCESS ####
                ## For prefilling email registration, go to registration/views.py
            # User enters site 
            if invitation_key and is_key_valid(invitation_key): 
                # has valid key

                # grab associated object with key
                str_invitation = '"'+invitation_key+'"'
                invitee_object = InvitationKey.objects.get(key=invitation_key)

                # save email and album_no in session to pass into registration
                request.session['email'] = invitee_object.to_user_email
                request.session['invited_album'] = invitee_object.from_user_album
                request.session['invite_key'] = invitation_key

                # show registration landing w/ prefilled
                return register(request, backend, success_url, form_class, profile_callback, template_name, extra_context={'invitation_key': invitation_key, 'invitee_object': invitee_object})

            else:
                if invitation_key == None:
                    # User enters website normally (uninvited)
                    return register(request, backend, success_url, form_class, profile_callback, template_name, extra_context)
                else:
                    # User entered invalid key
                    template = 'invitation/wrong_invitation_key.html'
                    return render_to_response(template, {'invitation_key': invitation_key }, RequestContext(request))

        else: 
            # norm registration mode (not used unelss invite mode off)
            return register(request, backend, success_url, form_class, profile_callback, template_name, extra_context)
        
    ## SHOW PROFILE PAGE ##
    else:


        # grabs uncategorized memes from the database
        # filter by USER
            # filter out categorized memes
        memes = reversed(Meme.objects.filter(creator = request.user, e = None))
        
        # grabs existing experiences/albums from the database
        # filter by USER
        experiences = Experiences.objects.filter(creator = request.user)

        # form to create new experience/album
        addexperienceform = AddExperienceForm()

        # form to upload meme
        imageform = ImageUploadForm()
        
        return render_to_response(
                'profile.html',
                {'memes': memes, 'experiences': experiences, 'addexperienceform': addexperienceform, 'imageform' : imageform},
                RequestContext(request))

# Upload a Meme 
@login_required
def create(request):
    #import pdb; pdb.set_trace()

    # Handle file upload
    if request.method == 'POST':
        imageform = ImageUploadForm(request.POST, request.FILES)

        if imageform.is_valid():
            newimage = Meme(image = request.FILES['image'], creator = request.user)
            newimage.save()

            #redirect('webapp.views.index')
            return HttpResponseRedirect(reverse('webapp_index'))
            #return render_to_response(
                #'profile.html',
                #context_instance=RequestContext(request)
            #)



        #form = DocumentForm(request.POST, request.FILES)
        #if form.is_valid():
            #newdoc = Document(docfile = request.FILES['docfile'])
            #newdoc.save()


            # THIS SHOULD REDIRECT USER TO THE PROFILE PAGE AFTER UPLOADING
            #return HttpResponseRedirect(reverse('webapp.views.create'))
    else:
        imageform = ImageUploadForm()
        #form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    #documents = Document.objects.all()

    # Render list page with the documents and the form
        return render_to_response(
            'user/create.html',
            context_instance=RequestContext(request)
        )


def library(request, meme_id = None):
    # grab memes from library database
    if meme_id:
        # if remixing, filter only for the selected meme
        selected_meme_id = strip_tags(meme_id)  # need to sanitize

        meme_obj = Meme.objects.filter(pk=meme_id, creator = request.user) # filter for meme id and ownership
    else:
        meme_obj = MemeLibrary.objects.all()


    item_list = []
    for meme in meme_obj:

        # add fields into dict
        if meme_id:
            # if remixing, no need for thumb
            response_data = {
                "title": meme.title,
                "type": meme.type,
                "source": meme.source,
                #"source": "/static/images/bad_joke_eel.jpg"
            }
        else:
            response_data = {
                "title": meme.title,
                "type": meme.type,
                "thumb": meme.thumb,
                "source": meme.source,
            }

        # decode caption
        response_data['top_caption'] = json.loads(meme.top_caption)
        response_data['bottom_caption'] = json.loads(meme.bottom_caption)

        item_list.append(response_data)

    # Add the meme JSONs into larger items container
    items = {
        "items": item_list
    }

    # re-encode the dict and pass back to generator
    return HttpResponse(json.dumps(items), mimetype="application/json")

@csrf_exempt   # send in csrf token  in the future
def macromeme_publish(request):
    if request.method == 'POST':

        # sanitize input
        type = request.POST['type']
        title = strip_tags(request.POST['title'])
        top_caption = strip_tags(request.POST['top_caption'])
        bottom_caption = strip_tags(request.POST['bottom_caption'])

        # decode the byte array and save into disk
        img_byte_array = base64.b64decode(request.POST['image'])

        # when meme from facebook
        # request.POST = http://
        # when meme from computer/cropped
        # request.POST = base64 decode 

        ### OBSOLETE: saving to disk ###
        #out = open("temp_newfilepath.png", "wb")
        #out.write(img_byte_array) # write into disk
        #out.close()

        #saved_image = Image.open("temp_newfilepath.png")
        ### end ###


        # add image into DB
        img_content = ContentFile(img_byte_array)

        add_meme_in_db = Meme(creator = request.user, type = type, title = title, top_caption = top_caption, bottom_caption = bottom_caption) 

        img_file_path = request.user.get_profile().url_username # unique to username
        img_file_format = '.png'

        # check what photo source is
        if request.POST['photo_source'] == 'library':
            add_meme_in_db.source = request.POST['source'] # source is just filepath to library source image

        elif request.POST['photo_source'] == 'facebook':
            # take img from URL and download to server
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(request.POST['source']).read())
            img_temp.flush()

            add_meme_in_db.source_content.save(img_file_path+'_source'+img_file_format, File(img_temp))
            add_meme_in_db.source = '/static/media/'+add_meme_in_db.source_content.name # filepath of saved source

        elif request.POST['photo_source'] == 'computer': # source is from 'upload image' or was cropped
            # write base64 into disk

            source_byte_array = base64.b64decode(request.POST['source'])
            source_image = ContentFile(source_byte_array)

            add_meme_in_db.source_content.save(img_file_path+'_source'+img_file_format, source_image)
            add_meme_in_db.source = '/static/media/'+add_meme_in_db.source_content.name # filepath of saved source

        # save created image with filepath
        add_meme_in_db.image.save(img_file_path+img_file_format, img_content) # save image into database

        ### OBSOLETE: thumb ###
        # create thumbnail and save path to disk
        #saved_image.thumbnail((120, 120), Image.ANTIALIAS)
        #new_out = open("test_thumbnail.png", "wb")
        #saved_image.save(new_out, 'PNG')

        # add thumbnail image into DB
        #thumb_data = open('test_thumbnail.png', 'r')
        #thumbnail_img_content = File(thumb_data)
        #add_meme_in_db.thumb.save('test_thumbnail.png', thumbnail_img_content)
        #add_meme_in_db.thumb = '/static/images/test_thumbnail.png' #filepath
        ### end ###

        add_meme_in_db.save()
        
        return HttpResponse('http://new.memeja.com')



# Add new album for user   
@login_required
def add_experience(request):
    if request.method == 'POST':
        # add experience into database
        
        new_experience_form = AddExperienceForm(request.POST)
        if new_experience_form.is_valid(): 
            post = request.POST
            logged_user = request.user # the user's username

            # adds the experience from form into database
            creator_obj = User.objects.get(pk=request.user.id) # grab user object with id
            new_experience = Experiences(title = request.POST['title']) # create the experience
            new_experience.save()
            new_experience.creator.add(creator_obj) # add user object into the experience

            return HttpResponseRedirect(reverse('webapp_index'))

# User clicks an album and experiences are displayed
@login_required
def show_experience(request, pk,
        success_url=None, form_class=InvitationKeyForm,
        template_name='user/experience_display.html',
        extra_context=None,):


    # Check if user has access to the experiences album
    try:
        experiences = request.user.experiences_set.get(pk=pk)

        # Form to invite friends
        form = form_class()

        # Grabs memes within the experience albums
            # reverse order: newest memes are on top
        memes = reversed(experiences.meme_set.all())
        return invite(request, success_url, form_class, template_name, extra_context={'experiences':experiences, 'memes':memes})

    # User does not have access to the experiences album
    except:
        return render_to_response('profile/access_denied.html', RequestContext(request))

# User clicks on linked username & profile of shared albums displayed
def linked_username(request, linked_username):
    # Check if username exists
    #try: 
        # Index by username provided in hyphened URL
        linked_user_obj = UserProfile.objects.get(url_username = linked_username).user

        # Check if USER is logged in (if not show a landing page)
        if request.user.is_authenticated():
            # Grab albums that this user has in common with you
            linked_experiences = Experiences.objects.filter(creator = request.user).filter(creator = linked_user_obj)

            return render_to_response('user/shared_profile.html', 
                    {'linked_experiences': linked_experiences, 'linked_user': linked_user_obj},
                    RequestContext(request)) 
        else:
            return HttpResponseRedirect(reverse('webapp_index'))

    #except:
        # Username doesn't exist
            # maybe replace with surprise/delight page later
        #return HttpResponseRedirect(reverse('webapp_index'))


# drag meme into album and update server
@login_required
def meme_in_album(request):
    if request.is_ajax():
        if request.method == 'POST':
            dragged_meme_id = request.POST['meme']
            dropped_album_id = request.POST['album']

            dragged_meme_obj = Meme.objects.get(pk=dragged_meme_id)
            dropped_album_obj = Experiences.objects.get(pk=dropped_album_id)

            # Check if user is authenticated for album and meme
            if request.user == dragged_meme_obj.creator and request.user.experiences_set.get(pk=dropped_album_id):
                dragged_meme_obj.e.add(dropped_album_obj)

                # If no album profile pic, add it
                if not dropped_album_obj.album_pic: 
                    dropped_album_obj.album_pic = dragged_meme_obj # adding instance
                    dropped_album_obj.save()

            # newimage = Meme.objects.get(pk=#)
            # testalbum = Experiences.objects.get(pk=#)
            # newimage.e.add(testalbum)

            #updated_meme_count = dropped_album_obj.meme_set.count
            return HttpResponse('success')
            #return render_to_response('user/experience_display.html')
    else:
        return HttpResponse('this is not ajax')

@login_required
def delete_meme(request, delete_meme_id=None):

    if delete_meme_id:
        # Query for the meme
        try:
            selected_meme = Meme.objects.get(pk=delete_meme_id)

            # Check if user created the meme
            if request.user == selected_meme.creator:
                # Delete it and refresh page
                selected_meme.delete()
                    # calls post_delete signal to delete files
                messages.add_message(request, messages.INFO, 'Success! You deleted the meme!')

                return HttpResponseRedirect(reverse('webapp_index'))
            else:
                # Meme does not belong to user
                return render_to_response('profile/access_denied.html', RequestContext(request))
        except:
            # Meme does not exist
            return render_to_response('profile/access_denied.html', RequestContext(request))

@login_required
def delete_album(request, delete_album_id=None):
    if delete_album_id:
        # Query for the album
        try:
            selected_album = request.user.experiences_set.get(pk=delete_album_id)

            # delete memes in album
            selected_album.meme_set.all().delete()

            # delete album and refresh page
            selected_album.delete()
            messages.add_message(request, messages.INFO, 'Success! You deleted the album')

            return HttpResponseRedirect(reverse('webapp_index'))
        except:
            # User does not have access to album or DNE
            return render_to_response('profile/access_denied.html', RequestContext(request))

def custom_404(request):
    return render_to_response('400.html', RequestContext(request))

def custom_500(request, template_name='500.html'):
    return render_to_response(template_name, RequestContext(request))



