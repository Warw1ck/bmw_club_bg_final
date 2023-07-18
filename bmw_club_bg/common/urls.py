from django.urls import path, include

from bmw_club_bg.common.views import UserPostListView, like_post, dislike_post, PostDetailView, add_comment, \
    CreatePostView




urlpatterns = [
    path('', UserPostListView.as_view(), name='home'),
    path('like/<int:pk>/', like_post, name='like'),
    path('dislike/<int:pk>/', dislike_post, name='dislike'),
    path('post/', include([
        path('<int:pk>/', PostDetailView.as_view(), name='details_post'),
        path('add/', CreatePostView.as_view(), name='add_post'),

    ])),

    path('comment/<int:pk>/', add_comment, name='add_comment'),

]