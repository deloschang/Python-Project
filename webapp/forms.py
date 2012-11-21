from django import forms
from ajax_select.fields import AutoCompleteSelectMultipleField

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class AddExperienceForm(forms.Form):
    title = forms.CharField(max_length=60,
                                widget=forms.TextInput(attrs={'placeholder': 'Our Shared Experience'}))

class InvitationKeyForm(forms.Form):
    email = forms.EmailField()

class SearchForm(forms.Form):

    #q = AutoCompleteField(
    #q = AutoCompleteSelectField(
    q = AutoCompleteSelectMultipleField(
            'label',
            required=True,
            help_text="Invite via email or add an existing user",
            label="",
            #attrs={'size': 100}
            )

class TutorialNameForm(forms.Form):
    friend_name = forms.CharField(max_length=70,
                                widget=forms.TextInput(attrs={'placeholder': 'Friend\'s name'}))
