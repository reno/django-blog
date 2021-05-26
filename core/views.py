from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from core.models import Post, Comment


class Login(LoginView):
    template_name = 'core/login.html'


class Logout(LogoutView):
    template_name = 'core/logout.html'


class PostList(ListView):
    queryset = Post.objects.all().order_by('-created_at')
    paginate_by = 5


class PostDetail(DetailView):
    model = Post


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'core/post_create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'core/post_update.html'

    def get_success_url(self, **kwargs):
        return self.object.get_absolute_url()


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    # bypass delete confirmation
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CreateComment(CreateView):
    model = Comment
    fields = ['author', 'text']
    template_name = 'core/add_comment_to_post.html'

    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs['pk'])
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post.get_absolute_url()


@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)