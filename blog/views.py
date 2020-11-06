from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Post, Like
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from django.contrib.auth.decorators import login_required


# Create your views here.


# model for the post list for the blog
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_created', '-date_published', 'id']
    paginate_by = 5


# model for details for the view
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post-detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']
    success_message = "Blog post successful"

    def form_valid(self, form):  # pre-populate author field with the current user
        form.instance.author = self.request.user  # assign author field with the user
        return super(PostCreateView, self).form_valid(form)

    # to use kwargs access using object i.e. use self.object.name
    # remove this if you want to use get_absolute_url
    def get_success_url(self):
        return reverse_lazy('blog-home')


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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Post
    success_url = '/blog/'
    success_message = "Post updated successful"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    # def get_success_url(self):
    #     return reverse_lazy('blog-home')


@login_required
def post_like(request):
    # user = request.user
    # if request.method == 'POST' and request.is_ajax():
    if request.POST.get('action') == 'post':
        result = ''
        postid = int(request.POST.get('post_id'))
        post_obj = get_object_or_404(Post, id=postid)

        if post_obj.likes.filter(id=request.user.id).exists():
            post_obj.likes.remove(request.user)
            post_obj.like_count -= 1
            result = post_obj.like_count
            post_obj.save()
        else:
            post_obj.likes.add(request.user)
            post_obj.like_count += 1
            result = post_obj.like_count
            post_obj.save()
        
        return JsonResponse({'result': post_obj.like_count,})
    return HttpResponse("Error access denied")





