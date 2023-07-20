from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bmw_club_bg.common.forms import CommentForm, CreatePostForm
from bmw_club_bg.common.models import Post
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

        scroll_position = self.request.session.pop('scroll_position', 0)
        context['scroll_position'] = scroll_position

        if user.is_authenticated:
            liked_posts = user.liked_posts.all()
        context['liked_posts'] = liked_posts

        return context

@login_required
def like_post(request, pk, action):
    print("Post ID:", pk)
    print("Action:", action)
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
        context['comment_form'] = CommentForm()

        return context


@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post_id = pk
            comment.save()
    return redirect('details_post', pk=pk)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'posts/post-add-page.html'
    success_url = reverse_lazy('home')  # Redirect to the home page after successful creation

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save(commit=False)  # Save the form data without committing to the database
        post.save()  # Save the post to generate the post ID

        group_data = form.cleaned_data.get('group')
        print(group_data)
        post.groups.set([group_data])

        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/post-edit-page.html'
    context_object_name = 'post'
    fields = ['content', 'location', 'image_url']
    success_url = reverse_lazy('home')

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
        if post.author != self.request.user:
            raise Http404("You are not allowed to delete this post.")
        return post