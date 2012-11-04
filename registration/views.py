"""
Views which allow users to create and activate accounts.

"""


from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from registration.backends import get_backend

from django.contrib.auth.models import User

# for mailing admins
#from django.core.mail import send_mail
#from django.conf import settings

from datetime import datetime
import os
from django.conf import settings

# skip to login
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# for messages
from django.contrib import messages



def activate(request, backend,
             template_name='registration/activate.html',
             success_url=None, extra_context=None, **kwargs):
    """
    Activate a user's account.

    The actual activation of the account will be delegated to the
    backend specified by the ``backend`` keyword argument (see below);
    the backend's ``activate()`` method will be called, passing any
    keyword arguments captured from the URL, and will be assumed to
    return a ``User`` if activation was successful, or a value which
    evaluates to ``False`` in boolean context if not.

    Upon successful activation, the backend's
    ``post_activation_redirect()`` method will be called, passing the
    ``HttpRequest`` and the activated ``User`` to determine the URL to
    redirect the user to. To override this, pass the argument
    ``success_url`` (see below).

    On unsuccessful activation, will render the template
    ``registration/activate.html`` to display an error message; to
    override thise, pass the argument ``template_name`` (see below).

    **Arguments**

    ``backend``
        The dotted Python import path to the backend class to
        use. Required.

    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context. Optional.

    ``success_url``
        The name of a URL pattern to redirect to on successful
        acivation. This is optional; if not specified, this will be
        obtained by calling the backend's
        ``post_activation_redirect()`` method.
    
    ``template_name``
        A custom template to use. This is optional; if not specified,
        this will default to ``registration/activate.html``.

    ``\*\*kwargs``
        Any keyword arguments captured from the URL, such as an
        activation key, which will be passed to the backend's
        ``activate()`` method.
    
    **Context:**
    
    The context will be populated from the keyword arguments captured
    in the URL, and any extra variables supplied in the
    ``extra_context`` argument (see above).
    
    **Template:**
    
    registration/activate.html or ``template_name`` keyword argument.
    
    """
    backend = get_backend(backend)
    account = backend.activate(request, **kwargs)

    if account:
        # activated, first time logging in 
        account.backend = 'django.contrib.auth.backends.ModelBackend' # manual patch to avoid authenticate
        user = login(request, account) # log in user now

        # record it for admins
        date = []
        date.append(str(datetime.now()))

        with open(os.path.join(settings.STATIC_ROOT, 'registration_track.txt'), "a") as text_file:
            text_file.write(date[0]+'    '+account.username+' activated\n')

        # check if first login (probably are - just to be safe)
        if request.user.get_profile().is_first_login:
            # send to the tutorial
            messages.add_message(request, messages.SUCCESS, 'Woohoo!  This is your brand, spanking new account', extra_tags="text-success")
            return HttpResponseRedirect(reverse('webapp_helloworld'))

        #if success_url is None:
            #to, args, kwargs = backend.post_activation_redirect(request, account)
            #return redirect(to, *args, **kwargs)
        #else:
            #return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)


def register(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='landing.html',
             extra_context=None):
    """
    Allow a new user to register an account.

    The actual registration of the account will be delegated to the
    backend specified by the ``backend`` keyword argument (see below);
    it will be used as follows:

    1. The backend's ``registration_allowed()`` method will be called,
       passing the ``HttpRequest``, to determine whether registration
       of an account is to be allowed; if not, a redirect is issued to
       the view corresponding to the named URL pattern
       ``registration_disallowed``. To override this, see the list of
       optional arguments for this view (below).

    2. The form to use for account registration will be obtained by
       calling the backend's ``get_form_class()`` method, passing the
       ``HttpRequest``. To override this, see the list of optional
       arguments for this view (below).

    3. If valid, the form's ``cleaned_data`` will be passed (as
       keyword arguments, and along with the ``HttpRequest``) to the
       backend's ``register()`` method, which should return the new
       ``User`` object.

    4. Upon successful registration, the backend's
       ``post_registration_redirect()`` method will be called, passing
       the ``HttpRequest`` and the new ``User``, to determine the URL
       to redirect the user to. To override this, see the list of
       optional arguments for this view (below).
    
    **Required arguments**
    
    None.
    
    **Optional arguments**

    ``backend``
        The dotted Python import path to the backend class to use.

    ``disallowed_url``
        URL to redirect to if registration is not permitted for the
        current ``HttpRequest``. Must be a value which can legally be
        passed to ``django.shortcuts.redirect``. If not supplied, this
        will be whatever URL corresponds to the named URL pattern
        ``registration_disallowed``.
    
    ``form_class``
        The form class to use for registration. If not supplied, this
        will be retrieved from the registration backend.
    
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    ``success_url``
        URL to redirect to after successful registration. Must be a
        value which can legally be passed to
        ``django.shortcuts.redirect``. If not supplied, this will be
        retrieved from the registration backend.
    
    ``template_name``
        A custom template to use. If not supplied, this will default
        to ``registration/registration_form.html``.
    
    **Context:**
    
    ``form``
        The registration form.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    registration/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    backend = get_backend(backend)
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)



    if request.method == 'POST':
        # User registering

        # copying POST values because POST is immutable
        post_values = request.POST.copy()
        post_values['username'] = post_values['username'].title()
        post_values['password2'] = post_values['password1'] # fix for 2nd 'type again' pass

        # Check if user is using invitation
        if not request.POST.get('email', False) and request.session['email']:
            # User uses invitation so replace email
            #post_values['email'] = request.session['email']
            post_values['email'] = request.session['invite_key']+'@dartmouth.edu' # hack for non-BDNYU users


        form = form_class(data=post_values, files=request.FILES)
        if form.is_valid():

            # Check for invitation -- hack in email to avoid regex in forms.py
            if request.session.get('email', False):
                form.cleaned_data['email'] = request.session['email']       # hack for non-BDNYU users

            new_user = backend.register(request, **form.cleaned_data)

            # Save hyphenated name for URL
            count_existing = User.objects.filter(username__iexact=new_user.username).count() # count existing duplicates
            new_reg_count = count_existing + 1 # add 1 for new user
            url_username = post_values['username'].replace(' ','-').lower()+'-'+str(new_reg_count)

            new_user_profile = new_user.get_profile()
            new_user_profile.url_username = url_username

            # Check if Berkeley/Dartmouth
            if 'berkeley.edu' in new_user.email:
                new_user_profile.school = 'Berkeley'
            elif 'dartmouth.edu' in new_user.email:
                new_user_profile.school = 'Dartmouth'

            new_user_profile.save()


            ####### send an email to admins #######
            #if not settings.DEBUG:
                #subject = 'New login'
                #message = request.user.username+' logged in with '+request.user.email
                #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['memeja@googlegroups.com'], fail_silently=True)
            ####### end #######

            date = []
            date.append(str(datetime.now()))

            with open(os.path.join(settings.STATIC_ROOT, 'registration_track.txt'), "a") as text_file:
                text_file.write(date[0]+'    '+new_user.username+' registered with '+new_user.email+'\n')

            # Check if user is coming from invited album
            if request.session.get('invited_album', False):
            # add invitee into album 'creator'
                linked_experience = request.session['invited_album']
                linked_experience.creator.add(new_user)

            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)


    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)
