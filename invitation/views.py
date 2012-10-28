from django.conf import settings
from django.views.generic.simple import direct_to_template

# modify to allow extra_context for invite function
from django.template import RequestContext
from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth.models import User

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

    # User entered in field and invited friend
    if request.method == 'POST':
        #import pdb;
        #pdb.set_trace()

        ### foreign key ==> request.POST['q']
        ### email ==> request.POST['q_text']

        #form = form_class(data=request.POST, files=request.FILES)

        post_values = request.POST.copy()
        post_values['email'] = post_values['q_text'] # copy email from input into email for form

        # some autocomplete for existing users selected (e.g. |2|3|4|)
        if post_values['q'] != "":

            auto_list = post_values['q'].split('|')  # sep list of users

            linked_experience = request.session['experience_no']  # find selected album
            for invited_existing_user_pk in auto_list[1:len(auto_list)-1]:  # slice off first | and last |

                invited_existing_user = User.objects.get(pk=invited_existing_user_pk)
                linked_experience.creator.add(invited_existing_user) 

        # If an email value was entered
        if post_values['email'] != "":
            # for email invitation processing
            form = form_class(data=post_values, files=request.FILES)

            # check if email is valid
            if form.is_valid():
                # Check for album number
                if request.session['experience_no']:
                    invitation = InvitationKey.objects.create_invitation(request.user, form.cleaned_data["email"], request.session['experience_no'])
                    invitation.send_to(form.cleaned_data["email"], request.user, request.session['experience_no'])

                    # success_url needs to be dynamically generated here; setting a
                    # a default value using reverse() will cause circular-import
                    # problems with the default URLConf for this application, which
                    # imports this file.

        # Add a message that is output in templates/profile.html
        messages.add_message(request, messages.INFO, 'Hooray! You invited your friend')
        return HttpResponseRedirect(success_url or reverse('webapp_index'))

    else:
        # Show standard experience_display.html page

        form = form_class()
        request.session['experience_no'] = extra_context['experiences']


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
