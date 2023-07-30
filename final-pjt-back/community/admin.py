from django.contrib import admin
from .models import MovieComment,MovieReview,Post,PostComment # 명시적 상대경로 표현

# Register your models here.
admin.site.register(MovieComment)
admin.site.register(MovieReview)
admin.site.register(Post)
admin.site.register(PostComment)
