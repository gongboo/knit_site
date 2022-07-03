from django import forms
from .models import Post, Pattern, CommentForPost


from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title':forms.TextInput(
                attrs={
                    'placeholder': '제목을 적어주세요', 
                    'style': 'width: 100%;margin-bottom:10px;', 
                    'class': 'form-control'
                }
            ),
            'content': SummernoteWidget(),
        }

class CommentForPostForm(forms.ModelForm):
    class Meta:
        model = CommentForPost
        fields = ['content']
        widgets={'content':forms.TextInput(
                attrs={
                    'placeholder': '댓글을 적어주세요', 
                    'style': 'width: 100%; margin-bottom:10px;', 
                    'class': 'form-control'
                }
            ),
        }

class PatternForm(forms.ModelForm):
    class Meta:
        model = Pattern
        fields = ['title', 'comment','color_list','pattern_list','row_length','col_length']
        widgets = {
            'color_list': forms.HiddenInput(
                attrs={'id': 'color_list'} 
            ),
            'pattern_list': forms.HiddenInput(
                attrs={'id': 'pattern_list'}
            ),
            'row_length': forms.HiddenInput(
                attrs={'id': 'row_length'}
            ),
            'col_length': forms.HiddenInput(
                attrs={'id': 'col_length'}
            ),
            'title':forms.TextInput(
                attrs={
                    'placeholder': '제목을 적어주세요', 
                    'style': 'width: 100%;', 
                    'class': 'form-control'
                }
            ),
            'comment':forms.TextInput(
                attrs={
                    'placeholder': '설명을 적어주세요', 
                    'style': 'width: 100%; height:80px;', 
                    'class': 'form-control',
                    
                }
            ),
        }
    # def patternListToJson(self):
    #     pattern_list=json.dumps({"pattern_list":request.POST.get('pattern_list').split(',')})
    #     return pattern_list
    
    # def colorListToJson(self):
    #     color_list=json.dumps({"color_list":request.POST.get('color_list').split(',')})
    #     return color_list
