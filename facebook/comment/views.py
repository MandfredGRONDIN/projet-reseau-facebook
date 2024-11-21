from django.views.generic import ListView, CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment
from .forms import CommentForm
from post.models import Post

class CommentListView(ListView):
    model = Comment
    template_name = 'comments/comment_list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.filter(parent_comment__isnull=True).order_by('-created_at')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.POST.get('next', reverse('home'))
