from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "nickname",
            'profile_image',
        ]
        labels = {
            'username': '아이디',
            'nickname': '닉네임',
            'profile_image': '프로필 사진(선택)',
        }


class CustomUserChangeForm(UserChangeForm):
    password = None  ## profile_update에서 password를 없애기 위함. exclude로는 안됨.

    class Meta:
        model = get_user_model()
        fields = [
            "nickname",
            "email",
            "profile_image",
        ]
        labels = {
            'nickname': '닉네임',
            'email': '이메일',
            'profile_image': '프로필 사진',
        }