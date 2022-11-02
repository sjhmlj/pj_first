from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    cast = models.TextField()
    producer = models.CharField(max_length=20)
    opening_date = models.DateField()
    image = ProcessedImageField(blank=False, upload_to='images/', processors=[Thumbnail(300, 400)], format='JPEG', options={'quality':80})

class Review(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    grade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="0~5사이 값으로 입력하세요",)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(get_user_model(), related_name='like_reviews')

class Comment(models.Model):
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(get_user_model(), related_name='like_comments')