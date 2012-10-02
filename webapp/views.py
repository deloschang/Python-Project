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
        #return render_to_response('landing.html', RequestContext(request))
        return register(request, backend, success_url, form_class, profile_callback, template_name, extra_context)
    else:
        # logic to show albums
        return render_to_response('base.html', RequestContext(request))

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('webapp.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    #documents = Document.objects.all()
    documents = False;

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


