from django.urls import path
from django.conf.urls import include
from .views import *

urlpatterns = [
  path('', HomeView.as_view(), name="home"),
  path('article/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
  path('add_post/', AddPostView.as_view(),  name="add_post"),
  path('add_category/', AddCategoryView.as_view(), name="add_category"),
  path('article/edit/<int:pk>', UpdatePostView.as_view(), name ='update_post'),
  path('article/<int:pk>/delete', DeletePostView.as_view(), name ='delete_post'),
  path('category/<str:cats>/', CategoryView, name ='category'),
  path('category-list/', CategoryListView, name ='category-list'),
  path('article/53', ArticleDetailView.as_view(),name="execute_order_article"),
  path('article/52', ArticleDetailView.as_view(),name="vaultafed_article"),
  path('article/51', ArticleDetailView.as_view(),name="file_encryption_article"),


  path('like/<int:pk>', LikeView, name="like_post"),
  path('article/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
  path('search_posts', search_posts, name = "search_posts"),
]
