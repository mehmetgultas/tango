#-*-coding:utf-8-*-
from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length = 128, help_text = 'Lutfen bir kategori ismi girin')
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    likes = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)

    class Meta:
        model = Category

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length = 128, help_text = 'lutfen sayfanin basligini yaziniz')
    url = forms.URLField(max_length = 200, help_text = 'lutfen sayfanin internet adresini yaziniz')
    views = forms.IntegerField(widget = forms.HiddenInput(), initial = 0)
    
    class Meta:
        model = Page
        fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data
