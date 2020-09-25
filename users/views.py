from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from blog.models import Post
from cookella.models import FoodType
from django.views.generic import ListView
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username} you  can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# the profile view now receive an attribute which is the current username
# i needed a way when the update form filled it reloads back to the profile with the updated name
# i could use the get absolute url on the model but it doesn't update the profile
@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)  # getting the current user passed to it
    user_post = Post.objects.filter(author=user)
    contribution_count = FoodType.objects.filter(contributor=user).count()
    post_count = user_post.count()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,  instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'account successfully updated')
            return redirect('profile', username=request.user.username)  # i solved that by passing the requesting user username
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user': user,
        'post_count': post_count,
        'contribution_count': contribution_count,


    }
    return render(request, 'users/profile.html', context)


# handles the view for the user list template.
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))  # getting the username on the fly
        return Post.objects.filter(author=user).order_by('-date_created')


# handles the view for the user contribution list template.
class ContributorListView(ListView):
    model = FoodType
    template_name = 'users/user_contribution.html'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))  # getting the username on the fly
        return FoodType.objects.filter(contributor=user).order_by('-date_added')