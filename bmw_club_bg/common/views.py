import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse, request
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bmw_club_bg.common.forms import CreatePostForm
from bmw_club_bg.common.models import Post, Comment
from bmw_club_bg.notifications.models import Notification


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'common/home-page.html'

    def get_queryset(self):
        user = self.request.user
        search_query = self.request.GET.get('search_query', None)

        if search_query:
            queryset = Post.objects.filter(author__username__icontains=search_query, groups__users=user).order_by(
                '-date')
        else:
            queryset = Post.objects.filter(groups__users=user).order_by('-date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked_posts = []
        user = self.request.user


        if user.is_authenticated:
            liked_posts = user.liked_posts.all()
        context['liked_posts'] = liked_posts

        # Add post URLs to the context
        for post in context['object_list']:
            post_url = self.request.build_absolute_uri(reverse('details_post', args=[post.pk]))
            post.post_url = post_url

        return context



@login_required
def like_post(request, pk, action):
    post = get_object_or_404(Post, id=pk)
    if action == 'like':
        post.likes.add(request.user)
    elif action == 'dislike':
        post.likes.remove(request.user)
    else:
        return JsonResponse({'success': False})

    if request.user != post.author:  # Avoid sending notification if the user liked their own post
        notification_content = f"liked your post: {post.content}"
        notification = Notification(user=post.author, user_like=request.user, content=notification_content)
        notification.save()

    return JsonResponse({'success': True, 'action': action})


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked_posts = []
        user = self.request.user
        if user.is_authenticated:
            liked_posts = user.liked_posts.all()
        context['liked_posts'] = liked_posts
        context['now_user'] = user
        context['group_chef'] = self.object.groups.first().created_by

        return context



@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON data
            comment_text = data.get('comment')  # Get the comment from the JSON data
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if not comment_text:
            return JsonResponse({'error': 'Comment is empty'}, status=400)

        # Save the comment to the database
        comment = Comment(user=request.user, post=post, comment=comment_text)
        comment.save()

        # Return the new comment data as JSON
        return JsonResponse({
            'user': {
                'username': comment.user.username,
                'profile': {
                    'first_name': comment.user.profile.first_name,
                    'last_name': comment.user.profile.last_name,
                    'image': comment.user.profile.image.url if comment.user.profile.image else None,
                    # Include other profile attributes as needed...
                }},

            'comment': comment.comment,
            'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    # Return an empty JSON response for non-POST requests
    return JsonResponse({})

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'posts/post-add-page.html'

    def get_success_url(self):
        # Redirect to the details page of the newly created post
        return reverse('details_post', args=[self.object.pk])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)  # Save the form data without committing to the database
        post.save()  # Save the post to generate the post ID

        group_data = form.cleaned_data.get('group')
        post.groups.set([group_data])

        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post-edit-page.html'
    context_object_name = 'post'
    fields = ['content', 'location', 'image_url']

    def get_success_url(self):
        # Redirect to the details page of the newly updated post
        return reverse('details_post', args=[self.object.pk])

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author != self.request.user:
            # If the user is not the author of the post, return a 404 error
            raise Http404
        return post

    def form_valid(self, form):
        response = super().form_valid(form)
        # Perform any additional actions after the form is successfully validated
        return response


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post-delete-page.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author != self.request.user and self.request.user != post.groups.first().created_by:
            raise Http404("You are not allowed to delete this post.")
        return post
