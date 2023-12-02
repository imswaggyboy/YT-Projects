from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('post/new', views.PostCreateView.as_view(), name='post-create'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/', views.post_details, name='post_detail'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('comment-like/<int:pk>/', views.like_comment, name='like_comment'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/update/',
          views.PostUpdateView.as_view(),
            name='post_update'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/delete/',
          views.PostDeleteView.as_view(),
            name='post_delete'),
    path('tagged-posts/<int:id>',views.post_tag_view , name='tagged_posts'),
    path('search/', views.post_search, name='post_search'),

]