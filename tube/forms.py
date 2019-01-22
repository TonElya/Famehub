from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Video
from django.forms import ModelForm
from django.utils.safestring import mark_safe
#from froala_editor.widgets import FroalaEditor
#from ckeditor.widgets import CKEditorWidget


class VideoCreationForm(ModelForm):
    #body=forms.CharField(widget=CKEditorWidget())#(widget=FroalaEditor)
    # username = forms.CharField(max_length=200,
    # widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})))
    class Meta:
        model =Video
        fields = ('title','vid_desc','video','link')

class VideoChangeForm(ModelForm):
    #body=forms.CharField(widget=CKEditorWidget())#(widget=FroalaEditor)
    class Meta:
        model = Video
        fields = ('title','vid_desc','video','link','user')

