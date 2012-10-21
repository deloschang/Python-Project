# required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q

# for login required
from django.contrib.auth.decorators import login_required

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
        
        return render_to_response(
                'profile.html',
                {'memes': memes, 'experiences': experiences, 'addexperienceform': addexperienceform},
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
            #{'documents': documents, 'form': form},
            {'form': imageform},
            context_instance=RequestContext(request)
        )


# Add new album for user   

@login_required
def add_experience(request):
    #import pdb;
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



