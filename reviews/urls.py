from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('<int:pk>/movie_update/', views.movie_update, name='movie_update'),
    path('<int:pk>/review_create/', views.review_create, name='review_create'),
    path('<int:movie_pk>/review/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/review/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:movie_pk>/review/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/review/<int:review_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/review/<int:review_pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
    path('<int:movie_pk>/review/<int:review_pk>/like', views.like, name='like'),

]