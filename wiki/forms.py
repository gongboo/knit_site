from django import forms
from .models import WikiPost


from django_summernote.widgets import SummernoteWidget

class WikiPostForm(forms.ModelForm):
    class Meta:
        model = WikiPost
        fields = ['name', 'content']
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'placeholder': '제목을 적어주세요', 
                    'style': 'width: 100%; margin-bottom:10px;', 
                    'class': 'form-control'
                }
            ),
            'content': SummernoteWidget(),
        }
