from .models import Movie,Review,Comment
from django import forms

class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'
        exclude = ['opening_date']
        labels = {
            'title': '영화제목',
            'content': '줄거리',
            'running_time':'상영시간(분)',
            'cast':'출연진',
            'producer':'감독',
            'trailer_url':'예고편URL (유튜브 URL의 v= 뒤의 값을 embed/뒤에 넣어주세요.)',
            'image':'포스터이미지',
        }

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
