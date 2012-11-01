from django import forms
from ajax_select.fields import AutoCompleteSelectMultipleField

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class AddExperienceForm(forms.Form):
    title = forms.CharField(max_length=60)

class InvitationKeyForm(forms.Form):
    email = forms.EmailField()

class SearchForm(forms.Form):

    #q = AutoCompleteField(
    #q = AutoCompleteSelectField(
    q = AutoCompleteSelectMultipleField(
            'label',
            required=True,
            help_text="Enter name or email. Or leave email in input box to invite",
            label="Invite users to album",
            #attrs={'size': 100}
            )
