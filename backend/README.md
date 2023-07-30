## intro
시작할 떄 
`pip install –r requirements.txt`
`python manage.py loaddata accounts/accounts.json`
`python manage.py loaddata community/community.json`
## 11/19

project 설정

1. project 이름, app 설치

2. `settings.py` 에 필요한 것 추가

   ```python
   AUTH_USER_MODEL = 'accounts.User'
   INSTALLED_APPS = [
       'accounts',
       'community',
       'rest_framework',
       'corsheaders',
   ]
   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
   ]
   CORS_ALLOWED_ORIGINS = [
       'http://localhost:8080',
   ]
   ```

3. `models.py` 설정

   user, movie_review, post

4. `serializers.py` 설정

5. `admin` 설정

6. `ulrs.py` 설정

   - accounts

     ```python
     urlpatterns = [
         path('signup/', views.signup),
         path('api-token-auth/', obtain_jwt_token),
     ]
     ```

   - community

     ```python
     urlpatterns = [
         path('movie_review_list_create/',views.movie_review_list_create),
         path('movie_review_update_delete/<int:movie_review_pk>/',views.movie_review_update_delete),
         path('movie_review_comment_create/<int:movie_review_pk>/',views.movie_review_comment_create),
         path('movie_review_comment_delete/<int:comment_pk>/',views.movie_review_comment_delete),
     
         path('post_list_create/',views.post_list_create),
         path('post_update_delete/<int:post_pk>/',views.post_create),
         path('post_comment_create/<int:post_pk>/',views.post_comment_create),
         path('post_comment_delete/<int:comment_pk>/',views.post_comment_delete)
     ]
     ```

7. `views.py` 설정

   ```python
   from django.shortcuts import get_object_or_404
   from rest_framework import status
   from rest_framework.decorators import api_view
   from rest_framework.response import Response
   from .serializers import MovieReviewSerializer,PostSerializer,MovieCommentSerializer,PostCommentSerializer
   from .models import MovieReview,Post,MovieComment,PostComment
   
   
   # Create your views here.
   @api_view(['GET', 'POST'])
   def movie_review_list_create(request):
       if request.method == 'GET':
           movie_reviews = MovieReview.objects.all()
           serializer = MovieReviewSerializer(movie_reviews, many=True)
           # serializer = MovieReviewSerializer(request.user.movie_reviews, many=True)
           return Response(serializer.data)
       else:
           serializer = MovieReviewSerializer(data=request.data)
           if serializer.is_valid(raise_exception=True):
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
   
   
   @api_view(['PUT', 'DELETE'])
   def movie_review_update_delete(request, movie_review_pk):
       movie_review = get_object_or_404(MovieReview, pk=movie_review_pk)
   
       # if not request.user.movie_reviews.filter(pk=movie_review_pk).exists():
       #     return Response({'detail': '권한이 없습니다.'})
       
       if request.method == 'PUT':
           serializer = MovieReviewSerializer(movie_review, data=request.data)
           if serializer.is_valid(raise_exception=True):
               serializer.save()
               return Response(serializer.data)
       else:
           movie_review.delete()
           return Response({ 'id': movie_review_pk })
   
   @api_view(['POST'])
   def movie_review_comment_create(request, movie_review_pk):
       movie_review = get_object_or_404(MovieReview, pk=movie_review_pk)
       serializer = MovieCommentSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):
           serializer.save(movie_review=movie_review)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
   
   @api_view(['DELETE'])
   def movie_review_comment_delete(request, comment_pk):
       print('yyyyyyyyyyyyyy')
       comment = get_object_or_404(MovieComment, pk=comment_pk)
       comment.delete()
       return Response({ 'id': comment_pk })
   
   @api_view(['GET', 'POST'])
   def post_list_create(request):
       if request.method == 'GET':
           posts = Post.objects.all()
           serializer = PostSerializer(posts, many=True)
           # serializer = PostSerializer(request.user.posts, many=True)
           return Response(serializer.data)
       else:
           serializer = PostSerializer(data=request.data)
           if serializer.is_valid(raise_exception=True):
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
   
   @api_view(['PUT', 'DELETE'])
   def post_create(request, post_pk):
       post = get_object_or_404(Post, pk=post_pk)
   
       # if not request.user.posts.filter(pk=post_pk).exists():
       #     return Response({'detail': '권한이 없습니다.'})
   
       if request.method == 'PUT':
           serializer = PostSerializer(post, data=request.data)
           if serializer.is_valid(raise_exception=True):
               serializer.save()
               return Response(serializer.data)
       else:
           post.delete()
           return Response({ 'id': post_pk })
   
   
   @api_view(['POST'])
   def post_comment_create(request, post_pk):
       post = get_object_or_404(Post, pk=post_pk)
       serializer = PostSerializer(data=request.data)
       if serializer.is_valid(raise_exception=True):
           serializer.save(post=post)
           return Response(serializer.data, status=status.HTTP_201_CREATED)
   
   @api_view(['DELETE'])
   def post_comment_delete(request, comment_pk):
       comment = get_object_or_404(PostComment, pk=comment_pk)
       comment.delete()
       return Response({ 'id': comment_pk })
   
   ```

   





```python
class NaverMovieMaker:
    client_id = '8Idp51BjlArqf0yFAzqI'
    client_secret = 'FyncJk8ARV'
    url='https://openapi.naver.com/v1/search/movie.json?'
    header_params = {
        "X-Naver-Client-Id":client_id,
        "X-Naver-Client-Secret":client_secret
        }

def naver_movie_search_basic(search_text):
    base_url = NaverMovieMaker()
    payload = {'query' : search_text }
    response = requests.get(base_url.url,params=payload,headers=base_url.header_params).json()

    if response.get('total')==0:
        return 
    else:
        result = [ (item.get('title').replace('<b>','').replace('</b>',''), item.get('userRating')) for item in response.get('items')]
        return sorted(result, key =lambda score:score[1],reverse=True)

def naver_movie_search_year(search_text,yearfrom,yearto):
    base_url = NaverMovieMaker()
    payload = {'query' : search_text,'yearfrom' : yearfrom, 'yearto' : yearto}
    response = requests.get(base_url.url,params=payload,headers=base_url.header_params).json()
    result = []
    for item in response.get('items'):
        
        year=int(item.get('pubDate'))
        if year<=yearto and year >= yearfrom:
            result.append((item.get('title').replace('<b>','').replace('</b>',''), item.get('userRating')))

    return sorted(result, key =lambda score:score[1],reverse=True)

print(naver_movie_search_basic('스타워즈'))

print(naver_movie_search_year('스타워즈',2015,2020))

```

https://openapi.naver.com/v1/search/movie.json