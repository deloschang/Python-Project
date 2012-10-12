from django import forms

#class ImageUploadForm(forms.Form):
    #"""Image upload form."""
    #image = forms.ImageField()

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a field',
        help_text='max. 42 meg'
    )

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class AddExperienceForm(forms.Form):
    title = forms.CharField(max_length=60)

class InvitationKeyForm(forms.Form):
    email = forms.EmailField()
