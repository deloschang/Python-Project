from django.conf import settings
from django.views.generic.simple import direct_to_template

# modify to allow extra_context for invite function
from django.template import RequestContext
from django.shortcuts import render

from django.contrib import messages

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from registration.views import register as registration_register
from registration.forms import RegistrationForm

from invitation.models import InvitationKey
from invitation.forms import InvitationKeyForm

is_key_valid = InvitationKey.objects.is_key_valid

# TODO: move the authorization control to a dedicated decorator

def invite(request, success_url=None,
            form_class=InvitationKeyForm,
            template_name='invitation/invitation_form.html', extra_context=None):
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            invitation = InvitationKey.objects.create_invitation(request.user)
            invitation.send_to(form.cleaned_data["email"])
            # success_url needs to be dynamically generated here; setting a
            # a default value using reverse() will cause circular-import
            # problems with the default URLConf for this application, which
            # imports this file.


            # Add a message that is output in templates/profile.html
            messages.add_message(request, messages.INFO, 'Hooray! You invited your friend')
            return HttpResponseRedirect(success_url or reverse('webapp_index'))
    else:
        form = form_class()

    # add extra context to load memes and experiences in 
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = value

    return render(request, template_name, {
        'form': form,
        'remaining_invitations': InvitationKey.objects.remaining_invitations_for_user(request.user),
    }, context_instance=context)
invite = login_required(invite)
