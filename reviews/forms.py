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
            'grade',
        ]

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'content',
        ]