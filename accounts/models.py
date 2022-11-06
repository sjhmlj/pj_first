from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    profile_image = ProcessedImageField(
        upload_to="profile_images/",
        blank=True,
        processors=[ResizeToFill(120, 120)],  ## 유튜브 프로필 이미지 크기 120x120
        format="JPEG",
        options={"quality": 60},  ## 구글링한 프로필 이미지 퀄리티가 대체로 60으로 되어 있었음
    )
