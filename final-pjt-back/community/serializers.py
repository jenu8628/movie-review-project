from rest_framework import serializers
from .models import MovieReview,MovieComment,Post,PostComment


class MovieReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MovieReview
        # 'like',
        fields = ('username','id', 'rank', 'content', 'movie_title', 'title','created_at')


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ('username','id','content', 'title','created_at')


class MovieCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MovieComment
        fields = ('username','id','content',)


class PostCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PostComment
        fields = ('username','content','id')
