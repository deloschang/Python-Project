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
from email_usernames.forms import EmailRegistrationForm, EmailLoginForm

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

# for autocomplete
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteField


# login for YC
from django.contrib.auth import login

# for mailing admins
#from django.core.mail import send_mail
from datetime import datetime
import os

#### TEST URL FOR YC ####
def yc_no_login(request, extra=None):
    # preauthenticate with email and password
    post_values = {}
    post_values['email'] = 'yc@gmail.com'
    post_values['password'] = 'dmang'

    login_form = EmailLoginForm(data=post_values)
    if login_form.is_valid():
        # The user has been authenticated, so log in and redirect
        user = login(request, login_form.user)

        ####### send an email to admins #######
        #if not settings.DEBUG:
            #subject = 'YCombinator logged in'
            #message = request.user.username+' logged in with '+request.user.email
            #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['deloschang@memeja.com'], fail_silently=True)
        ####### end #######

        if extra != 'test':
            date = []
            date.append(str(datetime.now()))
            with open(os.path.join(settings.STATIC_ROOT, 'login_track.txt'), "a") as text_file:
                text_file.write(date[0]+'    '+request.user.username+' logged in with '+request.user.email+'\n')
        else:
            date = []
            date.append(str(datetime.now()))
            with open(os.path.join(settings.STATIC_ROOT, 'login_track.txt'), "a") as text_file:
                text_file.write(date[0]+'     TEST:'+request.user.username+' logged in with '+request.user.email+'\n')

        if extra == 'create':
            return HttpResponseRedirect(reverse('create'))

        else:
            # Send YC to tutorial
            messages.add_message(request, messages.INFO, 'For our demo, this first-time tutorial is shown every time', extra_tags="text-warning")
            return HttpResponseRedirect(reverse('webapp_helloworld'))


