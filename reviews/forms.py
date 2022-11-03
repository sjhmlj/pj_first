from .models import Movie,Review,Comment
from django import forms

class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'
        exclude = ['opening_date']

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'title',
            'content',
        ]
        labels = {
            'title':'제목',
            'content':'내용',
            'grade':'평점'
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        labels = {
            'content':'댓글 작성'
        }
