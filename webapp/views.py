from django.shortcuts import render_to_response
from django.template import RequestContext

# for file uploader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from webapp.models import Document
from webapp.forms import DocumentForm

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
        return render_to_response('profile.html', RequestContext(request))

def create(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('webapp.views.create'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    #documents = Document.objects.all()
    documents = False;

    # Render list page with the documents and the form
    return render_to_response(
        'user/create.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


