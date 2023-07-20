from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bmw_club_bg.common.models import Post
from bmw_club_bg.groups.forms import CreateGroupForm, UpdateGroupForm
from bmw_club_bg.groups.models import Group


class GroupListView(ListView):
    model = Group
    template_name = 'groups/groups-page.html'
    paginate_by = 5  # Number of groups per page

    def get_queryset(self):
        search_query = self.request.GET.get('search_query', None)
        queryset = Group.objects.all().order_by('-date_of_creation')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset


@login_required
def join_group(request, pk):
    print(pk)
    group = get_object_or_404(Group, pk=pk)
    group.users.add(request.user)
    messages.success(request, f"You have joined the group: {group.name}")
    return redirect('groups')

@login_required
def leave_group(request, pk):
    print(pk)
    group = get_object_or_404(Group, pk=pk)
    group.users.remove(request.user)
    messages.success(request, f"You have left the group: {group.name}")
    return redirect('groups')


class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group-posts-page.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group = self.get_object()
        search_query = self.request.GET.get('search_query', None)

        if search_query:
            context['posts'] = Post.objects.filter(groups=group, author__username__icontains=search_query).order_by('-date')
        else:
            context['posts'] = Post.objects.filter(groups=group).order_by('-date')

        return context


class CreateGroupView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = 'groups/group-add-page.html'
    success_url = reverse_lazy('groups')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)

        # Add the current user to the users field of the newly created group
        self.object.users.add(self.request.user)

        return response


class UpdateGroupView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = UpdateGroupForm
    template_name = 'groups/group-edit-page.html'
    success_url = reverse_lazy('groups')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.created_by == self.request.user:
            # If the user is not the creator of the group, raise a 403 Forbidden error
            raise PermissionDenied("You do not have permission to edit this group.")
        return obj



class DeleteGroupView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = 'groups/group-delete-page.html'
    success_url = reverse_lazy('groups')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj.created_by == self.request.user:
            # If the user is not the creator of the group, raise a 403 Forbidden error
            raise PermissionDenied("You do not have permission to delete this group.")
        return obj