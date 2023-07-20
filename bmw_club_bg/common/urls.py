from django.urls import path, include

from bmw_club_bg.common.views import UserPostListView, like_post, PostDetailView, add_comment, \
    CreatePostView, EditPostView, DeletePostView

urlpatterns = [
    path('', UserPostListView.as_view(), name='home'),
    path('like_post/<int:pk>/<str:action>/', like_post, name='like_post'),
    path('post/', include([
        path('<int:pk>/', PostDetailView.as_view(), name='details_post'),
        path('add/', CreatePostView.as_view(), name='add_post'),
        path('edit/<int:pk>/', EditPostView.as_view(), name='edit_post'),
        path('delete/<int:pk>/', DeletePostView.as_view(), name='delete_post'),
    ])),

    path('comment/<int:pk>/', add_comment, name='add_comment'),

]