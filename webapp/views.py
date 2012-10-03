from django.shortcuts import render_to_response
from django.template import RequestContext

# for file uploader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from webapp.models import Document, Meme
from webapp.forms import DocumentForm, ImageUploadForm

# for registration
from registration.views import register

def index(request, backend, success_url=None, 
        form_class=None, profile_callback=None,
        template_name='landing.html',
        extra_context=None):
    if not request.user.is_authenticated():
        # logic to show landing page with 
        return register(request, backend, success_url, form_class, profile_callback, template_name, extra_context)
    else:
        # logic to show albums/profile page

        # show uncategorized memes on the profile 
        memes = Meme.objects.all()
        return render_to_response(
                'profile.html',
                {'memes': memes},
                RequestContext(request))

def create(request):
    #import pdb; pdb.set_trace()
    # Handle file upload
    if request.method == 'POST':
        imageform = ImageUploadForm(request.POST, request.FILES)

        if imageform.is_valid():
            newimage = Meme(image = request.FILES['image'])
            newimage.save()

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


