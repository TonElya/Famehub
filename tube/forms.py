from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Video
from django.forms import ModelForm
from django.utils.safestring import mark_safe
#from froala_editor.widgets import FroalaEditor
#from ckeditor.widgets import CKEditorWidget

from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')


class VideoCreationForm(ModelForm):
    #body=forms.CharField(widget=CKEditorWidget())#(widget=FroalaEditor)
    # username = forms.CharField(max_length=200,
    # widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})))
    video = forms.FileField(required=False, validators=[file_size])
    class Meta:
        model =Video
        fields = ('title','vid_desc','video')

video = forms.FileField(required=False, validators=[file_size])
class VideoChangeForm(ModelForm):
    #body=forms.CharField(widget=CKEditorWidget())#(widget=FroalaEditor)
    class Meta:
        model = Video
        fields = ('title','vid_desc','video','link','user')

