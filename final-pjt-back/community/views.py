from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication 
from .serializers import MovieReviewSerializer,PostSerializer,MovieCommentSerializer,PostCommentSerializer
from .models import MovieReview,Post,MovieComment,PostComment
from django.db.models import Count
import requests
from lxml import html
from bs4 import BeautifulSoup



# Create your views here.
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_review_list_create(request):
    if request.method == 'GET':
        movie_reviews = MovieReview.objects.all().order_by('-created_at')
        serializer = MovieReviewSerializer(movie_reviews, many=True)
        return Response(serializer.data)
    else:
        print(request.data)
        serializer = MovieReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_review_list_order_by_like(request):
    movie_reviews = MovieReview.objects.all().annotate(num_likes=Count('like')).order_by('-num_likes')
    serializer = MovieReviewSerializer(movie_reviews, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_review_update_delete(request, movie_review_pk):
    movie_review = get_object_or_404(MovieReview, pk=movie_review_pk)

    if not request.user.movie_reviews.filter(pk=movie_review_pk).exists():
        return Response({'detail': '권한이 없습니다.'})
    
    if request.method == 'PUT':
        serializer = MovieReviewSerializer(movie_review, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        movie_review.delete()
        return Response({ 'id': movie_review_pk })

@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_review_comment_create(request, movie_review_pk):
    movie_review = get_object_or_404(MovieReview, pk=movie_review_pk)
    serializer = MovieCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie_review=movie_review,user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def movie_review_comment_delete(request, comment_pk):
    movie_review_comment = get_object_or_404(MovieComment, pk=comment_pk)
    print(movie_review_comment)

    if not request.user.review_comments.filter(pk=comment_pk).exists():
        return Response({'detail': '권한이 없습니다.'})
    comment = get_object_or_404(MovieComment, pk=comment_pk)
    comment.delete()
    return Response({ 'id': comment_pk })

@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    else:
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_list_order_by_like(request):
    posts = Post.objects.all().annotate(num_likes=Count('like')).order_by('-num_likes')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_update_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if not request.user.posts.filter(pk=post_pk).exists():
        return Response({'detail': '권한이 없습니다.'})
    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    else:
        post.delete()
        return Response({ 'id': post_pk })


@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_comment_create(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = PostCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(post=post,user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def post_comment_delete(request, comment_pk):
    if not request.user.post_comments.filter(pk=comment_pk).exists():
        return Response({'detail': '권한이 없습니다.'})
    comment = get_object_or_404(PostComment, pk=comment_pk)
    comment.delete()
    return Response({ 'id': comment_pk })


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_movie_reviews(request, movie_review_pk):
    movie_review = get_object_or_404(MovieReview, pk=movie_review_pk)
    serializer = MovieReviewSerializer(movie_review)
    username = str(movie_review.user)
    is_review_user=False
    if username == str(request.user):
        is_review_user=True
    newdict={'username':username,'is_review_user':is_review_user}
    newdict.update(serializer.data)
    return Response(newdict)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_movie_review_comments(request,movie_review_pk):
    movie_review = get_object_or_404(MovieReview, pk=movie_review_pk)
    serializer = MovieCommentSerializer(movie_review.review_comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_reviews(request):
    movie_review = MovieReview.objects.filter(user=request.user)
    # for m in movie_review:
    #     print(len(m.like.filter()))
    serializer = MovieReviewSerializer(request.user.movie_reviews, many=True)
    return Response(serializer.data)


@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like_movie_review(request,movie_review_pk):
    movie_review = get_object_or_404(MovieReview, pk=movie_review_pk)
    if request.method == 'POST':
        if movie_review.like.filter(pk=request.user.id).exists():
            movie_review.like.remove(request.user.id)
        else:
            movie_review.like.add(request.user.id)
    is_like_user= False
    if movie_review.like.filter(pk=request.user.id).exists():
        is_like_user = True
    like_users=(len(movie_review.like.filter()))
    newdict={'is_like_user': is_like_user, 'like_users' : like_users}
    return Response(newdict)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_posts(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = PostSerializer(post)
    username = str(post.user)
    is_post_user=False
    if username == str(request.user):
        is_post_user=True
    newdict={'username':username,'is_post_user':is_post_user}
    newdict.update(serializer.data)
    return Response(newdict)

@api_view(['GET','POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like_post(request,post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        if post.like.filter(pk=request.user.id).exists():
            post.like.remove(request.user.id)
        else:
            post.like.add(request.user.id)
    is_like_user= False
    if post.like.filter(pk=request.user.id).exists():
        is_like_user = True
    like_users=(len(post.like.filter()))
    newdict={'is_like_user': is_like_user, 'like_users' : like_users}
    return Response(newdict)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_post_comments(request,post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = PostCommentSerializer(post.post_comments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_movie_info(request,search_value):

    pub_year=request.GET['pubdate'][0:4]
    url='https://openapi.naver.com/v1/search/movie.json?'   
    header_params = {
        "X-Naver-Client-Id":'8Idp51BjlArqf0yFAzqI',
        "X-Naver-Client-Secret":'FyncJk8ARV',
        }
    newdict = { 
        'info' : [],
        }
        
    payload = {'query' : search_value ,'display' : 100}
    response = requests.get(url,params=payload,headers=header_params).json()
    filtered_movie = list(filter(lambda year: year['pubDate']== pub_year,response.get('items')))

    if (filtered_movie):
        movie_info_url = filtered_movie[0]['link']
        movie_info_page = requests.get(movie_info_url)

        soup = BeautifulSoup(movie_info_page.text, 'html.parser')
        
        
        one_line_script=soup.select (
            'div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(1) > div > div > strong'
        )
        one_line_script_actor=soup.select (
            'div.article > div:nth-child(7) > div:nth-child(1) > div > ul > li:nth-child(1) > div >  em > span'
        )
        result = soup.select (
            'div.article > div.section_group.section_group_frst > div > div > ul > li > a.thumb_people > img'
        )
        newdict['script']=one_line_script[0].get_text()
        newdict['script_actor']=one_line_script_actor[0].get_text()
        for res in result:
            tmp = {'img' : res.get('src'),'name' : res.get('alt')}
            newdict['info'].append(tmp)
            

    return Response(newdict)


def get_code(url):
    url_len = len(url)
    for i in range(url_len-1,-1,-1):
        if url[i] == '=':
            return url[i+1:url_len]