from .models import Movie,Review,Comment
from django import forms

class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'title',
            'content',
            'movie',
            'grade',
        ]

class CommentForm(forms.ModelsForm):

    class Meta:
        model = Comment
        fields = [
            'content',
        ]