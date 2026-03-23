from django.urls import path

from blog.views import index, category_detail, post_detail, create_category, create_post, PostListView, PostDetailView

urlpatterns = [
    path('', index, name='index'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('create_category/', create_category, name='create_category'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('post_detail/<int:pk>/detail/', PostDetailView.as_view(), name='post_detail_view')
]