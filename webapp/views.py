from django.shortcuts import render_to_response
from django.template import RequestContext

# for file uploader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from webapp.models import *
from webapp.forms import *

# for registration
from registration.views import register

# Home URL
def index(request, backend, success_url=None, 
        form_class=None, profile_callback=None,
        template_name='landing.html',
        extra_context=None):

    # Show landing page with registration 
    if not request.user.is_authenticated():
        return register(request, backend, success_url, form_class, profile_callback, template_name, extra_context)
    else:

        # SHOW PROFILE PAGE 

        # grabs uncategorized memes from the database
        memes = Meme.objects.all()
        
        # grabs existing experiences/albums from the database
        experiences = Experiences.objects.all()

        # form to create new experience/album
        addexperienceform = AddExperienceForm()
        
        return render_to_response(
                'profile.html',
                {'memes': memes, 'experiences': experiences, 'addexperienceform': addexperienceform},
                RequestContext(request))

# Upload a Meme 
def create(request):
    #import pdb; pdb.set_trace()

    # Handle file upload
    if request.method == 'POST':
        imageform = ImageUploadForm(request.POST, request.FILES)

        if imageform.is_valid():
            newimage = Meme(image = request.FILES['image'])
            newimage.save()

            testalbum = Experiences.objects.get(pk=1)

            #
            # Move to dragging functionality
            #
            newimage.e.add(testalbum)

            #redirect('webapp.views.index')
            return HttpResponseRedirect(reverse('memeja_index'))
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
def add_experience(request):
    #import pdb;
    if request.method == 'POST':
        # add experience into database
        
        new_experience_form = AddExperienceForm(request.POST)
        if new_experience_form.is_valid(): 
            post = request.POST

            # adds the title into database
            new_experience = Experiences(title = request.POST['title'])
            new_experience.save()
            return HttpResponseRedirect(reverse('memeja_index'))

def show_experience(request, pk):
    experiences = Experiences.objects.get(pk=pk)

    # Grabs memes within the experience albums
    memes = experiences.meme_set.all()
    return render_to_response(
        'user/experience_display.html', 
        {'experiences' : experiences, 'memes' : memes},
        context_instance = RequestContext(request)
    ) 
