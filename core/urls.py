from django.urls import path
from core.views import *

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('post/new/', CreatePost.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', UpdatePost.as_view(), name='post_edit'),
    path('post/<pk>/remove/', DeletePost.as_view(), name='post_remove'),
    path('post/<int:pk>/comment/', CreateComment.as_view(), name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', approve_comment, name='comment_approve'),
    path('comment/<int:pk>/remove/', delete_comment, name='comment_remove'),
]