# Home URL and Profile Page
@csrf_exempt
def index(request, backend, success_url=None, 
        form_class=EmailRegistrationForm, profile_callback=None,
        #authentication_form = EmailLoginForm,
        template_name='landing.html',
        page_template = 'entry_index_page.html',
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
                    #1 User enters website normally (uninvited)
                    #form_auth = EmailLoginForm() # for login form
                    return register(request, backend, success_url, form_class, profile_callback, template_name, extra_context=None)
                            #extra_context={'form_auth': form_auth})
                else:
                    # User entered invalid key
                    template = 'invitation/wrong_invitation_key.html'
                    return render_to_response(template, {'invitation_key': invitation_key }, RequestContext(request))

        else: 
            # norm registration mode (not used unless invite mode off)
            return register(request, backend, success_url, form_class, profile_callback, template_name, extra_context)
        
    ## SHOW PROFILE PAGE with SCHOOL FEED ##
    else:


        ### TEMP ###
        berkeley = 0 
        dartmouth = 0 
        ## end ##




        ###### BRING UP SCHOOL FEED ######
        # Find College Meme user w/ school memes
        college_meme_obj = User.objects.get(username = 'College Memes')

        user_school = request.user.get_profile().school
        if user_school == 'Berkeley':
            drag_list_experience = Experiences.objects.get(title = settings.SCHOOL_UCB_ALBUM, creator = college_meme_obj) 

            #temp
            berkeley = drag_list_experience
        elif user_school == 'Dartmouth': 
            drag_list_experience = Experiences.objects.get(title = settings.SCHOOL_DARTMOUTH_ALBUM, creator = college_meme_obj) 


            #temp
            dartmouth = drag_list_experience
        else:
            drag_list_experience = Experiences.objects.get(title = 'General', creator = college_meme_obj) # if nothing, default to General

        school_feed_memes = drag_list_experience.meme_set.all().order_by('-id')

        # grabs user's albums from the database
        experiences = Experiences.objects.filter(creator = request.user)

        # form to create new experience/album
        addexperienceform = AddExperienceForm()

        # form to upload meme
        imageform = ImageUploadForm()

        if request.is_ajax():
            template = page_template
        else:
            template = 'profile.html'

        return render_to_response(
                template,
                {'memes': school_feed_memes, 'experiences': experiences,
                    'page_template': page_template, 
                    'addexperienceform': addexperienceform,
                    'imageform' : imageform,
                    'user_school': user_school,

                    # temp
                    'dartmouth': dartmouth,
                    'berkeley': berkeley,
                },
                # is_uncat is 0 (user on feed not uncat page)
                RequestContext(request))

# shows uncategorized feed
def index_uncat(request):
        ##### For uncategorized ####
        # grabs uncategorized memes from the database
        # filter by USER
            # filter out categorized memes

        user_school = request.user.get_profile().school



        #### TEMP #####
        ### TEMP ###
        berkeley = 0 
        dartmouth = 0 
        college_meme_obj = User.objects.get(username = 'College Memes')
        if user_school == 'Berkeley':
            drag_list_experience = Experiences.objects.get(title = settings.SCHOOL_UCB_ALBUM, creator = college_meme_obj) 

            #temp
            berkeley = drag_list_experience
        elif user_school == 'Dartmouth': 
            drag_list_experience = Experiences.objects.get(title = settings.SCHOOL_DARTMOUTH_ALBUM, creator = college_meme_obj) 


            #temp
            dartmouth = drag_list_experience
        else:
            drag_list_experience = Experiences.objects.get(title = 'General', creator = college_meme_obj) # if nothing, default to General
        ## end ##


        memes = reversed(Meme.objects.filter(creator = request.user, e = None))
        
        # grabs user's albums from the database
        experiences = Experiences.objects.filter(creator = request.user)

        # form to create new experience/album
        addexperienceform = AddExperienceForm()

        # form to upload meme
        imageform = ImageUploadForm()

        return render_to_response(
                'profile.html',
                {'memes': memes, 'experiences': experiences, 'addexperienceform': addexperienceform,
                    'imageform' : imageform, 'user_school': user_school,
                    'is_uncat':1,
                    'is_album':0,

                    # temp
                    'dartmouth': dartmouth,
                    'berkeley': berkeley,
                    },
                # is_uncat tells profile.html if user is on uncat page or feed page
                # is_album says if album
                RequestContext(request))

# Upload a Meme 
@login_required
def create(request):
    # Handle file upload
    if request.method == 'POST':
        imageform = ImageUploadForm(request.POST, request.FILES)

        if imageform.is_valid():
            newimage = Meme(image = request.FILES['image'], creator = request.user)
            newimage.save()

            #redirect('webapp.views.index')
            return HttpResponseRedirect(reverse('webapp_index_uncat'))
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
        
        if request.path == '/welcome/hello-world/publish/': ## hardcoded from the urls.py - DO NOT CHANGE
            # add the created meme into the tutorial album
            first_friend_experience = request.session['first_friend_experience']

            add_meme_in_db.e.add(first_friend_experience)
            return HttpResponse('invite') # like localhost:8000/welcome/hello-world/invite
        else:
            #return HttpResponse('')
            return HttpResponse('http://memeja.com/uncat_library')
            #return HttpResponse('http://localhost:8000/uncat_library')

# First-time user tutorial page 'experience'
@login_required
def helloworld(request):
    ### bring back when done testing ###

    #if request.user.get_profile().is_first_login or request.user.email == 'yc@gmail.com' or request.user.email == 'lol.i.laugh@gmail.com':
    if True:
    #if not request.user.get_profile().is_first_login:
         #not first time login ANYMORE

        #####test ###
        request.user.get_profile().is_first_login = False
        request.user.get_profile().save()

        # Check which school they are from package import module
        school = request.user.get_profile().school 

        # Add user to the album
        ### not implemented yet
        #first_friend_experience.creator.add(request.user) 


        ## check if user was invited ##
        try:
            ### doesnt work
            invitations = InvitationKey.objects.filter(key=request.user.social_auth.all().get(user=request.user).uid)

            for invitee_obj in invitations:
                invitee_obj.delete() #cleanup

        except:
            invitations = 0

        #import pdb; pdb.set_trace()
        access_token = request.user.social_auth.get(user = request.user, provider = 'facebook').extra_data['access_token']
        return render_to_response('user/tutorial.html', {'school':school, 
            'access_token':access_token,
            'invitations':invitations,
            }, RequestContext(request))
    import pdb; pdb.set_trace()

#def testpost(request):
    #from facepy import GraphAPI

    #access_token = request.user.social_auth.all().get(user = request.user).extra_data['access_token']
    #graph = GraphAPI(access_token)

    #graph.post(path="https://graph.facebook.com/426364720649/feed", retry=1, message="Hello", source = " ")
#message, picture, link, name, caption, description, source, place, tags
    

@login_required
def helloworld_create(request):

    # Tutorial: user just entered friends name
    if request.method == 'POST':

        friend_name = strip_tags(request.POST['friend_name'])
        friend_id = request.POST['hash']

        #friend_form = TutorialNameForm(request.POST)
        #if friend_form.is_valid():

        friend_name = strip_tags(request.POST['friend_name'].title())
        # create first album with friend name: "My Experiences with <friend>"
        first_friend_experience = Experiences(title='Stories with '+friend_name)
        first_friend_experience.save()
        first_friend_experience.creator.add(request.user) # added to user's album

        # pass to next page (dragging memes into album)
        request.session['first_friend_experience'] = first_friend_experience

        # pass to invitation process
        request.session['friend_id'] = strip_tags(friend_id)
        request.session['friend_inv_exist'] = True
        request.session['friend_name'] = friend_name.split()[0] # Take only first name

        # create album and return for user
        response = {
            "title": first_friend_experience.title,
            "id": first_friend_experience.id
        }
        return HttpResponse(json.dumps(response), mimetype="application/json")


    # Tutorial: user can drag memes now
    #first_friend_experience = request.session['first_friend_experience']

    ## Grab College Meme user with the tutorial memes
    #college_meme_obj = User.objects.get(username = 'College Memes')

    #if request.user.get_profile().school == 'Berkeley':
        #drag_list_experience = Experiences.objects.get(title = settings.SCHOOL_UCB_ALBUM, creator = college_meme_obj) # hardcoded UCB meme album, made by user 'Berkeley Memes'(?)
    #elif request.user.get_profile().school == 'Dartmouth': 
        #drag_list_experience = Experiences.objects.get(title = settings.DARTMOUTH_ALBUM, creator = college_meme_obj) # hardcoded Dartmouth album
    #elif request.user.get_profile().school == 'Y Combinator':
        #drag_list_experience = Experiences.objects.get(title = 'YCombinator', creator = college_meme_obj) # for YC memes
    #else:
        #drag_list_experience = Experiences.objects.get(title = 'General', creator = college_meme_obj) # if nothing, default to General

    #drag_list_memes = reversed(drag_list_experience.meme_set.all())

    #return render_to_response('user/tutorial2.html',
            #{'first_friend_experience':first_friend_experience, 
                #'memes': drag_list_memes }, 
            #RequestContext(request))
    

# deprecated
# Tutorial: user makes a meme with generator
#@login_required
#def helloworld_generator(request):
    #return render_to_response('user/tutorial3.html',
            #{'friend_name': request.session['friend_name']},
            #RequestContext(request))

# Tutorial: user invites friends
#@login_required
#def helloworld_invite(request):
    ## Grab the memes in the album

    #first_friend_experience = request.session['first_friend_experience']
    #first_friend_experience_memes = reversed(first_friend_experience.meme_set.all())

    ##### New implementation for autocomplete####
    #dd = {}
    #if 'q' in request.GET:
        #dd['entered'] = request.GET.get('q')
    ##initial = {'q':"\"This is an initial value,\" said O'Leary."}
    ##autocomplete_form = SearchForm(initial=initial)
    #autocomplete_form = SearchForm()
    #dd['autocomplete_form'] = autocomplete_form

    #request.session['experience_no'] = first_friend_experience
    #return render_to_response('user/tutorial4.html',
            #{'friend_name': request.session['friend_name'], 
                #'memes': first_friend_experience_memes,
                #'first_friend_experience': first_friend_experience,
                #'autocomplete_form':autocomplete_form},
            #RequestContext(request))


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

        #### New implementation for autocomplete####
        dd = {}
        if 'q' in request.GET:
            dd['entered'] = request.GET.get('q')
        #initial = {'q':"\"This is an initial value,\" said O'Leary."}
        #autocomplete_form = SearchForm(initial=initial)
        autocomplete_form = SearchForm()
        dd['autocomplete_form'] = autocomplete_form

        # Grabs memes within the experience albums
            # reverse order: newest memes are on top
        memes = reversed(experiences.meme_set.all())



        ### TEMP ###
        berkeley = 0 
        dartmouth = 0 
        ## end ##

        ###### BRING UP SCHOOL FEED ######
        # Find College Meme user w/ school memes
        college_meme_obj = User.objects.get(username = 'College Memes')

        user_school = request.user.get_profile().school
        if user_school == 'Berkeley':
            drag_list_experience = Experiences.objects.get(title = settings.SCHOOL_UCB_ALBUM, creator = college_meme_obj) 

            #temp
            berkeley = drag_list_experience
        elif user_school == 'Dartmouth': 
            drag_list_experience = Experiences.objects.get(title = settings.SCHOOL_DARTMOUTH_ALBUM, creator = college_meme_obj) 


            #temp
            dartmouth = drag_list_experience
        else:
            drag_list_experience = Experiences.objects.get(title = 'General', creator = college_meme_obj) # if nothing, default to General

        school_feed_memes = drag_list_experience.meme_set.all().order_by('-id')

        return invite(request, success_url, form_class, template_name, extra_context={'experiences':experiences, 'memes':memes, 'autocomplete_form':autocomplete_form,
            'user_school': user_school, 'is_album':1})

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
            # grab college meme user first
            college_meme_obj = User.objects.get(username = 'College Memes')


            # if meme from public SCHOOL feed is dragged, let anybody do it. BUT DONT CANNABLIZE the meme.
            if dragged_meme_obj.e.filter(title = settings.SCHOOL_UCB_ALBUM, creator = college_meme_obj).count() or dragged_meme_obj.e.filter(title = settings.SCHOOL_DARTMOUTH_ALBUM, creator = college_meme_obj).count() or dragged_meme_obj.e.filter(title = 'YCombinator', creator = college_meme_obj).count() or dragged_meme_obj.e.filter(title = 'General', creator = college_meme_obj).count():
                dragged_meme_obj.e.add(dropped_album_obj)
                return HttpResponse('you dragged a meme from school feed')

            ## check for school feed ##
            # if public SCHOOL feed then anybody can drag a meme in
            elif dropped_album_obj.title == settings.SCHOOL_UCB_ALBUM and college_meme_obj in dropped_album_obj.creator.all():
                dragged_meme_obj.e.add(dropped_album_obj)
                return HttpResponse('you dropped a meme into school feed')

            # if public SCHOOL feed then anybody can drag a meme in
            elif dropped_album_obj.title == settings.SCHOOL_DARTMOUTH_ALBUM and college_meme_obj in dropped_album_obj.creator.all():
                dragged_meme_obj.e.add(dropped_album_obj)
                return HttpResponse('you dropped a meme into school feed')

            # if public SCHOOL feed then anybody can drag a meme in
            elif dropped_album_obj.title == settings.YCOMBINATOR and college_meme_obj in dropped_album_obj.creator.all():
                dragged_meme_obj.e.add(dropped_album_obj)
                return HttpResponse('you dropped a meme into school feed')

            # if public SCHOOL feed then anybody can drag a meme in
            elif dropped_album_obj.title == settings.GENERAL and college_meme_obj in dropped_album_obj.creator.all():
                dragged_meme_obj.e.add(dropped_album_obj)
                return HttpResponse('you dropped a meme into school feed')
            ## end ##

            # otherwise, check if user owns the album
            elif request.user == dragged_meme_obj.creator and request.user.experiences_set.filter(pk=dropped_album_id).count():
                dragged_meme_obj.e.add(dropped_album_obj)

                # If no album profile pic, add it
                if not dropped_album_obj.album_pic: 
                    dropped_album_obj.album_pic = dragged_meme_obj # adding instance
                    dropped_album_obj.save()

            #updated_meme_count = dropped_album_obj.meme_set.count
                return HttpResponse('success')
            #return render_to_response('user/experience_display.html')

            return HttpResponse('forbidden')
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
                messages.add_message(request, messages.SUCCESS, 'Success! You deleted the meme', extra_tags="text-success")

                return HttpResponseRedirect(reverse('webapp_index'))
            else:
                # Meme does not belong to user
                return render_to_response('profile/access_denied.html', RequestContext(request))
        except:
            # Meme does not exist
            return render_to_response('profile/access_denied.html', RequestContext(request))

# view called when user clicks a meme on the feed to see the node.
def recreate_map(request, meme_id=None):

    # User clicked a meme while Fancybox was open (a node)
    if request.method == 'POST':
        meme_active_id = strip_tags(request.POST['meme_active_id'])

        selected_meme = Meme.objects.get(pk=meme_id)

        # sanitize to see if it came from original perspective
        if meme_active_id in selected_meme.meme_horizontal.all():
            return render_to_response('meme/meme_node_map_load.html',
                    {'selected_meme':selected_meme
                        },
                    RequestContext(request))

    # User clicked a meme on feed to open 
    if meme_id:
        # Query for the meme
        try:
            selected_meme = Meme.objects.get(pk=meme_id)
        except:
            # Something went wrong!
            return render_to_response('500.html', RequestContext(request))

        uncat_memes = Meme.objects.filter(creator = request.user, e = None)
        
        horizontal_memes = selected_meme.meme_horizontal.all()
        vertical_memes = selected_meme.meme_vertical

        # Filter out memes already added
        if vertical_memes:
            uncat_memes_filter = reversed(uncat_memes.exclude(id__in = [o.id for o in horizontal_memes]).exclude(id = vertical_memes.id).exclude(id = selected_meme.id))
        else:
            uncat_memes_filter = reversed(uncat_memes.exclude(id__in = [o.id for o in horizontal_memes]).exclude(id = selected_meme.id))

        return render_to_response('meme/meme_node_map.html',
                {'selected_meme':selected_meme,
                'uncat_memes': uncat_memes_filter,
                    },
                RequestContext(request))

# drag meme into the node and update server
@login_required
def add_meme_to_node(request):
    if request.is_ajax():
        if request.method == 'POST':
            dragged_meme_id = strip_tags(request.POST['meme'])
            add_type = strip_tags(request.POST['type'])
            meme_node = strip_tags(request.POST['meme_node'])
            
            # discover obj for drag and drop
            selected_meme = Meme.objects.get(pk=meme_node) # meme that was opened in fancybox
            dragged_meme_obj = Meme.objects.get(pk=dragged_meme_id) # meme that was dragged from uncat

            if add_type == 'horizontal':

                # first add connections to every permutation of DRAGGED MEME PERSPECTIVE
                for node in dragged_meme_obj.meme_horizontal.all():
                    node.meme_horizontal.add(selected_meme)

                # ADD CONNECTIONS TO OPENED MEMES PERSPECTIVE
                for node in selected_meme.meme_horizontal.all():
                    node.meme_horizontal.add(dragged_meme_obj)

                # add connection to original
                selected_meme.meme_horizontal.add(dragged_meme_obj) 

                return HttpResponse('success')

            if add_type == 'vertical':
                # just add 1 node
                selected_meme.meme_vertical = dragged_meme_obj
                selected_meme.save()

                return HttpResponse('success')



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
            messages.add_message(request, messages.SUCCESS, 'Success! You deleted the album', extra_tags="text-success")

            return HttpResponseRedirect(reverse('webapp_index'))
        except:
            # User does not have access to album or DNE
            return render_to_response('profile/access_denied.html', RequestContext(request))

# Registration - checks for email duplicates
def validate_email_duplicate(request):
    post_email = strip_tags(request.POST['email'])
    
    # find if an account with that email already exists
    try:
        user = User.objects.get(email__exact=post_email)
        response_str = "false"
    except User.DoesNotExist:
        response_str = "true" # response for jQuery validate to parse

    return HttpResponse(response_str)

def fb_privacy_explanation(request):
    return render_to_response('meme/ohwhy.html', RequestContext(request))

def custom_404(request):
    return render_to_response('400.html', RequestContext(request))

def custom_500(request, template_name='500.html'):
    return render_to_response(template_name, RequestContext(request))

# tracking page for admins
def privatetracking(request):
    if request.user.username == 'Delos Chang' or request.user.username == 'Delos-Chang-1' or request.user.username == 'Max Frenkel' or request.user.username == 'deloschang':
        readlogfile = open(os.path.join(settings.STATIC_ROOT, 'login_track.txt'), 'r+').read()
        readregfile = open(os.path.join(settings.STATIC_ROOT, 'registration_track.txt'), 'r+').read()
        return render_to_response('privatetracking.html', {'readlogfile':readlogfile, 'readregfile':readregfile}, RequestContext(request))

def userlist(request):
    if 'Delos' in request.user.username or 'Frenkel' in request.user.username == 'Max Frenkel':

        handle=open(os.path.join(settings.STATIC_ROOT, 'userlist.txt'), 'r+')
        for userobj in User.objects.all():
            handle.write(userobj.username +'......  email: ' + userobj.email)
            try: 
                fb_id = userobj.social_auth.all().get(user = userobj).uid # grab fb id
                handle.write('......http://facebook.com/'+fb_id+'\n')
            except:
                handle.write('\n')

        handle.close()

        readuserlist = open(os.path.join(settings.STATIC_ROOT, 'userlist.txt'), 'r+').read()
        return render_to_response('privatetracking.html', {'readlogfile':readuserlist, 'readregfile':0}, RequestContext(request))
