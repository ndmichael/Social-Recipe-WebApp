from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Post
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.contrib.auth.decorators import login_required


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_created', '-date_published', 'id']
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    success_message = "Blog post created successful"

    def form_valid(self, form):  # pre-populate author field with the current user
        form.instance.author = self.request.user  # assign author field with the user
        return super(PostCreateView, self).form_valid(form)

    # remove this if you want to use get_absolute_url
    def get_success_url(self):
        return reverse_lazy('blog-home')


# user must be login and the author to update this post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    success_message = "Post updated successful"

    def form_valid(self, form):  # pre-populate author field with the current user
        form.instance.author = self.request.user  # assign author field with the user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# user must be login and the author to delete this post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = '/blog/'
    success_message = "Post updated successful"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# the like button view
@login_required
def post_like(request):
    # if request.method == 'POST' and request.is_ajax():
    if request.POST.get('action') == 'post':
        result = ''
        flag = None
        postid = int(request.POST.get('post_id'))
        post_obj = get_object_or_404(Post, id=postid)

        if post_obj.likes.filter(id=request.user.id).exists():
            post_obj.likes.remove(request.user)
            post_obj.like_count -= 1
            result = post_obj.like_count
            post_obj.save()
            flag = False
        else:
            post_obj.likes.add(request.user)
            post_obj.like_count += 1
            result = post_obj.like_count
            post_obj.save()
            flag = True
        
        return JsonResponse({'result': result, 'flag': flag,})
    return HttpResponse("Error access denied")





