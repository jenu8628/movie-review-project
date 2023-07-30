from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('movie_review_list_create/',views.movie_review_list_create),
    path('movie_review_list_order_by_like/',views.movie_review_list_order_by_like),
    path('movie_review_update_delete/<int:movie_review_pk>/',views.movie_review_update_delete),
    path('movie_review_comment_create/<int:movie_review_pk>/',views.movie_review_comment_create),
    path('movie_review_comment_delete/<int:comment_pk>/',views.movie_review_comment_delete),
    
    path('get_user_movie_reviews/<int:movie_review_pk>/',views.get_user_movie_reviews),
    path('get_user_reviews/',views.get_user_reviews),
    path('get_movie_review_comments/<int:movie_review_pk>/',views.get_movie_review_comments),
    path('like_movie_review/<int:movie_review_pk>/',views.like_movie_review),
    
    path('post_list_create/',views.post_list_create),
    path('post_list_order_by_like/',views.post_list_order_by_like),
    path('post_update_delete/<int:post_pk>/',views.post_update_delete),
    path('post_comment_create/<int:post_pk>/',views.post_comment_create),
    path('post_comment_delete/<int:comment_pk>/',views.post_comment_delete),

    path('get_user_posts/<int:post_pk>/',views.get_user_posts),
    path('get_post_comments/<int:post_pk>/',views.get_post_comments),
    path('like_post/<int:post_pk>/',views.like_post),

    path('get_movie_info/<str:search_value>',views.get_movie_info),
]