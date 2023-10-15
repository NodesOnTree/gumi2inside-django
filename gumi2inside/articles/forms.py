from django import forms
from .models import Poll, Choice


class PollAddForm(forms.ModelForm):

    choice1 = forms.CharField(label='항목 1', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(label='항목 2', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ['title','text', 'choice1', 'choice2']
        labels = {
            'title': '제목',
            'text': '내용',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text', ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        labels = {
            'choice_text': '보기',
            
        }
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
        }
