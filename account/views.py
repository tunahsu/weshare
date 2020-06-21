from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from account.forms import MyUserCreationForm, MyUserChangeForm, ChangeAvatarForm
from account.models import Contact
from post.models import Post


def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return render(
                request,
                'account/register_done.html'
            )
    else:
        form = MyUserCreationForm()
    return render(
        request,
        'account/register.html',
        {
            'form': form
        }
    )

@login_required
def user_profile(request, username):
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    user = User.objects.get(username=username)
    form = ChangeAvatarForm()
    # recommend_users = get_recommend_users(request.user)
    posts = Post.objects.filter(user=user)
    paginator = Paginator(posts, 12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'account/user_profile.html',
        {
            'user': user,
            'posts': posts,
            'form': form
        }
    )

@login_required
def user_edit(request):
    if request.method == 'POST':
        form = MyUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    form = MyUserChangeForm(instance=request.user)
    return render(
        request,
        'account/user_edit.html',
        {
            'form': form
        }
    )

@login_required
def user_follow(request, username):
    user = User.objects.get(username=username)
    con = Contact(user_from=request.user, user_to=user)
    con.save()
    return redirect(
        'account:user_profile',
        username=username
    )

@login_required
def user_unfollow(request, username):
    user = User.objects.get(username=username)
    con = Contact.objects.get(user_from=request.user, user_to=user)
    con.delete()
    return redirect(
        'account:user_profile',
        username=username
    )