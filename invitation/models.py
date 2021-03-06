import os
import random
import datetime

# manually imported to fix naive and aware comparisons
from django.utils import timezone

from django.db import models
from django.conf import settings
from django.utils.http import int_to_base36
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from registration.models import SHA1_RE

# link invitation with the album that is shared
from webapp.models import Experiences

class InvitationKeyManager(models.Manager):
    def is_key_valid(self, invitation_key):
        """
        Check if an ``InvitationKey`` is valid or not, returning a boolean,
        ``True`` if the key is valid.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(invitation_key):
            try:
                invitation_key = self.get(key=invitation_key)
            except self.model.DoesNotExist:
                return False
            return not invitation_key.key_expired()
        return False

    def create_invitation(self, user, from_user_album):
        """
        Create an ``InvitationKey`` and returns it.
        
        The key for the ``InvitationKey`` will be a SHA1 hash, generated 
        from a combination of the ``User``'s username and a random salt.
        """
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        key = sha_constructor(salt+user.username).hexdigest()
        return self.create(from_user=user, key=key, from_user_album=from_user_album) 

    def remaining_invitations_for_user(self, user):
        """
        Returns the number of remaining invitations for a given ``User``.
        """

        # able to tell number of invitations
            # distinguish between DBN users and non ... 

        # if DBN user then create invitation key with other object..
        inviteds_count = self.filter(from_user=user).count()
        return settings.INVITATIONS_PER_USER - inviteds_count

    def delete_expired_keys(self):
        for key in self.all():
            if key.key_expired():
                key.delete()


class InvitationKey(models.Model):
    key = models.CharField(_('invitation key'), max_length=40)
    date_invited = models.DateTimeField(_('date invited'), 
                                        default=datetime.datetime.now)
    from_user = models.ForeignKey(User)
    from_user_album = models.ForeignKey(Experiences, null=True) # album that User1 invites invitee to join
    #to_user_email = models.EmailField() # email of invite recipient from form
    
    
    objects = InvitationKeyManager()
    
    def __unicode__(self):
        return u"Invitation from %s on %s" % (self.from_user.username, self.date_invited)
    
    def key_expired(self):
        """
        Determine whether this ``InvitationKey`` has expired, returning 
        a boolean -- ``True`` if the key has expired.
        
        The date the key has been created is incremented by the number of days 
        specified in the setting ``ACCOUNT_INVITATION_DAYS`` (which should be 
        the number of days after invite during which a user is allowed to
        create their account); if the result is less than or equal to the 
        current date, the key has expired and this method returns ``True``.
        
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_INVITATION_DAYS)
        return self.date_invited + expiration_date <= timezone.now()
    key_expired.boolean = True
    
    def send_to(self, email, user, album):
        """
        Send an invitation email to ``email``.
        """
        subject = render_to_string('invitation/invitation_email_subject.txt',
                                   { 'from_user': user,
                                     'album': album,
                                       })
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message = render_to_string('invitation/invitation_email.txt',
                                   { 'invitation_key': self.key,
                                     'from_user': user,
                                     'album': album,
                                     'expiration_days': settings.ACCOUNT_INVITATION_DAYS,
                                     })
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        
